# filepath: /Users/lucky/chatcsvai/chatcsvai/core.py
# === chatcsvai/core.py ===
import pandas as pd
import duckdb
from langchain_core.tools import Tool
from sentence_transformers import SentenceTransformer
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_groq.chat_models import ChatGroq
from langchain.agents import initialize_agent, AgentType
from langchain_experimental.utilities import PythonREPL 
from langchain.memory import ConversationBufferMemory

def initialize_chat(csv_path: str, description: str, groq_api_key: str, model_name: str):
    df = pd.read_csv(csv_path)
    print(f"\U0001F4C4 Data Description: {description}\n")

    def query_df(query: str) -> str:
        try:
            normalized_query = query.replace(' LIKE ', ' ILIKE ')
            duckdb.register('df', df)
            result = duckdb.sql(normalized_query).df()
            duckdb.unregister('df')
            return result.to_string(index=False) if not result.empty else "No results found."
        except Exception as e:
            return f"Error: {e}"

    df_tool = Tool(
        name="DataFrame SQL Query",
        func=query_df,
        description="Use SQL to query the dataset. Table name is 'df'."
    )

    columns_tool = Tool(
        name="DataFrame Columns",
        func=lambda _: str(df.columns.tolist()),
        description="List all available columns in the dataset."
    )

    texts = [f"{row.to_string()}" for _, row in df.iterrows()]
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_store = FAISS.from_texts(texts, embeddings)

    llm = ChatGroq(model=model_name, api_key=groq_api_key)

    retrieval_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vector_store.as_retriever()
    )

    retrieval_tool = Tool(
        name="Semantic CSV Search",
        func=retrieval_chain.run,
        description="Ask about rows using natural language like 'best price in Mumbai', etc."
    )

    python_tool = Tool(
        name="Python Executor",
        func=PythonREPL().run,
        description="Use for calculations or data manipulations."
    )

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    agent = initialize_agent(
        tools=[df_tool, columns_tool, retrieval_tool, python_tool],
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        memory=memory,
        verbose=True
    )

    return agent

def cli_chat(agent):
    print("\U0001F916 CSV Chatbot is ready! Type your questions (or 'exit' to quit).")
    while True:
        q = input("You: ")
        if q.strip().lower() in ["exit", "quit"]:
            break
        try:
            response = agent.run(q)
            print("Bot:", response, "\n")
        except Exception as e:
            print("Bot: Error:", e, "\n")