
from setuptools import setup, find_packages

setup(
    name="mseep-cryptopanic-mcp-server",
    version="0.1.0",
    description="Provide the latest cryptocurrency news for AI agents.",
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
    install_requires=['dotenv>=0.9.9', 'mcp[cli]>=1.3.0', 'requests>=2.32.3'],
    keywords=["mseep"] + [],
)
