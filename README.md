# Password Manager CLI

A secure command-line password manager with encryption, recycle bin, and modular package structure.

## Features
- Add, edit, delete, search passwords
- Recycle bin (restore deleted items)
- Strong random password generator
- Copy password to clipboard
- Encryption with `cryptography.fernet`
- Save/load data from JSON file
- Package structure (`core`, `utils`, `common`)

## How to Run
1. Clone the repo
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Linux/Mac)
4. Install dependencies: `pip install -r requirements.txt` 
5. Run: `python main_menu.py`

## Requirements
- Python 3.8+
- cryptography

## Future Improvements
- GUI version
- Cloud sync