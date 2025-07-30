from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="lazymodels",
    version="0.1.3",
    description="Smart lazy loader for Transformers with memory-based unloading (CPU/GPU aware)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Nikita",
    packages=find_packages(),
    install_requires=[
        "transformers",
        "torch",
        "psutil",
    ],
    python_requires=">=3.8",
)