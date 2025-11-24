// ======================================================
// Local Storage Notes Manager (Guest Mode)
// ======================================================

// All notes stored under one key
const LS_KEY = "guest_notes";

// Load notes from localStorage
function loadNotes() {
    const data = localStorage.getItem(LS_KEY);
    try {
        return data ? JSON.parse(data) : [];
    } catch (err) {
        console.error("Failed to parse local notes", err);
        return [];
    }
}

// Save notes to localStorage
function saveNotes(notes) {
    localStorage.setItem(LS_KEY, JSON.stringify(notes));
}

// Generate a unique ID for each note
function generateId() {
    return "note_" + Date.now() + "_" + Math.floor(Math.random() * 1000);
}

// Create a new note
function createNote(title, content) {
    const notes = loadNotes();

    const newNote = {
        id: generateId(),
        title: title.trim(),
        content: content.trim(),
        created_at: new Date().toISOString()
    };

    notes.push(newNote);
    saveNotes(notes);
    renderNotes();
}

// Edit an existing note
function updateNote(id, newTitle, newContent) {
    const notes = loadNotes();
    const index = notes.findIndex(n => n.id === id);
    if (index !== -1) {
        notes[index].title = newTitle.trim();
        notes[index].content = newContent.trim();
        saveNotes(notes);
        renderNotes();
    }
}

// Delete a note
function deleteNote(id) {
    let notes = loadNotes();
    notes = notes.filter(n => n.id !== id);
    saveNotes(notes);
    renderNotes();
}

// Render notes into the list container
function renderNotes() {
    const container = document.getElementById("guest-notes-list");
    if (!container) return; // Only run on guest pages

    const notes = loadNotes();
    container.innerHTML = "";

    if (notes.length === 0) {
        container.innerHTML = "<p class='no-notes'>No notes yet. Start writing above.</p>";
        return;
    }

    notes.forEach(note => {
        const card = document.createElement("div");
        card.className = "note-card";

        card.innerHTML = `
            <h3>${note.title || "Untitled"}</h3>
            <p>${note.content.substring(0, 200)}${note.content.length > 200 ? "..." : ""}</p>

            <div class="note-footer">
                <button class="btn-small edit-btn" data-id="${note.id}">Edit</button>
                <button class="btn-small-danger delete-btn" data-id="${note.id}">Delete</button>
            </div>
        `;

        container.appendChild(card);
    });

    attachNoteButtons();
}

// Attach click events to all edit/delete buttons
function attachNoteButtons() {
    document.querySelectorAll(".edit-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            const id = btn.dataset.id;
            loadNoteIntoEditor(id);
        });
    });

    document.querySelectorAll(".delete-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            const id = btn.dataset.id;
            if (confirm("Delete this note?")) {
                deleteNote(id);
            }
        });
    });
}

// Load an existing note into the editor for editing
function loadNoteIntoEditor(id) {
    const notes = loadNotes();
    const note = notes.find(n => n.id === id);

    if (!note) return;

    document.getElementById("guest-title").value = note.title;
    document.getElementById("guest-content").value = note.content;

    const saveBtn = document.getElementById("guest-save-btn");
    saveBtn.textContent = "Update Note";
    saveBtn.dataset.editId = id;
}

// Save or update a note from the form
function initEditor() {
    const saveBtn = document.getElementById("guest-save-btn");
    if (!saveBtn) return;

    saveBtn.addEventListener("click", () => {
        const title = document.getElementById("guest-title").value;
        const content = document.getElementById("guest-content").value;

        if (!title.trim() && !content.trim()) {
            alert("Note cannot be empty.");
            return;
        }

        const editId = saveBtn.dataset.editId;

        if (editId) {
            updateNote(editId, title, content);
            delete saveBtn.dataset.editId;
            saveBtn.textContent = "Save Note";
        } else {
            createNote(title, content);
        }

        // Clear editor
        document.getElementById("guest-title").value = "";
        document.getElementById("guest-content").value = "";
    });
}

// Initialize guest mode UI
function initGuestMode() {
    if (document.getElementById("guest-notes-list")) {
        renderNotes();
    }
    initEditor();
}

// Start after DOM load
document.addEventListener("DOMContentLoaded", initGuestMode);
