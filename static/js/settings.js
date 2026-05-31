let currentSettings = {};

async function loadSettings() {
  try {
    currentSettings = await apiFetch("/api/settings");
  } catch (err) {
    Toast.show("Could not load settings", "error");
    return;
  }

  // AI mode dropdown
  const modeSelect = document.getElementById("ai-mode-select");
  if (modeSelect) modeSelect.value = currentSettings.ai_mode || "online";

  // Profile
  document.getElementById("handle-input").value = currentSettings.instagram_handle || "";
  document.getElementById("niche-input").value   = currentSettings.niche || "";

  // Times
  document.getElementById("time1-input").value = currentSettings.posting_time_1 || "06:00";
  document.getElementById("time2-input").value = currentSettings.posting_time_2 || "21:00";

  // Model names
  document.getElementById("openai-model-input").value   = currentSettings.openai_model   || "gpt-4o-mini";
  document.getElementById("mistral-model-input").value  = currentSettings.mistral_model  || "mistral-small-latest";
  document.getElementById("ollama-model-input").value   = currentSettings.ollama_model   || "llama3";
  document.getElementById("lmstudio-model-input").value = currentSettings.lmstudio_model || "local-model";
  document.getElementById("lmstudio-url-input").value   = currentSettings.lmstudio_url   || "http://localhost:1234/v1";

  // Design
  setThemeUI(currentSettings.default_theme || "dark");
  setFontUI(currentSettings.default_font   || "DMSans");

  updateStatusBadges();
}

function setThemeUI(theme) {
  document.querySelectorAll('.option-chip[data-group="theme"]').forEach(c => {
    c.classList.toggle("selected", c.dataset.value === theme);
  });
}

function setFontUI(font) {
  document.querySelectorAll('.option-chip[data-group="font"]').forEach(c => {
    c.classList.toggle("selected", c.dataset.value === font);
  });
}

function setStatus(id, textId, available, trueText, falseText) {
  const dot  = document.getElementById(id);
  const text = document.getElementById(textId);
  if (!dot) return;
  dot.className  = `status-dot ${available ? "online" : "offline"}`;
  if (text) text.textContent = available ? trueText : falseText;
}

function updateStatusBadges() {
  setStatus("claude-status-dot",   "claude-status-text",   currentSettings.claude_available,   "API key found",  "No API key in .env");
  setStatus("openai-status-dot",   "openai-status-text",   currentSettings.openai_available,   "API key found",  "No API key in .env");
  setStatus("mistral-status-dot",  "mistral-status-text",  currentSettings.mistral_available,  "API key found",  "No API key in .env");
  setStatus("ollama-status-dot",   "ollama-status-text",   currentSettings.ollama_available,   "Running",        "Not detected");
  setStatus("lmstudio-status-dot", "lmstudio-status-text", currentSettings.lmstudio_available, "Running",        "Not detected");
}

async function saveSettings() {
  const modeSelect = document.getElementById("ai-mode-select");
  const theme = document.querySelector('.option-chip[data-group="theme"].selected')?.dataset.value || "dark";
  const font  = document.querySelector('.option-chip[data-group="font"].selected')?.dataset.value  || "DMSans";

  const payload = {
    ai_mode:           modeSelect ? modeSelect.value : "online",
    default_theme:     theme,
    default_font:      font,
    instagram_handle:  document.getElementById("handle-input").value.trim().replace(/^@/, ""),
    niche:             document.getElementById("niche-input").value.trim(),
    posting_time_1:    document.getElementById("time1-input").value,
    posting_time_2:    document.getElementById("time2-input").value,
    openai_model:      document.getElementById("openai-model-input").value.trim()   || "gpt-4o-mini",
    mistral_model:     document.getElementById("mistral-model-input").value.trim()  || "mistral-small-latest",
    ollama_model:      document.getElementById("ollama-model-input").value.trim()   || "llama3",
    lmstudio_model:    document.getElementById("lmstudio-model-input").value.trim() || "local-model",
    lmstudio_url:      document.getElementById("lmstudio-url-input").value.trim()   || "http://localhost:1234/v1",
  };

  try {
    await apiFetch("/api/settings", { method: "POST", body: payload });
    Toast.show("Settings saved", "success");
    Object.assign(currentSettings, payload);
  } catch (err) {
    Toast.show("Save failed: " + err.message, "error");
  }
}

document.addEventListener("DOMContentLoaded", async () => {
  await loadSettings();

  document.querySelectorAll(".option-chip").forEach(chip => {
    chip.addEventListener("click", () => {
      const group = chip.dataset.group;
      document.querySelectorAll(`.option-chip[data-group="${group}"]`).forEach(c => c.classList.remove("selected"));
      chip.classList.add("selected");
    });
  });

  document.getElementById("save-btn").addEventListener("click", saveSettings);
});
