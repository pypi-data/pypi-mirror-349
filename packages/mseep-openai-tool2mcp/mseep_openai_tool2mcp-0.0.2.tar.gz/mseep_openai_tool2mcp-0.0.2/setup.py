
from setuptools import setup, find_packages

setup(
    name="mseep-openai-tool2mcp",
    version="0.0.1",
    description="A MCP wrapper server for OpenAI built-in tools. You can use openai search and computer use on Claude APP!",
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
    install_requires=['fastapi>=0.100.0', 'uvicorn>=0.23.0', 'pydantic>=2.0.0', 'openai>=1.0.0', 'python-dotenv>=1.0.0', 'requests>=2.0.0', 'mcp[cli]>=1.4.0', 'httpx>=0.28.1'],
    keywords=["mseep"] + ['python'],
)
