
from setuptools import setup, find_packages

setup(
    name="mseep-blender-open-mcp",
    version="0.2.0",
    description="Blender integration with local AI models via MCP and Ollama",
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
    install_requires=['mcp[cli]>=1.3.0', 'httpx>=0.24.0', 'ollama>=0.4.7'],
    keywords=["mseep"] + [],
)
