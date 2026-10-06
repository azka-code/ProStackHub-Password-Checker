import math
import secrets
import string
from zxcvbn import zxcvbn


def entropy(password):
    if not password:
        return 0.0

    charset = 0

    if any(c.islower() for c in password):
        charset += 26

    if any(c.isupper() for c in password):
        charset += 26

    if any(c.isdigit() for c in password):
        charset += 10

    if any(c in string.punctuation for c in password):
        charset += len(string.punctuation)

    if charset == 0:
        return 0.0

    return len(password) * math.log2(charset)


def analyze_password(password):
    result = zxcvbn(password)

    labels = [
        "Very Weak",
        "Weak",
        "Fair",
        "Strong",
        "Very Strong"
    ]

    suggestions = list(result["feedback"]["suggestions"])

    if len(password) < 12:
        suggestions.append("Use at least 12 characters.")

    if len(password) < 16:
        suggestions.append("A longer password or passphrase is recommended.")

    if not suggestions:
        suggestions.append("Good password characteristics detected.")

    return {
        "score": result["score"],
        "label": labels[result["score"]],
        "entropy": entropy(password),
        "length": len(password),
        "suggestions": list(dict.fromkeys(suggestions))
    }


def generate_password(length, uppercase, lowercase, numbers, symbols):
    groups = []

    if uppercase:
        groups.append(string.ascii_uppercase)

    if lowercase:
        groups.append(string.ascii_lowercase)

    if numbers:
        groups.append(string.digits)

    if symbols:
        groups.append(string.punctuation)

    if not groups:
        raise ValueError("Select at least one character type.")

    if length < len(groups):
        raise ValueError("Password length is too short.")

    password = [secrets.choice(group) for group in groups]

    pool = "".join(groups)

    for _ in range(length - len(password)):
        password.append(secrets.choice(pool))

    secrets.SystemRandom().shuffle(password)

    return "".join(password)


def generate_passphrase(words=5):
    wordlist = [
        "amber", "anchor", "apple", "arrow",
        "atlas", "breeze", "cactus", "candle",
        "cedar", "cloud", "comet", "coral",
        "crystal", "dawn", "delta", "eagle",
        "ember", "falcon", "forest", "galaxy",
        "garden", "harbor", "hazel", "island",
        "jungle", "lantern", "lemon", "maple",
        "meadow", "meteor", "moon", "ocean",
        "olive", "orbit", "pebble", "phoenix",
        "planet", "river", "rocket", "silver",
        "solar", "sparrow", "stone", "sunset",
        "thunder", "tiger", "violet", "willow"
    ]

    return "-".join(
        secrets.choice(wordlist)
        for _ in range(words)
    )
