# app_modules/notes.py

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    jsonify,
    send_file
)
from flask_login import login_required, current_user

from .models import (
    create_note,
    update_note,
    delete_note,
    get_note_by_id,
    get_notes_by_user,
    search_notes,
    get_categories,
)
import io

notes_bp = Blueprint("notes",  __name__, template_folder="../template", url_prefix="/notes")


# -----------------------------------------------------------
# DASHBOARD (LIST ALL NOTES)
# -----------------------------------------------------------
@notes_bp.route("/dashboard")
@login_required
def dashboard():
    query = request.args.get("q", "").strip()

    if query:
        notes = search_notes(current_user.id, query)
    else:
        notes = get_notes_by_user(current_user.id)

    categories = get_categories(current_user.id)

    return render_template(
        "dashboard.html",
        notes=notes,
        categories=categories,
        query=query,
    )


# -----------------------------------------------------------
# CREATE NOTE
# -----------------------------------------------------------
@notes_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()
        category_id = request.form.get("category_id")
        pinned = request.form.get("pinned") == "on"
        reminder = request.form.get("reminder")  # ISO timestamp or empty

        if not title and not content:
            flash("A note cannot be empty.")
            return redirect(url_for("notes.create"))

        create_note(
            user_id=current_user.id,
            title=title,
            content=content,
            category_id=category_id if category_id else None,
            pinned=pinned,
            reminder=reminder if reminder else None,
        )

        return redirect(url_for("notes.dashboard"))

    categories = get_categories(current_user.id)
    return render_template("note_edit.html", categories=categories, mode="create")


# -----------------------------------------------------------
# EDIT NOTE
# -----------------------------------------------------------
@notes_bp.route("/edit/<int:note_id>", methods=["GET", "POST"])
@login_required
def edit(note_id):
    note = get_note_by_id(note_id, current_user.id)
    if not note:
        flash("Note not found.")
        return redirect(url_for("notes.dashboard"))

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()
        category_id = request.form.get("category_id")
        pinned = request.form.get("pinned") == "on"
        reminder = request.form.get("reminder")

        update_note(
            note_id=note_id,
            user_id=current_user.id,
            title=title,
            content=content,
            category_id=category_id if category_id else None,
            pinned=pinned,
            reminder=reminder if reminder else None,
        )
        return redirect(url_for("notes.dashboard"))

    categories = get_categories(current_user.id)

    return render_template(
        "note_edit.html",
        note=note,
        categories=categories,
        mode="edit",
    )


# -----------------------------------------------------------
# DELETE NOTE
# -----------------------------------------------------------
@notes_bp.route("/delete/<int:note_id>", methods=["POST"])
@login_required
def delete(note_id):
    note = get_note_by_id(note_id, current_user.id)
    if not note:
        flash("Note not found.")
        return redirect(url_for("notes.dashboard"))

    delete_note(note_id, current_user.id)
    return redirect(url_for("notes.dashboard"))


# -----------------------------------------------------------
# PIN / UNPIN NOTE
# -----------------------------------------------------------
@notes_bp.route("/pin/<int:note_id>", methods=["POST"])
@login_required
def pin(note_id):
    note = get_note_by_id(note_id, current_user.id)
    if not note:
        return jsonify({"status": "error", "msg": "Note not found"}), 404

    new_state = 0 if note["pinned"] else 1

    update_note(
        note_id,
        user_id=current_user.id,
        title=note["title"],
        content=note["content"],
        category_id=note["category_id"],
        pinned=new_state,
        reminder=note["reminder"],
    )

    return jsonify({"status": "success", "pinned": bool(new_state)})


# -----------------------------------------------------------
# SYNC ENDPOINT
# (Optional – used by /static/js/sync.js)
# -----------------------------------------------------------
@notes_bp.route("/sync", methods=["POST"])
@login_required
def sync():
    """
    Accepts a list of local notes (from JS localStorage) and merges them.
    Actual merging happens in sync.py (which you’ll add next).
    """
    from .sync import sync_local_to_cloud

    data = request.get_json()
    local_notes = data.get("notes", [])

    sync_local_to_cloud(current_user.id, local_notes)

    return jsonify({"status": "success"})



# ===============================================
# DOWNLOAD NOTE AS .TXT
# ===============================================
@notes_bp.get("/notes/download/<int:note_id>")
@login_required
def download_note(note_id):
    # Get note
    note = get_note_by_id(note_id, current_user.id)

    if not note:
        flash("Note not found")
        return redirect(url_for("notes.dashboard"))

    # Prepare content
    title = note["title"] or "Untitled"
    content = note["content"] or ""

    text_data = f"{title}\n\n{content}"

    return send_file(
        io.BytesIO(text_data.encode("utf-8")),
        mimetype="text/plain",
        as_attachment=True,
        download_name=f"{title}.txt"
    )