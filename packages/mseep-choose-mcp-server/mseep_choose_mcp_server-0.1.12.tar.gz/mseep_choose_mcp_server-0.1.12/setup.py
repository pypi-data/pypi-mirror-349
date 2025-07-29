
from setuptools import setup, find_packages

setup(
    name="mseep-choose-mcp-server",
    version="0.1.10",
    description="Add your description here",
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
    install_requires=['google-cloud-bigquery>=3.29.0', 'mcp[cli]>=1.3.0'],
    keywords=["mseep"] + [],
)
