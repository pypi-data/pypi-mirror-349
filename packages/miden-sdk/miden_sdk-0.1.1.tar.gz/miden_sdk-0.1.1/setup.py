from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="miden-sdk",
    version="0.1.1",
    author="Miden Python SDK Team",
    author_email="amon@chumba.shop",
    description="Python SDK for Miden blockchain",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chumbacash/miden-sdk",
    project_urls={
        "Bug Tracker": "https://github.com/chumbacash/miden-sdk/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
    ],
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "pydantic>=2.0.0",
        "wasmtime>=0.32.0",
        "grpcio>=1.32.0",
        "requests>=2.25.0",
        "blake3>=0.3.0",
    ],
    include_package_data=True,
    package_data={
        "miden_sdk": ["wasm/*"],
    },
) 