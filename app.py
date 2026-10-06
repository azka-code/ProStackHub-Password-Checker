import streamlit as st
from datetime import datetime

from password_utils import (
    analyze_password,
    generate_password,
    generate_passphrase
)

from hibp import (
    check_password_breach,
    check_email_breach
)

from database import (
    init_database,
    save_event,
    get_events
)


st.set_page_config(
    page_title="Password Strength & Breach Checker",
    page_icon="🔐",
    layout="wide"
)

init_database()

st.title("🔐 Password Strength & Breach Checker")

st.caption(
    "Entropy-based password analysis • HIBP breach checking • "
    "Secure password generation"
)


tab1, tab2, tab3 = st.tabs([
    "🔍 Password Checker",
    "📧 Email Breach Check",
    "🔑 Password Generator"
])


# ---------------- PASSWORD CHECKER ----------------

with tab1:

    st.subheader("Password Security Analysis")

    password = st.text_input(
        "Enter password",
        type="password"
    )

    if password:

        result = analyze_password(password)

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Strength",
            result["label"]
        )

        col2.metric(
            "Score",
            f'{result["score"]}/4'
        )

        col3.metric(
            "Entropy",
            f'{result["entropy"]:.1f} bits'
        )

        col4.metric(
            "Length",
            result["length"]
        )

        st.progress(
            (result["score"] + 1) / 5
        )

        st.subheader("Password Improvement Suggestions")

        for suggestion in result["suggestions"]:
            st.write("•", suggestion)

        st.divider()

        st.subheader(
            "Have I Been Pwned Password Breach Check"
        )

        if st.button(
            "Check Password Breach",
            type="primary"
        ):

            with st.spinner(
                "Checking HIBP securely..."
            ):

                breach = check_password_breach(
                    password
                )

            if breach["error"]:

                st.error(
                    breach["error"]
                )

            elif breach["breached"]:

                st.error(
                    f'⚠️ Password found in breach data '
                    f'{breach["count"]:,} times.'
                )

                st.warning(
                    "Do not use this password. "
                    "Choose a unique replacement."
                )

                save_event(
                    "Password Breach",
                    "HIGH",
                    f"Password matched HIBP dataset {breach['count']} times."
                )

            else:

                st.success(
                    "✅ Password was not found "
                    "in the HIBP Pwned Passwords dataset."
                )

                save_event(
                    "Password Check",
                    "LOW",
                    "Password was not found in HIBP dataset."
                )

            st.info(
                "Privacy: the full password is never sent "
                "to HIBP. Only the first five characters "
                "of its SHA-1 hash are sent."
            )


# ---------------- EMAIL CHECK ----------------

with tab2:

    st.subheader(
        "Email Breach Check"
    )

    email = st.text_input(
        "Email address",
        placeholder="example@email.com"
    )

    st.warning(
        "Email breach lookup requires an HIBP API key. "
        "Do not enter a private email for a demonstration."
    )

    if st.button("Check Email Breaches"):

        if "@" not in email:

            st.error(
                "Enter a valid email address."
            )

        else:

            result = check_email_breach(
                email
            )

            if result["error"]:

                st.error(
                    result["error"]
                )

            elif result["breached"]:

                st.error(
                    f'⚠️ {len(result["breaches"])} '
                    'breach record(s) found.'
                )

                for breach in result["breaches"][:10]:

                    st.write(
                        "•",
                        breach.get(
                            "Name",
                            "Unknown"
                        )
                    )

                save_event(
                    "Email Breach",
                    "HIGH",
                    f"Breach records found for {email}."
                )

            else:

                st.success(
                    "✅ No breach records returned."
                )


# ---------------- GENERATOR ----------------

with tab3:

    st.subheader(
        "Secure Password Generator"
    )

    length = st.slider(
        "Password length",
        8,
        64,
        16
    )

    uppercase = st.checkbox(
        "Uppercase",
        True
    )

    lowercase = st.checkbox(
        "Lowercase",
        True
    )

    numbers = st.checkbox(
        "Numbers",
        True
    )

    symbols = st.checkbox(
        "Symbols",
        True
    )

    if st.button(
        "Generate Secure Password",
        type="primary"
    ):

        try:

            generated = generate_password(
                length,
                uppercase,
                lowercase,
                numbers,
                symbols
            )

            st.code(
                generated
            )

        except ValueError as error:

            st.error(
                str(error)
            )

    st.divider()

    st.subheader(
        "Memorable Passphrase"
    )

    word_count = st.slider(
        "Number of words",
        3,
        8,
        5
    )

    if st.button(
        "Generate Passphrase"
    ):

        phrase = generate_passphrase(
            word_count
        )

        st.code(
            phrase
        )


# ---------------- HISTORY ----------------

st.divider()

st.subheader(
    "📊 Security Event History"
)

events = get_events()

if events:

    for event in events[:20]:

        timestamp, event_type, severity, message = event

        with st.expander(
            f"{severity} — {event_type} — {timestamp}"
        ):

            st.write(message)

else:

    st.info(
        "No security events recorded yet."
    )


st.caption(
    "Educational cybersecurity project — "
    "Password data is not stored by this application."
)
