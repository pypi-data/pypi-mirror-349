from chatcsvai.core import initialize_chat, cli_chat
import argparse

def main():
    parser = argparse.ArgumentParser(description="Chat with your CSV using AI.")
    parser.add_argument("--csv", required=True, help="Path to the CSV file.")
    parser.add_argument("--desc", required=True, help="Description of your dataset.")
    parser.add_argument("--groq-api-key", required=True, help="Your Groq API key.")
    parser.add_argument("--model-name", default="meta-llama/llama-4-scout-17b-16e-instruct", help="Groq model name.")
    args = parser.parse_args()

    agent = initialize_chat(args.csv, args.desc, args.groq_api_key, args.model_name)
    cli_chat(agent)
