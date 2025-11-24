// ======================================================
// Auto-save Drafts Every 5 Seconds (Guest Mode)
// ======================================================

const DRAFT_KEY = "guest_note_draft";

// Save draft to localStorage
function saveDraft() {
    const titleEl = document.getElementById("guest-title");
    const contentEl = document.getElementById("guest-content");

    if (!titleEl || !contentEl) return;

    const draft = {
        title: titleEl.value,
        content: contentEl.value,
        timestamp: new Date().toISOString()
    };

    localStorage.setItem(DRAFT_KEY, JSON.stringify(draft));
}

// Load draft on page load
function loadDraft() {
    const titleEl = document.getElementById("guest-title");
    const contentEl = document.getElementById("guest-content");

    if (!titleEl || !contentEl) return;

    const data = localStorage.getItem(DRAFT_KEY);
    if (!data) return;

    try {
        const draft = JSON.parse(data);

        // Only restore if fields are empty
        if (!titleEl.value.trim() && !contentEl.value.trim()) {
            titleEl.value = draft.title || "";
            contentEl.value = draft.content || "";
        }

    } catch (err) {
        console.error("Failed to load saved draft", err);
    }
}

// Clear draft after save (optional)
function clearDraft() {
    localStorage.removeItem(DRAFT_KEY);
}

// Listen for input changes
function initAutoSave() {
    const titleEl = document.getElementById("guest-title");
    const contentEl = document.getElementById("guest-content");

    if (!titleEl || !contentEl) return; // Only run on guest index page

    // Load existing draft
    loadDraft();

    // Auto-save every 5 seconds
    setInterval(saveDraft, 5000);

    // Clear draft when a real save happens
    const saveBtn = document.getElementById("guest-save-btn");
    if (saveBtn) {
        saveBtn.addEventListener("click", clearDraft);
    }
}

// Start when DOM loads
document.addEventListener("DOMContentLoaded", initAutoSave);
