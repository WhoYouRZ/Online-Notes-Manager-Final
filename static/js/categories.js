// ======================================================
// CATEGORY MANAGEMENT PAGE (AJAX)
// ======================================================

// Load categories for management page
async function loadCategories() {
    try {
        const res = await fetch("/category-api/list");
        const categories = await res.json();

        const list = document.getElementById("category-list");
        list.innerHTML = "";

        if (categories.length === 0) {
            list.innerHTML = `<p class="no-notes">No categories found.</p>`;
            return;
        }

        categories.forEach(cat => {
            const div = document.createElement("div");
            div.className = "category-item";

            div.innerHTML = `
                <span>${cat.name}</span>

                <div class="cat-actions">
                    <button class="btn-small rename-btn" 
                            data-id="${cat.id}" 
                            data-name="${cat.name}">
                        Rename
                    </button>

                    <button class="btn-small-danger delete-btn" 
                            data-id="${cat.id}">
                        Delete
                    </button>
                </div>
            `;

            list.appendChild(div);
        });

        attachCategoryEvents();

    } catch (err) {
        console.error("Failed to load categories:", err);
    }
}

// Create category
async function addCategory(name) {
    await fetch("/category-api/create", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ name })
    });

    loadCategories();
}

// Delete category
async function deleteCategory(id) {
    await fetch(`/category-api/delete/${id}`, {
        method: "DELETE"
    });

    loadCategories();
}

// Rename category
async function renameCategory(id, newName) {
    await fetch(`/category-api/rename/${id}`, {
        method: "PUT",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ name: newName })
    });

    loadCategories();
}

// Attach rename + delete events
function attachCategoryEvents() {
    document.querySelectorAll(".rename-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            openRenameModal(btn.dataset.id, btn.dataset.name);
        });
    });

    document.querySelectorAll(".delete-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            if (confirm("Delete this category?")) {
                deleteCategory(btn.dataset.id);
            }
        });
    });
}

// Modal Logic
let renameId = null;

function openRenameModal(id, currentName) {
    renameId = id;
    document.getElementById("rename-category-input").value = currentName;
    document.getElementById("rename-modal").style.display = "flex";
}

document.getElementById("rename-confirm-btn").addEventListener("click", () => {
    const newName = document.getElementById("rename-category-input").value.trim();
    if (!newName) return alert("Category name required.");
    renameCategory(renameId, newName);
    document.getElementById("rename-modal").style.display = "none";
});

document.getElementById("rename-cancel-btn").addEventListener("click", () => {
    document.getElementById("rename-modal").style.display = "none";
});

// Add new category form
document.getElementById("add-category-form").addEventListener("submit", e => {
    e.preventDefault();
    const name = document.getElementById("new-category-name").value.trim();
    if (!name) return;

    addCategory(name);
    document.getElementById("new-category-name").value = "";
});

// Initialize
document.addEventListener("DOMContentLoaded", loadCategories);
