// ======================================================
// Reminder Notification System (Logged-In Users Only)
// ======================================================

const TRIGGERED_KEY = "triggered_reminders";  // store IDs of already-fired reminders

// Load triggered reminders from localStorage (prevents duplicates)
function loadTriggered() {
    try {
        return JSON.parse(localStorage.getItem(TRIGGERED_KEY)) || [];
    } catch {
        return [];
    }
}

function saveTriggered(list) {
    localStorage.setItem(TRIGGERED_KEY, JSON.stringify(list));
}

// Parse datetime string from note_reminder field
function parseReminder(ts) {
    if (!ts) return null;
    try {
        return new Date(ts);
    } catch {
        return null;
    }
}

// Show a basic popup (lightweight & non-intrusive)
function showReminderPopup(message) {
    const popup = document.createElement("div");
    popup.className = "reminder-popup";
    popup.textContent = message;

    document.body.appendChild(popup);

    setTimeout(() => {
        popup.classList.add("visible");
    }, 10);

    // Hide after 6 seconds
    setTimeout(() => {
        popup.classList.remove("visible");
        setTimeout(() => popup.remove(), 400);
    }, 6000);
}

// Main reminder check function
function checkReminders() {
    const notes = document.querySelectorAll(".note-card");
    if (!notes.length) return;   // Not on dashboard

    const triggered = loadTriggered();
    const now = new Date();

    notes.forEach(card => {
        const noteId = card.dataset.noteId;
        const reminderEl = card.querySelector(".note-reminder");

        if (!reminderEl) return;

        const tsText = reminderEl.textContent.replace("Reminder:", "").trim();
        const reminderTime = parseReminder(tsText);

        if (!reminderTime) return;

        // Skip notifications that already fired
        if (triggered.includes(noteId)) return;

        // If time has passed → trigger notification
        if (now >= reminderTime) {
            showReminderPopup(`Reminder: ${card.querySelector(".note-title").textContent}`);
            triggered.push(noteId);
            saveTriggered(triggered);
        }
    });
}

// Initialize only for logged-in dashboard
function initReminderSystem() {
    const dashboard = document.querySelector(".dashboard-container");
    if (!dashboard) return;

    // Check every 30 seconds
    checkReminders();
    setInterval(checkReminders, 30000);
}

document.addEventListener("DOMContentLoaded", initReminderSystem);
