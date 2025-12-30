# app_modules/sync.py

from datetime import datetime
from .models import insert_synced_note


def normalize_timestamp(ts):
    """
    Normalize timestamps coming from JavaScript.
    JS usually sends ISO format. Example:
    '2025-01-14T06:20:51.123Z'
    """
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00")).isoformat()
    except Exception:
        return datetime.utcnow().isoformat()


def validate_local_note(note):
    """
    Ensure localStorage note contains required fields.
    Missing or malformed notes are ignored.
    """
    required = ("title", "content", "created_at")

    for field in required:
        if field not in note:
            return False
        if not isinstance(note[field], (str, int, float)):
            return False

    return True


def sync_local_to_cloud(user_id, local_notes):
    """
    Sync notes from the browser's localStorage into SQLite DB.

    Steps:
      1. Validate each note object.
      2. Normalize timestamps.
      3. Insert into DB unless duplicate.
      4. (Optional) Extend logic for merging content if needed.
    """
    if not local_notes or not isinstance(local_notes, list):
        return

    for note in local_notes:
        if not validate_local_note(note):
            continue  # Skip malformed notes

        title = note.get("title", "").strip()
        content = note.get("content", "").strip()

        # Skip empty notes
        if not title and not content:
            continue

        created_at = note.get("created_at")
        created_at = normalize_timestamp(created_at)

        # Categories are local-only for guests → ignore on sync
        insert_synced_note(
            user_id=user_id,
            title=title,
            content=content,
            category=None,
            created_at=created_at,
        )
