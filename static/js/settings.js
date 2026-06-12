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

  // API Keys (only populate if a stored value exists — keep blank otherwise)
  document.getElementById("anthropic-key-input").value = currentSettings.anthropic_api_key || "";
  document.getElementById("openai-key-input").value    = currentSettings.openai_api_key    || "";
  document.getElementById("mistral-key-input").value   = currentSettings.mistral_api_key   || "";

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
  setStatus("claude-status-dot",   "claude-status-text",   currentSettings.claude_available,   "API key set",  "No API key");
  setStatus("openai-status-dot",   "openai-status-text",   currentSettings.openai_available,   "API key set",  "No API key");
  setStatus("mistral-status-dot",  "mistral-status-text",  currentSettings.mistral_available,  "API key set",  "No API key");
  setStatus("ollama-status-dot",   "ollama-status-text",   currentSettings.ollama_available,   "Running",      "Not detected");
  setStatus("lmstudio-status-dot", "lmstudio-status-text", currentSettings.lmstudio_available, "Running",      "Not detected");
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
    anthropic_api_key: document.getElementById("anthropic-key-input").value.trim(),
    openai_api_key:    document.getElementById("openai-key-input").value.trim(),
    mistral_api_key:   document.getElementById("mistral-key-input").value.trim(),
  };

  try {
    await apiFetch("/api/settings", { method: "POST", body: payload });
    Toast.show("Settings saved", "success");
    Object.assign(currentSettings, payload);
    currentSettings.claude_available  = !!payload.anthropic_api_key || currentSettings.claude_available;
    currentSettings.openai_available  = !!payload.openai_api_key    || currentSettings.openai_available;
    currentSettings.mistral_available = !!payload.mistral_api_key   || currentSettings.mistral_available;
    updateStatusBadges();
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

  document.querySelectorAll(".key-toggle-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const input = document.getElementById(btn.dataset.target);
      if (!input) return;
      input.type = input.type === "password" ? "text" : "password";
    });
  });

  document.getElementById("save-btn").addEventListener("click", saveSettings);
});
