let selectedMood = null;

const MOODS = [
  { label: "Overthinking", emoji: "🌀" },
  { label: "Career Pressure", emoji: "💼" },
  { label: "Heartbreak", emoji: "💔" },
  { label: "Sunday Anxiety", emoji: "😶" },
  { label: "Quarter-life Crisis", emoji: "🪞" },
  { label: "Hustle vs Soft Life", emoji: "⚖️" },
  { label: "First-gen Pressure", emoji: "🎓" },
  { label: "Loneliness", emoji: "🪟" },
  { label: "Self-doubt", emoji: "🪨" },
  { label: "Healing Era", emoji: "🌱" },
];

function buildMoodGrid() {
  const grid = document.getElementById("mood-grid");
  MOODS.forEach(mood => {
    const card = document.createElement("div");
    card.className = "mood-card";
    card.dataset.mood = mood.label;
    card.innerHTML = `<div class="mood-emoji">${mood.emoji}</div><div class="mood-label">${mood.label}</div>`;
    card.addEventListener("click", () => {
      selectedMood = mood.label;
      document.querySelectorAll(".mood-card").forEach(c => c.classList.remove("selected"));
      card.classList.add("selected");
    });
    grid.appendChild(card);
  });
}

async function generate() {
  if (!selectedMood) {
    Toast.show("Pick a mood first", "error");
    return;
  }
  const userContext = document.getElementById("user-context").value.trim();
  const aiMode = document.getElementById("ai-mode-select").value;

  showSpinner("Writing your story...");
  try {
    const data = await apiFetch("/api/generate", {
      method: "POST",
      body: { mood: selectedMood, user_context: userContext, ai_mode: aiMode },
    });
    window.location.href = `/preview?id=${data.carousel.id}`;
  } catch (err) {
    hideSpinner();
    Toast.show(err.message, "error", 5000);
  }
}

document.addEventListener("DOMContentLoaded", async () => {
  buildMoodGrid();

  // Load saved AI mode from settings
  try {
    const settings = await apiFetch("/api/settings");
    const select = document.getElementById("ai-mode-select");
    if (settings.ai_mode) select.value = settings.ai_mode;
  } catch (_) {}

  document.getElementById("generate-btn").addEventListener("click", generate);
});
