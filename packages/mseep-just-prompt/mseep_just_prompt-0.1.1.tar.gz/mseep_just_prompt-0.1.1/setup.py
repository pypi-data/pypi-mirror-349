
from setuptools import setup, find_packages

setup(
    name="mseep-just-prompt",
    version="0.1.0",
    description="A lightweight MCP server for various LLM providers",
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
    install_requires=['anthropic>=0.49.0', 'google-genai>=1.11.0', 'groq>=0.20.0', 'ollama>=0.4.7', 'openai>=1.68.0', 'python-dotenv>=1.0.1', 'pydantic>=2.0.0', 'mcp>=0.1.5'],
    keywords=["mseep"] + [],
)
