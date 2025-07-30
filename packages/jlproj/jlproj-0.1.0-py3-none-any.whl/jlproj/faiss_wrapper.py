import faiss
import numpy as np
from jlproj.projector import JLProjector

class JLFaissIndex:
    def __init__(self, dim_in: int, dim_out: int = 64, seed: int = 42):
        self.projector = JLProjector(dim_out=dim_out, seed=seed)
        self.index = faiss.IndexFlatL2(dim_out)
        self.fitted = False

    def build(self, X: np.ndarray):
        """Fit the projector and build the FAISS index on projected vectors"""
        dim_in = X.shape[1]
        self.projector.fit(dim_in)
        X_proj = self.projector.transform(X)
        self.index.add(X_proj.astype(np.float32))
        self.fitted = True

    def search(self, query: np.ndarray, k: int = 5):
        """Search for k nearest neighbors of the projected query vector"""
        assert self.fitted, "Index is not built. Call build() first."
        if query.ndim == 1:
            query_proj = self.projector.transform_query(query.reshape(1, -1))
        else:
            query_proj = self.projector.transform(query)
        distances, indices = self.index.search(query_proj.astype(np.float32), k)
        return distances, indices