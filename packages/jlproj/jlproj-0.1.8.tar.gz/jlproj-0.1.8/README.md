[![PyPI version](https://badge.fury.io/py/jlproj.svg)](https://pypi.org/project/jlproj/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://static.pepy.tech/badge/jlproj)](https://pepy.tech/project/jlproj)

# JLProj — Johnson–Lindenstrauss Projection Toolkit

**JLProj** is a Python toolkit for dimensionality reduction using the Johnson–Lindenstrauss (JL) lemma. It preserves pairwise distances between high-dimensional vectors with strong theoretical guarantees.

The toolkit provides:

- CLI for projection, search, and file inspection
- Python API for batch and single-vector projection
- FAISS-compatible search in compressed space
- Matrix serialization for reproducibility

---

## Capabilities

- JL Projection: Fast and distance-preserving linear projection
- Search: Find nearest vectors in compressed space (via FAISS)
- Serialization: Save/load projection matrices
- CLI: Use as a command-line tool for embedding pipelines
- Reconstruction: Approximate inverse projection supported (via saved matrix)

---

## Use Cases

- Reducing the size of vector databases in semantic search systems (RAG pipelines)
- Enabling fast similarity search under memory constraints
- Embedding compression for offline applications or edge inference
- Experimental comparison of PCA vs random projection

## Why Johnson–Lindenstrauss?

In many NLP and ML systems, embeddings such as BERT or SentenceTransformer outputs have high dimensionality (e.g., 384 or 768 dimensions). These embeddings are powerful, but storing and searching over millions of such vectors becomes computationally expensive.

The Johnson–Lindenstrauss Lemma (1984) provides a mathematical guarantee that such high-dimensional vectors can be projected into a significantly lower-dimensional space (e.g., 64 or 32 dimensions) without significantly distorting the distances between them.

This is crucial in applications like:
- approximate nearest neighbor search
- semantic retrieval (RAG pipelines)
- memory-constrained vector storage

### What the JL Lemma says

Given a small distortion level ε in (0, 1), the JL Lemma states:

    (1 - ε) * ||x - y||² ≤ ||f(x) - f(y)||² ≤ (1 + ε) * ||x - y||²

Where:
- x, y ∈ ℝᵈ are your original vectors
- f is a random linear projection (e.g., multiplying by a Gaussian matrix)
- f(x), f(y) ∈ ℝᵏ live in the lower-dimensional space

And the required dimension k scales as:

    k = O(log(n) / ε²)

This means you can project thousands of vectors into a space of dimension 32–128 and still maintain the pairwise geometry with high fidelity. Unlike PCA, this method offers explicit probabilistic guarantees on distance preservation.

## Limitations

- Does not preserve angular similarity (cosine) as well as PCA in some cases
- Inverse projection is approximate; exact recovery is not possible
- FAISS search operates on projected vectors, not original ones
- Requires a projection matrix to be saved for decompression

---

## 📈 Distance Preservation

The JL projection preserves pairwise distances with low distortion:

![Distance and error metrics](docs/img/distortion.png)


- **Mean relative error**: 6.94%  
- **Max error**: 33.57%

## 🧭 Embedding Visualization

Comparison of projected and original embeddings using PCA and UMAP:

![Embedding visualization](docs/img/pca_vs_jl.png)
)

## 🧭 Embedding Structure Comparison

To visually assess the geometric consistency of the JL projection, we compared 2D reductions of the original and projected vectors using PCA and UMAP.

![Embedding structure](docs/img/pca_umap_comparison.png)
)

The structure and distribution of clusters is largely preserved, confirming that semantic neighborhood relations are maintained under JL compression.

## 📊 **Benchmark: JL vs PCA vs UMAP**

This benchmark compares the distance preservation accuracy of Johnson–Lindenstrauss projection (JL), PCA, and UMAP on synthetic high-dimensional vectors.  
• Input vectors were sampled from a normal distribution (N(0, 1)  
• Projections were made from 128, 768, and 2048 dimensions to 32–384  
• For each method, we compute the mean relative error of pairwise distances  
• Lower error means better preservation of the original vector space  

**JL vs PCA and UMAP (mean relative error)**

| From → To     | JL Error | PCA Error | UMAP Error | JL vs PCA | JL vs UMAP |
|---------------|----------|-----------|------------|-----------|------------|
| 128 → 32      | 0.1010   | 0.3517    | 0.9008     | +248.1%   | +791.5%    |
| 128 → 64      | 0.0718   | 0.1606    | 0.9006     | +123.7%   | +1154.2%   |
| 768 → 32      | 0.0978   | 0.5826    | 0.9606     | +495.9%   | +882.6%    |
| 768 → 64      | 0.0715   | 0.4392    | 0.9607     | +514.4%   | +1244.0%   |
| 768 → 128     | 0.0500   | 0.2620    | 0.9607     | +423.7%   | +1820.4%   |
| 768 → 256     | 0.0363   | 0.0880    | 0.9607     | +142.4%   | +2547.0%   |
| 768 → 384     | 0.0296   | 0.0186    | 0.9607     | –37.1%    | +3151.0%   |
| 2048 → 32     | 0.0990   | 0.6481    | 0.9757     | +554.5%   | +885.4%    |
| 2048 → 64     | 0.0739   | 0.5219    | 0.9758     | +606.2%   | +1220.4%   |
| 2048 → 128    | 0.0502   | 0.3523    | 0.9758     | +601.4%   | +1842.7%   |
| 2048 → 256    | 0.0345   | 0.1581    | 0.9758     | +357.6%   | +2724.9%   |
| 2048 → 384    | 0.0292   | 0.0517    | 0.9757     | +77.2%    | +3240.9%   |

---

## Installation

```bash
pip install -e .
```

Install dependencies:

```bash
pip install numpy faiss-cpu sentence-transformers scikit-learn
```

---

## Usage

### In Python

```python
import numpy as np
from jlproj.projector import JLProjector

# Load high-dimensional vectors
X = np.load("embeddings.npy")  # shape: (n_samples, dim_in)

# Initialize projector and fit
projector = JLProjector(dim_out=64)
projector.fit(dim_in=X.shape[1])

# Project the full matrix
X_proj = projector.transform(X)
np.save("compressed.npy", X_proj)

# Save projection matrix
projector.save("projection_matrix.npz")

# Later: load the matrix and project a single query vector
projector2 = JLProjector()
projector2.load("projection_matrix.npz")

query = np.random.randn(X.shape[1])
query_proj = projector2.transform_query(query)
```

### From the Command Line (CLI)

All commands are accessible via:

```bash
python -m jlproj.cli <command> [args]
```

#### Compress embeddings

```bash
python -m jlproj.cli compress embeddings.npy --dim 64 --out compressed.npy --save-matrix
```

#### Search nearest neighbors

```bash
python -m jlproj.cli search --index compressed.npy --query query.npy --k 5
```

#### Inspect file shape

```bash
python -m jlproj.cli info compressed.npy
```

#### Decompress using saved projection matrix

```bash
python -m jlproj.cli decompress --input compressed.npy --matrix compressed_matrix.npz --out restored.npy
```

### API Overview

- `transform(X)` — project a full batch of vectors (e.g. 10,000 × 768 → 10,000 × 64)
- `transform_query(x)` — fast projection for a single input (e.g. real-time search)

---

## Tests

This project includes unit tests for the core projection functionality (`JLProjector`):

- shape validation (projected vectors have expected shape)
- distance preservation (relative error stays bounded)
- serialization / deserialization of projection matrix
- single-query transformation (for search scenarios)

Run tests with:

```bash
pytest
```

Tests are located in `tests/test_projector.py`.

Example output:

```
============================= test session starts ==============================
test_projector.py::test_projection_shape PASSED
test_projector.py::test_distance_preservation PASSED
test_projector.py::test_transform_query_shape PASSED
test_projector.py::test_save_and_load PASSED
============================== 4 passed in 0.61s ===============================
```

---

## Project Structure

```
jlproj/
├── projector.py         # JLProjector core class
├── cli.py               # Command-line interface (compress/search/info/decompress)
├── faiss_wrapper.py     # (optional for future)
├── __init__.py
```