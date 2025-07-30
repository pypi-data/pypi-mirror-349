# src/cka_analyzer/pca_analysis.py

import os
import torch
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from transformers import AutoTokenizer, AutoModelForCausalLM
from sklearn.decomposition import PCA

def run_pca_shift(
    model_reference_path: str,
    model_path: str,
    texts: list[str],
    output_path: str,
    device: str = "cuda",
    max_length: int = 128
):
    """
    Compute and plot PCA shift vs principal component for a list of texts,
    comparing a reference model to an updated model.
    
    Args:
      model_reference_path: HF or local path to the reference model.
      model_path:           HF or local path to the updated model.
      texts:                List of raw text strings to analyze.
      output_path:          Path to save a PDF figure.
      max_length:           Tokenizer max_length for truncation/padding.
    """

    # Load tokenizer once
    tokenizer = AutoTokenizer.from_pretrained(model_reference_path, trust_remote_code=True)

    # Helper to load & move a causal LM
    def load_model(path):
        return (AutoModelForCausalLM
                .from_pretrained(path,
                                 torch_dtype=torch.bfloat16,
                                 trust_remote_code=True)
                .to(device)
                .eval())

    # Load both models
    model_ref = load_model(model_reference_path)
    model_upd = load_model(model_path)

    # Extract mean hidden state at a given layer
    def extract_mean_hidden(model, layer_idx):
        inputs = tokenizer(
            texts,
            return_tensors="pt",
            padding="max_length",
            truncation=True,
            max_length=max_length
        ).to(device)
        with torch.no_grad():
            outs = model(**inputs, output_hidden_states=True)
        # take hidden_states[layer_idx], shape (batch, seq, hidden)
        hs = outs.hidden_states[layer_idx].float().cpu().numpy()
        # mean over sequence dimension → (batch, hidden)
        return hs.mean(axis=1)

    # Determine number of layers
    cfg = model_ref.config
    n_layers = getattr(cfg, "num_hidden_layers", None) or getattr(cfg, "n_layer", None)
    if n_layers is None:
        n_layers = len(model_ref.model.layers)
    # include embedding layer as layer 0
    layers = list(range(n_layers + 1))

    records = []
    for L in layers:
        # Extract features for each model
        feat_ref = extract_mean_hidden(model_ref, L)
        feat_upd = extract_mean_hidden(model_upd, L)

        # Fit PCA on reference features
        pca = PCA(n_components=2).fit(feat_ref)
        comp1, comp2 = pca.components_

        # Project and average along PC1 & PC2
        pc1_ref = feat_ref.dot(comp1).mean()
        pc2_ref = feat_ref.dot(comp2).mean()
        pc1_upd = feat_upd.dot(comp1).mean()
        pc2_upd = feat_upd.dot(comp2).mean()

        records.append({
            "layer":     L,
            "state":   "Reference",
            "shift":      0.0,
            "principal":  pc2_ref
        })
        records.append({
            "layer":     L,
            "state":   "Updated",
            "shift":      pc1_upd - pc1_ref,
            "principal":  pc2_upd
        })

    # Build DataFrame
    df = pd.DataFrame(records)

    # Plot style
    mpl.rcParams.update({
        'font.family': 'serif',
        'font.size': 18,
        'axes.titlesize': 20,
        'axes.labelsize': 18,
        'xtick.labelsize': 16,
        'ytick.labelsize': 16,
        'axes.grid': True,
        'grid.linestyle': '--',
        'lines.linewidth': 2,
    })

    fig, ax = plt.subplots(figsize=(6,4))
    # grey lines connecting points at each layer
    for L in df["layer"].unique():
        sub = df[df["layer"] == L]
        ax.plot(sub["shift"], sub["principal"], color="gray", alpha=0.5, zorder=1)

    # scatter points
    markers = {"Reference": "o", "Updated": "^"}
    colors  = {"Reference": "#0072B2", "Updated": "#D55E00"}
    for state in ["Reference", "Updated"]:
        sub = df[df["state"] == state]
        ax.scatter(
            sub["shift"], sub["principal"],
            marker=markers[state],
            color=colors[state],
            edgecolors="black",
            label=state,
            zorder=2
        )

    ax.set_xlabel("Δ PC1")
    ax.set_ylabel("PC2")
    ax.set_title("PCA Shift vs. Principal Component")
    ax.legend(loc="best")
    fig.tight_layout()

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig.savefig(output_path, bbox_inches="tight", dpi=300)
    plt.close(fig)
