import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import pairwise_distances

def evaluate_projection_error(X_orig, X_proj, save_path="output/distortion_plot.png"):
    D_orig = pairwise_distances(X_orig)
    D_proj = pairwise_distances(X_proj)

    triu_idx = np.triu_indices_from(D_orig, k=1)
    orig_dists = D_orig[triu_idx]
    proj_dists = D_proj[triu_idx]

    mask = orig_dists > 1e-8
    rel_errors = np.zeros_like(orig_dists)
    rel_errors[mask] = np.abs(proj_dists[mask] - orig_dists[mask]) / orig_dists[mask]

    mean_err = rel_errors.mean()
    max_err = rel_errors.max()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    ax1.scatter(orig_dists, proj_dists, alpha=0.6)
    ax1.set_title("Original vs Projected Distances")
    ax1.set_xlabel("Original")
    ax1.set_ylabel("Projected")
    ax1.grid(True)

    ax2.hist(rel_errors, bins=15, color="orange", edgecolor="black")
    ax2.set_title(f"Relative Error Distribution\nMean={mean_err:.4f}, Max={max_err:.4f}")
    ax2.set_xlabel("Relative Error")
    ax2.set_ylabel("Count")
    ax2.grid(True)

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

    print(f"[✓] Saved plot to {save_path}")
    return mean_err, max_err