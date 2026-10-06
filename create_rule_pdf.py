from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

OUTPUT = "Rule_Documentation.pdf"

doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=A4,
    rightMargin=45,
    leftMargin=45,
    topMargin=45,
    bottomMargin=45
)

styles = getSampleStyleSheet()

story = []

story.append(
    Paragraph(
        "Password Strength & Breach Checker",
        styles["Title"]
    )
)

story.append(
    Paragraph(
        "Rule Documentation",
        styles["Heading1"]
    )
)

sections = [
    (
        "1. Password Strength Analysis",
        "The system evaluates password strength using zxcvbn scoring and entropy-based analysis."
    ),
    (
        "2. Entropy Analysis",
        "Entropy is estimated from password length and character-set size."
    ),
    (
        "3. HIBP Password Breach Check",
        "The password is hashed locally using SHA-1. Only the first five hash characters are sent to the HIBP Pwned Passwords range API. Returned suffixes are compared locally."
    ),
    (
        "4. Email Breach Check",
        "The application supports the HIBP v3 breached-account API when a valid API key is configured."
    ),
    (
        "5. Secure Password Generator",
        "Python's secrets module is used to generate configurable random passwords and memorable passphrases."
    ),
    (
        "6. SQLite Storage",
        "Security events are stored with timestamp, event type, severity and message."
    ),
    (
        "7. Watchdog",
        "Watchdog monitors the security log for new or modified entries."
    ),
    (
        "8. Privacy",
        "Plaintext passwords are never stored. For password breach checks, only five SHA-1 hash characters are transmitted to HIBP."
    ),
    (
        "9. Limitations",
        "This is an educational cybersecurity prototype. Live breach checks depend on HIBP availability and email checks require appropriate API access."
    )
]

for heading, body in sections:

    story.append(
        Paragraph(
            heading,
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            body,
            styles["BodyText"]
        )
    )

    story.append(
        Spacer(1, 12)
    )

doc.build(story)

print("Rule_Documentation.pdf created successfully.")
