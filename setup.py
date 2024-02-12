from setuptools import setup, find_packages

setup(
    name="ailetic",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "flask",
        "flask-cors",
        "numpy",
        "Pillow",
        "pydub",
        "torch",
        "torchvision",
        "urllib3==1.26.6"
    ]
)