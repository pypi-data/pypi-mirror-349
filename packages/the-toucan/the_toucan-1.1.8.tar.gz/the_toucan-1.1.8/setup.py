from setuptools import setup, find_packages

setup(
    name="the-toucan",  
    version="1.1.8",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "torch",
        "torchvision",
        "albumentations",
        "Pillow"
    ],
    python_requires=">=3.9",
)