# app_modules/utils.py

import re
import html
import json
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


# -----------------------------------------------------------
# PASSWORD HELPERS
# -----------------------------------------------------------

def hash_password(password):
    """Generate a secure password hash."""
    return generate_password_hash(password)


def verify_password(stored_hash, password_input):
    """Check a password against a stored hash."""
    return check_password_hash(stored_hash, password_input)


# -----------------------------------------------------------
# TIMESTAMP HELPERS
# -----------------------------------------------------------

def now_iso():
    """Return the current timestamp in ISO format."""
    return datetime.utcnow().isoformat()


def to_iso(ts):
    """
    Convert various timestamp formats into ISO-8601.
    Accepts timestamps from JS, DB, or partial formats.
    """
    if not ts:
        return now_iso()

    try:
        # JavaScript timestamps often end with 'Z'
        ts = ts.replace("Z", "+00:00")
        return datetime.fromisoformat(ts).isoformat()
    except Exception:
        # Fallback: attempt to parse common datetime formats
        try:
            return datetime.strptime(ts, "%Y-%m-%d %H:%M:%S").isoformat()
        except Exception:
            return now_iso()


def format_timestamp(ts):
    """
    Convert ISO timestamps into a friendly display format:
    Example: '2025-01-14T12:22:03' → 'Jan 14, 2025 • 12:22 PM'
    """
    try:
        dt = datetime.fromisoformat(ts)
        return dt.strftime("%b %d, %Y • %I:%M %p")
    except Exception:
        return ts


# -----------------------------------------------------------
# STRING SANITIZATION
# -----------------------------------------------------------

def sanitize_text(text):
    """
    Remove potentially malicious HTML or scripts.
    Converts <, >, & into HTML-safe equivalents.
    """
    if not text:
        return ""

    text = html.escape(text, quote=True)
    return text.strip()


def slugify(text):
    """
    Convert text into a slug.
    Example: 'My New Category' → 'my-new-category'
    """
    if not text:
        return ""

    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    text = text.strip("-")
    return text


# -----------------------------------------------------------
# VALIDATION HELPERS
# -----------------------------------------------------------

def validate_required(*fields):
    """
    Ensure all fields are non-empty strings.
    Example:
        if not validate_required(username, password):
            return error
    """
    for field in fields:
        if not field or not isinstance(field, str) or not field.strip():
            return False
    return True


# -----------------------------------------------------------
# JSON UTILITIES
# -----------------------------------------------------------

def json_response(status="success", **kwargs):
    """
    Return a consistent JSON structure.
    Example:
        return json_response(message="Note created")
    """
    payload = {"status": status}
    payload.update(kwargs)
    return payload
