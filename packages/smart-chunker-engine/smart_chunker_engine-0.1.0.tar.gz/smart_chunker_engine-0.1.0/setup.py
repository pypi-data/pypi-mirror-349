from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="smart_chunker_engine",
    version="0.1.0",
    description="Modular semantic text chunking framework with rich metadata (ru/en)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Smart Chunker Team",
    url="https://github.com/maverikod/vvz-smart-chunker-engine",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "chunk_metadata_adapter>=1.3.0",
        "sentence-transformers>=2.2.2",
        "hdbscan>=0.8.29",
        "scikit-learn>=1.0.0",
        "spacy>=3.5.0"
    ],
    python_requires=">=3.10",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Text Processing :: Linguistic",
        "Framework :: Pytest",
    ],
    project_urls={
        "Documentation": "https://github.com/maverikod/vvz-smart-chunker-engine",
        "Source": "https://github.com/maverikod/vvz-smart-chunker-engine",
    },
) 