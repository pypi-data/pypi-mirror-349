import argparse
import numpy as np
from jlproj.projector import JLProjector
import faiss
import os

def compress(args):
    print(f"Loading embeddings from {args.input}...")
    X = np.load(args.input)
    print(f"Shape: {X.shape}")

    projector = JLProjector(dim_out=args.dim)
    projector.fit(dim_in=X.shape[1])
    X_proj = projector.transform(X)

    if args.save_matrix:
        matrix_path = os.path.splitext(args.output)[0] + "_matrix.npz"
        projector.save(matrix_path)
        print(f"Projection matrix saved to {matrix_path}")

    np.save(args.output, X_proj)
    print(f"Projected embeddings saved to {args.output}")

def search(args):
    print(f"Loading index from {args.index}...")
    X = np.load(args.index)
    print(f"Index shape: {X.shape}")

    print(f"Loading query from {args.query}...")
    q = np.load(args.query)
    if q.ndim == 1:
        q = q.reshape(1, -1)

    index = faiss.IndexFlatL2(X.shape[1])
    index.add(X)
    D, I = index.search(q, args.k)

    print("Top-k nearest neighbors:")
    for i in range(args.k):
        print(f"Rank {i+1}: index={I[0][i]}, distance={D[0][i]:.4f}")

def info(args):
    print(f"Reading: {args.path}")
    X = np.load(args.path)
    print(f"Shape: {X.shape}")
    print(f"Dtype: {X.dtype}")

def decompress(args):
    print(f"Loading projection matrix from {args.matrix}...")
    data = np.load(args.matrix)
    R = data["R"]

    print(f"Loading projected vectors from {args.input}...")
    X_proj = np.load(args.input)
    print(f"Projected shape: {X_proj.shape}, Matrix shape: {R.shape}")

    X_restored = np.dot(X_proj, R.T)
    np.save(args.output, X_restored)
    print(f"Restored embeddings saved to {args.output}")

def main():
    parser = argparse.ArgumentParser(description="JL Projection CLI")
    subparsers = parser.add_subparsers(dest="command")

    # compress
    compress_parser = subparsers.add_parser("compress", help="Compress embeddings using JL projection")
    compress_parser.add_argument("input", type=str, help="Path to input .npy file")
    compress_parser.add_argument("--dim", type=int, default=64, help="Output dimension")
    compress_parser.add_argument("--out", dest="output", type=str, required=True, help="Path to save projected embeddings")
    compress_parser.add_argument("--save-matrix", action="store_true", help="Whether to save the projection matrix")
    compress_parser.set_defaults(func=compress)

    # search
    search_parser = subparsers.add_parser("search", help="Search top-k neighbors using FAISS")
    search_parser.add_argument("--index", type=str, required=True, help="Path to compressed .npy file")
    search_parser.add_argument("--query", type=str, required=True, help="Path to .npy file with 1 query vector")
    search_parser.add_argument("--k", type=int, default=5, help="Top-k neighbors to retrieve")
    search_parser.set_defaults(func=search)

    # info
    info_parser = subparsers.add_parser("info", help="Print shape and dtype of a .npy file")
    info_parser.add_argument("path", type=str, help="Path to .npy file")
    info_parser.set_defaults(func=info)

    # decompress
    decompress_parser = subparsers.add_parser("decompress", help="Reconstruct vectors using saved projection matrix")
    decompress_parser.add_argument("--input", type=str, required=True, help="Path to projected .npy file")
    decompress_parser.add_argument("--matrix", type=str, required=True, help="Path to saved .npz matrix file")
    decompress_parser.add_argument("--out", dest="output", type=str, required=True, help="Path to save restored vectors")
    decompress_parser.set_defaults(func=decompress)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()