# ChatCSV AI

ChatCSV AI is a Python application that allows users to interact with CSV files using natural language queries. It leverages AI models to provide insights and perform operations on the data contained within CSV files.

## Features

- Query CSV data using SQL-like syntax.
- Retrieve data semantically using natural language.
- Execute Python code for calculations and data manipulations.
- Interactive command-line interface for user-friendly interactions.

## Installation

To install the project, clone the repository and navigate to the project directory. Then, run the following command:

```bash
pip install -e .
```

## Usage

To start the application, use the following command:

```bash
python main.py --csv <path_to_csv_file> --desc "<description_of_data>" --groq-api-key <your_groq_api_key> --model-name <model_name>
```

### Command-Line Arguments

- `--csv`: Path to the CSV file (required).
- `--desc`: Description of your data (required).
- `--groq-api-key`: Your GROQ API Key (required).
- `--model-name`: (Optional) Specify the GROQ model name. Defaults to `meta-llama/llama-4-scout-17b-16e-instruct`.

## Example

```bash
python main.py --csv data.csv --desc "Sales data for 2023" --groq-api-key your_api_key --model-name your_model_name
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.