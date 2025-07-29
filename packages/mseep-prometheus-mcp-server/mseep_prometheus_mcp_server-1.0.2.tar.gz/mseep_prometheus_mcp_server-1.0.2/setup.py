
from setuptools import setup, find_packages

setup(
    name="mseep-prometheus_mcp_server",
    version="1.0.0",
    description="MCP server for Prometheus integration",
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
    install_requires=['mcp[cli]', 'prometheus-api-client', 'python-dotenv', 'pyproject-toml>=0.1.0', 'requests'],
    keywords=["mseep"] + [],
)
