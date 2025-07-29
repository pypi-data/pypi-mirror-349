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
    print(f"📄 Data Description: {description}\n")

    def query_df(query: str) -> str:
        try:
            normalized_query = query.replace(' LIKE ', ' ILIKE ')
            duckdb.register('df', df)
            result = duckdb.sql(normalized_query).df()
            duckdb.unregister('df')
            return result.to_string(index=False) if not result.empty else "No results found."
        except Exception as e:
            return f"Error: {e}"

    tools = [
        Tool("SQL Query", query_df, "Run SQL queries against the CSV."),
        Tool("Show Columns", lambda _: str(df.columns.tolist()), "List available columns."),
        Tool(
            "Semantic Search",
            RetrievalQA.from_chain_type(
                llm=ChatGroq(model=model_name, api_key=groq_api_key),
                retriever=FAISS.from_texts(
                    [row.to_string() for _, row in df.iterrows()],
                    HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
                ).as_retriever()
            ).run,
            "Ask natural language questions about the CSV data."
        ),
        Tool("Python Executor", PythonREPL().run, "Execute Python code.")
    ]

    return initialize_agent(
        tools=tools,
        llm=ChatGroq(model=model_name, api_key=groq_api_key),
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        memory=ConversationBufferMemory(memory_key="chat_history", return_messages=True),
        verbose=True
    )

def cli_chat(agent):
    print("🤖 Chatbot ready. Ask questions (type 'exit' to quit).")
    while True:
        user_input = input("You: ")
        if user_input.lower().strip() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break
        try:
            response = agent.run(user_input)
            print("Bot:", response, "\n")
        except Exception as e:
            print("Error:", e)
