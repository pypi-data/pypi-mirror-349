from setuptools import setup, find_packages

setup(
    name="jlproj",
    version="0.1.0",
    author="Your Name",
    author_email="your@email.com",
    description="Johnson–Lindenstrauss Projection Toolkit for dimensionality reduction",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/jlproj",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "faiss-cpu",
        "scikit-learn",
        "sentence-transformers"
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    python_requires=">=3.8",
    include_package_data=True,
    zip_safe=False,
)