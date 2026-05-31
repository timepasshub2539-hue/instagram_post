async function loadDrafts() {
  const container = document.getElementById("drafts-container");
  container.innerHTML = "";

  let data;
  try {
    data = await apiFetch("/api/drafts");
  } catch (err) {
    container.innerHTML = `<div class="empty-state"><div class="empty-state-title">Could not load drafts</div><div class="empty-state-text">${err.message}</div></div>`;
    return;
  }

  const drafts = data.drafts || [];
  if (drafts.length === 0) {
    container.innerHTML = `
      <div class="empty-state">
        <div class="empty-state-icon">📭</div>
        <div class="empty-state-title">No drafts yet</div>
        <div class="empty-state-text">Generate a carousel from the home screen and it'll appear here.</div>
      </div>`;
    return;
  }

  const grid = document.createElement("div");
  grid.className = "drafts-grid";

  drafts.forEach(draft => {
    const card = document.createElement("div");
    card.className = "draft-card";
    card.innerHTML = `
      <div class="draft-mood-badge">${draft.mood || "Unknown"}</div>
      <div class="draft-hook">${draft.hook || ""}</div>
      <div class="draft-date">${formatDate(draft.created_at)}</div>
      <button class="draft-delete" data-id="${draft.id}" title="Delete">×</button>
    `;
    card.addEventListener("click", e => {
      if (e.target.classList.contains("draft-delete")) return;
      window.location.href = `/preview?id=${draft.id}`;
    });
    card.querySelector(".draft-delete").addEventListener("click", async e => {
      e.stopPropagation();
      if (!confirm("Delete this draft?")) return;
      try {
        await apiFetch(`/api/drafts/${draft.id}`, { method: "DELETE" });
        Toast.show("Draft deleted", "success");
        card.remove();
        if (grid.children.length === 0) loadDrafts();
      } catch (err) {
        Toast.show("Delete failed: " + err.message, "error");
      }
    });
    grid.appendChild(card);
  });

  container.appendChild(grid);
}

document.addEventListener("DOMContentLoaded", loadDrafts);
