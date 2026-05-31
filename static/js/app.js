// Shared utilities for JournalDrop

const Toast = (() => {
  let container = null;
  function getContainer() {
    if (!container) {
      container = document.createElement("div");
      container.className = "toast-container";
      document.body.appendChild(container);
    }
    return container;
  }
  return {
    show(msg, type = "info", duration = 3000) {
      const t = document.createElement("div");
      t.className = `toast ${type}`;
      t.textContent = msg;
      getContainer().appendChild(t);
      setTimeout(() => t.remove(), duration);
    }
  };
})();

function showSpinner(text = "Generating...") {
  let el = document.getElementById("spinner-overlay");
  if (!el) {
    el = document.createElement("div");
    el.id = "spinner-overlay";
    el.className = "spinner-overlay";
    el.innerHTML = `<div class="spinner"></div><div class="spinner-text">${text}</div>`;
    document.body.appendChild(el);
  } else {
    el.querySelector(".spinner-text").textContent = text;
    el.classList.remove("hidden");
  }
}

function hideSpinner() {
  const el = document.getElementById("spinner-overlay");
  if (el) el.classList.add("hidden");
}

async function apiFetch(url, options = {}) {
  const defaults = {
    headers: { "Content-Type": "application/json" },
  };
  const opts = { ...defaults, ...options };
  if (opts.body && typeof opts.body === "object") {
    opts.body = JSON.stringify(opts.body);
  }
  const res = await fetch(url, opts);
  if (!res.ok) {
    let detail = `Request failed (${res.status})`;
    try {
      const err = await res.json();
      detail = err.detail || detail;
    } catch (_) {}
    throw new Error(detail);
  }
  return res.json();
}

function formatDate(isoString) {
  if (!isoString) return "";
  const d = new Date(isoString);
  return d.toLocaleDateString("en-IN", { day: "numeric", month: "short", year: "numeric" });
}

// Mark current nav item active based on pathname
function setActiveNav() {
  const path = window.location.pathname;
  document.querySelectorAll(".nav-item").forEach(item => {
    const href = item.getAttribute("href") || "";
    const isActive =
      (path === "/" && href === "/") ||
      (path !== "/" && href !== "/" && path.startsWith(href));
    item.classList.toggle("active", isActive);
  });
}

document.addEventListener("DOMContentLoaded", setActiveNav);
