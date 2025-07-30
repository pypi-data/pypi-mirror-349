import os
import torch
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from torch.utils.data import Dataset, DataLoader
from transformers import AutoTokenizer, AutoModelForCausalLM


def run_fim_analysis(
    model_reference_path: str,
    model_path: str,
    texts: list[str],
    output_dir: str,
    batch_size: int = 4,
    num_batches: int = 10,
    max_length: int = 128,
    layers_to_analyze: list[int] | None = None,
):
    """
    Compare the reference and updated models by computing the diagonal of the
    Fisher Information Matrix (FIM) for specified layers, then plot histograms
    of these values for each layer.

    Args:
        model_reference_path: Path or identifier for the reference (original) model.
        model_path: Path or identifier for the updated model.
        texts: List of input text strings for analysis.
        output_dir: Directory where output histograms will be saved.
        batch_size: Number of samples per inference batch.
        num_batches: Number of batches to use for FIM estimation.
        max_length: Maximum token length for padding/truncation.
        layers_to_analyze: Specific layer indices to analyze; if None, all layers.
    """
    # Determine compute device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Load tokenizer and define a helper to load models
    tokenizer = AutoTokenizer.from_pretrained(model_reference_path, use_fast=True)
    def load_model(path: str) -> AutoModelForCausalLM:
        """Load and prepare a causal language model."""
        model = AutoModelForCausalLM.from_pretrained(
            path,
            torch_dtype=torch.bfloat16,
            trust_remote_code=True
        )
        return model.to(device).eval()

    # Instantiate reference and updated models
    model_ref = load_model(model_reference_path)
    model_upd = load_model(model_path)

    # Automatically detect layers if not specified
    if layers_to_analyze is None:
        cfg = model_ref.config
        n = getattr(cfg, "num_hidden_layers", None) or getattr(cfg, "n_layer", None)
        if n is None:
            # Fallback: inspect loaded model
            n = len(model_ref.model.layers)
        layers_to_analyze = list(range(n))

    # Prepare dataset and dataloader for input texts
    class TextDataset(Dataset):
        def __init__(self, texts: list[str]):
            # Tokenize with padding and truncation
            enc = tokenizer(
                texts,
                return_tensors="pt",
                truncation=True,
                padding="max_length",
                max_length=max_length
            )
            self.input_ids = enc["input_ids"]
            self.attention_mask = enc["attention_mask"]
            self.labels = enc["input_ids"]  # Labels equal inputs for loss computation

        def __len__(self) -> int:
            return self.input_ids.size(0)

        def __getitem__(self, idx: int) -> dict:
            return {
                "input_ids": self.input_ids[idx],
                "attention_mask": self.attention_mask[idx],
                "labels": self.labels[idx],
            }

    loader = DataLoader(
        TextDataset(texts),
        batch_size=batch_size,
        shuffle=False
    )

    # Function to compute diagonal of the Fisher Information Matrix for a layer
    def compute_fim_diag(model: AutoModelForCausalLM, layer_key: str) -> np.ndarray:
        # Collect parameters belonging to the specified layer
        params = [p for name, p in model.named_parameters() if p.requires_grad and layer_key in name]
        # Initialize accumulator for squared gradients
        acc = [torch.zeros_like(p) for p in params]

        for i, batch in enumerate(loader):
            if i >= num_batches:
                break
            # Move batch data to the compute device
            batch = {k: v.to(device) for k, v in batch.items()}
            # Zero gradients before backward pass
            model.zero_grad()
            # Forward pass with labels to compute loss
            loss = model(
                input_ids=batch["input_ids"],
                attention_mask=batch["attention_mask"],
                labels=batch["labels"]
            ).loss
            # Backward pass to accumulate gradients
            loss.backward()
            # Accumulate squared gradients for each parameter
            for j, p in enumerate(params):
                acc[j] += p.grad.detach() ** 2

        # Average the accumulated squared gradients
        denom = min(len(loader), num_batches)
        # Flatten and concatenate all parameter arrays
        fim_values = torch.cat([a.view(-1).float() / denom for a in acc]).cpu().numpy()
        return fim_values

    # Configure global plotting style
    mpl.rcParams.update({
        'font.size': 16,
        'axes.grid': True,
        'grid.linestyle': '--',
        'grid.linewidth': 0.5,
    })

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Iterate over layers and plot FIM histograms
    for L in layers_to_analyze:
        layer_key = f"model.layers.{L}"
        # Compute FIM diagonal for both models
        fim_ref = compute_fim_diag(model_ref, layer_key)
        fim_upd = compute_fim_diag(model_upd, layer_key)

        # Create histogram plot
        fig, ax = plt.subplots(figsize=(5, 3))
        ax.hist(fim_ref, bins=40, histtype='step', label="Reference")
        ax.hist(fim_upd, bins=40, histtype='step', label="Updated")

        ax.set_xscale('log')  # Log scale for better dynamic range
        ax.set_xlabel("FIM diagonal values (log scale)")
        ax.set_ylabel("Frequency")
        ax.set_title(f"FIM Histogram @ Layer {L}")
        ax.legend(loc="upper right")

        fig.tight_layout()
        fig.savefig(os.path.join(output_dir, f"layer_{L}.pdf"), dpi=300, bbox_inches='tight')
        plt.close(fig)

    print(f"[✓] All histograms saved under '{output_dir}'")



