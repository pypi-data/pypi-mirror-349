
from setuptools import setup, find_packages

setup(
    name="mseep-modal-server",
    version="0.1.0",
    description="",
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
    install_requires=['httpx>=0.28.1', 'mcp>=1.1.1', 'python-dotenv>=1.0.1', 'modal>=0.67'],
    keywords=["mseep"] + [],
)
