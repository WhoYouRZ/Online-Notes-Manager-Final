// ======================================================
// QUICK CATEGORY ADD INSIDE NOTE EDITOR (AJAX)
// ======================================================

const quickAddBtn = document.getElementById("quick-add-category-btn");
const categorySelect = document.getElementById("category_id");

let modal;

// Create modal dynamically
function createModal() {
    modal = document.createElement("div");
    modal.className = "modal-overlay";
    modal.style.display = "none";

    modal.innerHTML = `
        <div class="modal-box">
            <h3>Add New Category</h3>

            <input 
                type="text" 
                id="editor-new-category" 
                placeholder="Category name"
            >

            <button id="editor-save-category" class="btn-primary">Save</button>
            <button id="editor-cancel-category" class="btn-secondary">Cancel</button>
        </div>
    `;

    document.body.appendChild(modal);

    document.getElementById("editor-save-category").addEventListener("click", saveNewCategory);
    document.getElementById("editor-cancel-category").addEventListener("click", () => {
        modal.style.display = "none";
    });
}

function openCategoryModal() {
    document.getElementById("editor-new-category").value = "";
    modal.style.display = "flex";
}

// Save a new category
async function saveNewCategory() {
    const name = document.getElementById("editor-new-category").value.trim();
    if (!name) return alert("Enter category name.");

    // AJAX call
    const res = await fetch("/category-api/create", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ name })
    });

    if (!res.ok) {
        alert("Failed to create category.");
        return;
    }

    modal.style.display = "none";
    refreshDropdown();
}

// Refresh dropdown after creating a new category
async function refreshDropdown() {
    const res = await fetch("/category-api/list");
    const categories = await res.json();

    categorySelect.innerHTML = `<option value="">No Category</option>`;

    categories.forEach(cat => {
        const opt = document.createElement("option");
        opt.value = cat.id;
        opt.textContent = cat.name;
        categorySelect.appendChild(opt);
    });
}

// Init
document.addEventListener("DOMContentLoaded", () => {
    if (!quickAddBtn || !categorySelect) return;

    createModal();
    quickAddBtn.addEventListener("click", openCategoryModal);
});
