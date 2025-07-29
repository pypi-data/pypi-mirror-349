from setuptools import setup, find_packages

setup(
    name="chatcsvai",
    version="0.1.4",
    author="Lucky Kandpal",
    author_email="luckykandpal091@gmail.com",
    description="A chatbot for interacting with CSV files using AI.",
    packages=find_packages(),
    install_requires=[
        "pandas>=1.3.0,<3.0.0",
        "duckdb>=0.3.2",
        "langchain-core>=0.0.1,<0.4.0",
        "sentence-transformers>=2.2.0,<5.0.0",
        "langchain>=0.0.1,<0.4.0",
        "langchain-huggingface>=0.0.1,<0.3.0",
        "langchain-community>=0.0.1,<0.4.0",
        "langchain-groq>=0.0.1,<0.4.0",
        "langchain-experimental>=0.0.1,<0.4.0",
        "langchain-memory>=0.0.1,<0.4.0",
    ],
    entry_points={
        "console_scripts": [
            "chatcsvai=main:main",
        ],
    },
)