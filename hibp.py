import hashlib
import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

PASSWORD_API = "https://api.pwnedpasswords.com/range/"
EMAIL_API = "https://haveibeenpwned.com/api/v3/breachedaccount/"

HIBP_API_KEY = os.getenv("HIBP_API_KEY")

if not HIBP_API_KEY:
    try:
        HIBP_API_KEY = st.secrets["HIBP_API_KEY"]
    except Exception:
        HIBP_API_KEY = None

USER_AGENT = "ProStackHub-Password-Checker/1.0"


def check_password_breach(password):

    sha1_hash = hashlib.sha1(
        password.encode("utf-8")
    ).hexdigest().upper()

    prefix = sha1_hash[:5]
    suffix = sha1_hash[5:]

    try:
        response = requests.get(
            PASSWORD_API + prefix,
            headers={
                "User-Agent": USER_AGENT,
                "Add-Padding": "true"
            },
            timeout=10
        )

        response.raise_for_status()

        for line in response.text.splitlines():

            parts = line.split(":")

            if len(parts) != 2:
                continue

            returned_suffix = parts[0].strip().upper()
            count = int(parts[1].strip())

            if returned_suffix == suffix:
                return {
                    "breached": True,
                    "count": count,
                    "error": None
                }

        return {
            "breached": False,
            "count": 0,
            "error": None
        }

    except Exception as error:

        return {
            "breached": False,
            "count": 0,
            "error": str(error)
        }


def check_email_breach(email):

    if not HIBP_API_KEY:

        return {
            "breached": False,
            "breaches": [],
            "error": "HIBP_API_KEY is not configured."
        }

    try:

        url = EMAIL_API + requests.utils.quote(
            email,
            safe=""
        )

        response = requests.get(
            url,
            headers={
                "hibp-api-key": HIBP_API_KEY,
                "user-agent": USER_AGENT
            },
            params={
                "truncateResponse": "false"
            },
            timeout=15
        )

        if response.status_code == 404:

            return {
                "breached": False,
                "breaches": [],
                "error": None
            }

        if response.status_code == 401:

            return {
                "breached": False,
                "breaches": [],
                "error": "Invalid HIBP API key."
            }

        response.raise_for_status()

        data = response.json()

        return {
            "breached": True,
            "breaches": data,
            "error": None
        }

    except Exception as error:

        return {
            "breached": False,
            "breaches": [],
            "error": str(error)
        }
