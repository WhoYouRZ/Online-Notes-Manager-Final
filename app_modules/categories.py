from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required
from app_modules import get_db
from app_modules.models import create_category, get_categories

# All API endpoints live under `/category-api/*`
categories_bp = Blueprint("category_api", __name__, url_prefix="/category-api")


# ============================================================
# GET: all categories for logged-in user (JSON ONLY)
# ============================================================
@categories_bp.get("/list")
@login_required
def api_get_categories():
    rows = get_categories(current_user.id)
    return jsonify([dict(row) for row in rows])


# ============================================================
# POST: create new category for logged-in user
# ============================================================
@categories_bp.post("/create")
@login_required
def api_create_category():
    data = request.json
    name = data.get("name", "").strip()

    if not name:
        return jsonify({"error": "Name required"}), 400

    create_category(current_user.id, name)
    return jsonify({"status": "success"})


# ============================================================
# PUT: rename a category
# ============================================================
@categories_bp.put("/rename/<int:cat_id>")
@login_required
def api_rename_category(cat_id):
    data = request.json
    new_name = data.get("name", "").strip()

    if not new_name:
        return jsonify({"error": "Name required"}), 400

    db = get_db()

    # Update ONLY the user's own category
    db.execute(
        "UPDATE categories SET name = ? WHERE id = ? AND user_id = ?",
        (new_name, cat_id, current_user.id),
    )
    db.commit()

    return jsonify({"status": "success"})


# ============================================================
# DELETE: delete a category
# ============================================================
@categories_bp.delete("/delete/<int:cat_id>")
@login_required
def api_delete_category(cat_id):
    db = get_db()
    db.execute(
        "DELETE FROM categories WHERE id = ? AND user_id = ?",
        (cat_id, current_user.id),
    )
    db.commit()

    return jsonify({"status": "success"})
