from pathlib import Path
from setuptools import setup, find_packages

ROOT = Path(__file__).parent
README = (ROOT / "README.md").read_text(encoding="utf-8")

setup(
    name="jlproj",
    version="0.1.6",                         # ↑ новый номер
    author="Anton Smirnov",
    author_email="AntonSmirnovM@protonmail.com",
    description="Johnson–Lindenstrauss Projection Toolkit for dimensionality reduction",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Quchluk/jlproj",
    project_urls={
        "PyPI": "https://pypi.org/project/jlproj/",
        "Source": "https://github.com/Quchluk/jlproj",
        "Documentation": "https://github.com/Quchluk/jlproj#readme",
    },

    license="MIT",
    license_files=[],

    packages=find_packages(include=["jlproj*", ]),  # всё как было
    include_package_data=True,

    install_requires=[
        "numpy",
        "faiss-cpu",
        "scikit-learn",
        "sentence-transformers",
    ],
    extras_require={
        "dev": ["pytest", "black", "ruff"],
    },

    entry_points={
        "console_scripts": [
            "jlproj = jlproj.cli:main",
        ],
    },

    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    zip_safe=False,
)