
from setuptools import setup, find_packages

setup(
    name="mseep-k8s-mcp-server",
    version="1.3.0",
    description="MCP Server for Kubernetes CLI tools (kubectl, istioctl, helm, argocd)",
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
    install_requires=['mcp', 'pydantic>=2.0.0', 'psutil>=5.9.0', 'pyyaml>=6.0.0'],
    keywords=["mseep"] + [],
)
