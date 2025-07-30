from setuptools import setup, find_packages

setup(
    name="lazymodelsloader",
    version="0.1.0",
    description="Lazy transformer model loader with memory-based unloading (CPU/GPU)",
    author="Никита",
    packages=find_packages(),
    install_requires=[
        "transformers>=4.0.0",
        "torch",
        "psutil",
    ],
    python_requires=">=3.8",
)
