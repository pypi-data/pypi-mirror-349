import numpy as np
import os

class JLProjector:
    def __init__(self, dim_out: int = 64, seed: int = 42):
        self.dim_out = dim_out
        self.seed = seed
        self.R = None  # random projection matrix

    def fit(self, dim_in: int):
        """Generates a random projection matrix R of shape (dim_in x dim_out)"""
        rng = np.random.default_rng(self.seed)
        scale = 1.0 / np.sqrt(self.dim_out)
        self.R = rng.normal(loc=0.0, scale=scale, size=(dim_in, self.dim_out))

    def transform(self, X: np.ndarray) -> np.ndarray:
        """Projects all vectors X (n_samples x dim_in) using the matrix R"""
        assert self.R is not None, "Projection matrix not initialized. Call fit() first."
        return np.dot(X, self.R)

    def transform_query(self, x: np.ndarray) -> np.ndarray:
        """Projects a single vector x (dim_in,) using the matrix R"""
        assert self.R is not None, "Projection matrix not initialized. Call fit() first."
        return np.dot(x, self.R)

    def save(self, path: str):
        """Saves the projection matrix R to a .npz file"""
        assert self.R is not None, "Nothing to save: projection matrix not initialized."
        np.savez(path, R=self.R, dim_out=self.dim_out, seed=self.seed)

    def load(self, path: str):
        """Loads the projection matrix R from a .npz file"""
        assert os.path.exists(path), f"File not found: {path}"
        data = np.load(path)
        self.R = data['R']
        self.dim_out = int(data['dim_out'])
        self.seed = int(data['seed'])