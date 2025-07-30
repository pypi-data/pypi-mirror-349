# JLProj — Johnson–Lindenstrauss Projection Toolkit

**JLProj** is a Python toolkit for dimensionality reduction using the Johnson–Lindenstrauss (JL) lemma. It preserves pairwise distances between high-dimensional vectors with strong theoretical guarantees. Includes CLI for compression, search, decompression, and inspection.

---

## Features

- JL Projection: Fast and distance-preserving linear projection
- Search: Find nearest vectors in compressed space (via FAISS)
- Serialization: Save/load projection matrices
- CLI: Use as a command-line tool for embedding pipelines
- Reconstruction: Approximate inverse projection supported (via saved matrix)

---

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

---

## Empirical Results

We applied JL projection to real sentence-transformer vectors (384D → 64D) and measured distortion:

- Mean relative error in Euclidean distance: ~7.4%
- Maximum error: < 20%

These values are far below the theoretical upper bound (30%), validating the JL approach for compression in real-world NLP pipelines.

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