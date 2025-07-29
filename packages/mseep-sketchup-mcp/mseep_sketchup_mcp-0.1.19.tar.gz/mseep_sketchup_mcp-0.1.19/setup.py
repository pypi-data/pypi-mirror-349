
from setuptools import setup, find_packages

setup(
    name="mseep-sketchup-mcp",
    version="0.1.17",
    description="Sketchup integration through Model Context Protocol",
    author="mseep",
    author_email="support@skydeck.ai",
    url="",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=['mcp[cli]>=1.3.0'],
    keywords=["mseep"] + [],
)
