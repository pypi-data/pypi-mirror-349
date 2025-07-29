from setuptools import setup, find_packages

setup(
    name="chatcsvai",
    version="0.1.0",
    author="Your Name",
    author_email="luckykandpal091@gmail.com",
    description="A chatbot for interacting with CSV files using AI.",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "duckdb",
        "langchain-core",
        "sentence-transformers",
        "langchain",
        "langchain-huggingface",
        "langchain-community",
        "langchain-groq",
        "langchain-agents",
        "langchain-experimental",
        "langchain-memory",
        
    ],
    entry_points={
        "console_scripts": [
            "chatcsvai=main:main",
        ],
    },
)