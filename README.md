# PrivInvestigator

PrivInvestigator is a Python script that allows you to search two databases, Dehashed and Snusbase, for leaked information using their APIs.

## Requirements

- Python 3
- `requests` module

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/PrivInvestigator.git
cd PrivInvestigator

Create a virtual environment:
python3 -m venv venv

Activate the virtual environment:
On Unix or MacOS:

source venv/bin/activate

On Windows:

.\venv\Scripts\activate

Install the requests module:
pip install requests

Usage
Make sure you’re in the virtual environment where requests is installed. If not, activate it:
On Unix or MacOS:

source venv/bin/activate

On Windows:

.\venv\Scripts\activate

Run the script:
python PrivInvestigator.py

You will be prompted to enter your email, Dehashed API key, Snusbase API key, and the query you want to search. The script will then search both databases and print the results in a readable format in the terminal.

Troubleshooting
If you encounter the error ModuleNotFoundError: No module named 'requests', it means Python can’t find the requests module. This is likely because you’re trying to run the script outside of the virtual environment where requests is installed. Make sure to activate the virtual environment in each terminal session where you want to use it.

Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

