# Password Strength & Breach Checker

A cybersecurity tool for password strength analysis, breach detection, secure password generation, and security event monitoring.

## Features

- Entropy-based password strength analysis
- zxcvbn password scoring
- Have I Been Pwned (HIBP) password breach checking
- HIBP k-anonymity using SHA-1 hash prefixes
- Email breach lookup through HIBP API
- Secure password generator
- Memorable passphrase generator
- Watchdog real-time security log monitoring
- SQLite security event storage
- Streamlit web interface
- Rule documentation in PDF format

## Technology Stack

- Python 3
- Streamlit
- zxcvbn
- Requests
- Watchdog
- SQLite
- Have I Been Pwned API
- SHA-1
- ReportLab
- python-dotenv

## Project Structure

```text
ProStackHub_PasswordChecker/
├── app.py
├── password_utils.py
├── hibp.py
├── database.py
├── watcher.py
├── create_rule_pdf.py
├── requirements.txt
├── .env.example
├── .gitignore
├── Rule_Documentation.pdf
├── logs/
│   └── security.log
├── data/
├── rules/
│   └── detection_rules.md
└── screenshots/
