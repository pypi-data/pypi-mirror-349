
from setuptools import setup, find_packages

setup(
    name="mseep-mcp-rosetta",
    version="0.1.0",
    description="A simple CLI chatbot using the Model Context Protocol (MCP)",
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
    install_requires=['python-dotenv>=1.0.0', 'requests>=2.31.0', 'mcp[cli]>=1.0.0', 'uvicorn>=0.32.1', 'httpx>=0.28.1'],
    keywords=["mseep"] + ['mcp', 'llm', 'chatbot', 'cli'],
)
