from setuptools import setup, find_packages

setup(
    name="chatcsvai",
    version="0.2.0",
    description="A chatbot for interacting with CSV files using AI.",
    author="Lucky Kandpal",
    author_email="luckykandpal091@gmail.com",
    packages=find_packages(),
    install_requires=[
        "pandas>=1.3.0,<3.0.0",
        "duckdb>=0.3.2",
        "sentence-transformers>=2.2.0,<5.0.0",
        "langchain>=0.1.0,<0.4.0",
        "langchain-core>=0.0.1,<0.4.0",
        "langchain-community>=0.0.1,<0.4.0",
        "langchain-huggingface>=0.0.1,<0.3.0",
        "langchain-groq>=0.0.1,<0.4.0",
        "langchain-experimental>=0.0.1,<0.4.0",
        "python-dotenv>=1.0.0"
    ],
    entry_points={
        "console_scripts": [
            "chatcsvai = chatcsvai.cli:main"
        ]
    },
    python_requires=">=3.8"
)
