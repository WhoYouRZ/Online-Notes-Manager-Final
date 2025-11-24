// ======================================================
// Sync Local Notes → Cloud After Login
// ======================================================

const LS_KEY = "guest_notes";
const SYNC_FLAG = "sync_pending";

// ------------------------------------------------------
// Detect if user arrived on dashboard right after login
// We set SYNC_FLAG before redirecting to login (optional)
// ------------------------------------------------------

function shouldSync() {
    return localStorage.getItem(SYNC_FLAG) === "1";
}

// ------------------------------------------------------
// Get all guest notes from localStorage
// ------------------------------------------------------

function getLocalNotes() {
    const raw = localStorage.getItem(LS_KEY);
    try {
        return raw ? JSON.parse(raw) : [];
    } catch (err) {
        console.error("Failed to parse local notes for sync", err);
        return [];
    }
}

// ------------------------------------------------------
// Send notes to the backend for merging
// ------------------------------------------------------

async function sendNotesToServer(notes) {
    try {
        const response = await fetch("/notes/sync", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ notes: notes })
        });

        const data = await response.json();
        return data.status === "success";

    } catch (err) {
        console.error("Sync request failed", err);
        return false;
    }
}

// ------------------------------------------------------
// Main Sync Logic
// ------------------------------------------------------

async function syncNotes() {
    const notes = getLocalNotes();
    if (!notes.length) {
        localStorage.removeItem(SYNC_FLAG);
        return; // nothing to sync
    }

    const ok = await sendNotesToServer(notes);

    if (ok) {
        console.log("Local notes successfully synced to cloud.");
        localStorage.removeItem(LS_KEY);      // Clear guest notes
        localStorage.removeItem(SYNC_FLAG);   // Stop future syncs
    } else {
        console.warn("Note sync failed. Will try again on next login.");
    }
}

// ------------------------------------------------------
// Initialize: run only on logged-in pages
// ------------------------------------------------------

function initSync() {
    const dashboardEl = document.querySelector(".dashboard-container");

    // Only run sync if user is logged-in and on dashboard
    if (dashboardEl && shouldSync()) {
        syncNotes();
    }
}

document.addEventListener("DOMContentLoaded", initSync);
