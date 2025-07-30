# src/cka_analyzer/pca_similarity.py

import os
import torch
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from transformers import AutoTokenizer, AutoModelForCausalLM
from sklearn.decomposition import PCA

def run_pca_similarity(
    model_reference_path: str,
    model_path: str,
    texts: list[str],
    output_path: str,
    max_length: int = 128
):
    """
    Compute and plot the cosine similarity between the first principal components
    of a reference and an updated model, layer by layer.

    Args:
        model_reference_path: Path or HuggingFace ID for the reference model.
        model_path:           Path or HuggingFace ID for the updated model.
        texts:                List of input strings to analyze.
        output_path:          Path to save the PDF plot.
        max_length:           Tokenizer max_length for truncation/padding.
    """
    # 1) Set up device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # 2) Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(
        model_reference_path, trust_remote_code=True
    )

    # 3) Helper to load & move a causal LM
    def load_model(path):
        return (AutoModelForCausalLM
                .from_pretrained(
                    path,
                    torch_dtype=torch.bfloat16,
                    trust_remote_code=True
                )
                .to(device)
                .eval())

    # 4) Load both models
    model_ref = load_model(model_reference_path)
    model_upd = load_model(model_path)

    # 5) Determine number of layers (+1 for embedding)
    cfg = model_ref.config
    n = getattr(cfg, "num_hidden_layers", None) or getattr(cfg, "n_layer", None)
    if n is None:
        n = len(model_ref.model.layers)
    layers = list(range(n + 1))

    # 6) Function to extract mean hidden state at one layer
    def extract_mean(model, layer_idx):
        enc = tokenizer(
            texts, return_tensors="pt",
            padding=True, truncation=True, max_length=max_length
        ).to(device)
        with torch.no_grad():
            out = model(**enc, output_hidden_states=True)
        hs = out.hidden_states[layer_idx].float().cpu().numpy()
        return hs.mean(axis=1)

    # 7) Compute first principal component for each layer on reference
    pcs_ref = {}
    for L in layers:
        feats_ref = extract_mean(model_ref, L)
        pcs_ref[L] = PCA(n_components=1).fit(feats_ref).components_[0]

    # 8) Compute cosine similarities
    sims = []
    for L in layers:
        comp_ref = pcs_ref[L]
        feats_upd = extract_mean(model_upd, L)
        comp_upd = PCA(n_components=1).fit(feats_upd).components_[0]
        cos = (comp_ref @ comp_upd) / (np.linalg.norm(comp_ref) * np.linalg.norm(comp_upd))
        sims.append(cos)

    # 9) Plot styling
    mpl.rcParams.update({
        'font.family':    'serif',
        'font.serif':     ['DejaVu Serif'],
        'font.size':      18,
        'axes.titlesize': 20,
        'axes.labelsize': 18,
        'xtick.labelsize':16,
        'ytick.labelsize':16,
        'lines.linewidth':2,
        'axes.grid':      True,
        'grid.linestyle': '--',
        'grid.linewidth': 0.5,
    })

    # 10) Plot
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(
        layers, sims, '-o',
        color='#0072B2', label='Updated vs Reference'
    )
    ax.set_xlabel("Layer index")
    ax.set_ylabel("Cosine similarity of PC1")
    ax.set_title("Layer-wise PCA Similarity")
    ax.set_ylim(-1, 1)
    ax.legend(loc="best")
    fig.tight_layout()

    # 11) Save
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close(fig)
