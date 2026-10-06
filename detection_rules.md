# Password Strength & Breach Checker — Rule Documentation

## 1. Password Strength Analysis

The application evaluates password security using zxcvbn scoring and entropy-based analysis.

Score:
- 0 — Very Weak
- 1 — Weak
- 2 — Fair
- 3 — Strong
- 4 — Very Strong

## 2. Entropy Analysis

The application estimates password entropy using password length and the character set used.

Higher entropy generally indicates a larger search space for password guessing.

## 3. HIBP Password Breach Check

The password is hashed locally using SHA-1.

Only the first five characters of the SHA-1 hash are sent to the HIBP Pwned Passwords range API.

The returned hash suffixes are compared locally.

The plaintext password is never transmitted.

## 4. Email Breach Check

The application supports the HIBP v3 breached-account API.

This feature requires an HIBP API key.

## 5. Secure Password Generator

The generator uses Python's secrets module and supports:

- Configurable length
- Uppercase letters
- Lowercase letters
- Numbers
- Symbols

A memorable passphrase generator is also included.

## 6. SQLite Event Storage

Security-related breach-check events are stored in SQLite with:

- Timestamp
- Event type
- Severity
- Message

## 7. Watchdog Monitoring

Watchdog monitors the security log and processes newly added entries.

## 8. Privacy

Passwords are not stored in the database.

For HIBP password checking, only five SHA-1 hash characters leave the local system.

## 9. Limitations

- HIBP availability is required for live breach checking.
- Email breach lookup requires HIBP API access.
- Password strength scores are estimates.
- This is an educational cybersecurity prototype.
