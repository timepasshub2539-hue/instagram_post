let carouselId = null;
let draft = null;
let currentSlide = 0;
let images = [];
let hammer = null;
let design = {
  theme: "dark",
  font: "DMSans",
  font_size_body: 48,
  font_size_large: 72,
  background_color: "#0d0d0d",
  text_color: "#f5f5f5",
  accent_color: "#a78bfa",
  text_align: "left",
  handle: "",
};

const slideKeys = ["hook", "slide2", "slide3", "slide4", "closer"];
const slideLabels = ["Slide 1 — Hook", "Slide 2", "Slide 3", "Slide 4", "Slide 5 — Closer"];

function getSlideText(idx) {
  return draft ? draft[slideKeys[idx]] || "" : "";
}

function updateDots() {
  document.querySelectorAll(".dot").forEach((d, i) => {
    d.classList.toggle("active", i === currentSlide);
  });
}

function goToSlide(idx) {
  currentSlide = Math.max(0, Math.min(idx, 4));
  const track = document.getElementById("slides-track");
  track.style.transform = `translateX(-${currentSlide * 100}%)`;
  updateDots();
}

function renderImages() {
  const track = document.getElementById("slides-track");
  track.innerHTML = "";
  for (let i = 0; i < 5; i++) {
    const item = document.createElement("div");
    item.className = "slide-item";
    if (images[i]) {
      const img = document.createElement("img");
      img.src = `data:image/png;base64,${images[i]}`;
      img.alt = `Slide ${i + 1}`;
      item.appendChild(img);
    } else {
      const ph = document.createElement("div");
      ph.className = "slide-placeholder";
      ph.textContent = `Slide ${i + 1}`;
      item.appendChild(ph);
    }
    item.addEventListener("click", () => openEditor(i));
    track.appendChild(item);
  }
  goToSlide(currentSlide);
}

async function renderCarousel() {
  showSpinner("Rendering slides...");
  try {
    const data = await apiFetch("/api/render", {
      method: "POST",
      body: { carousel_id: carouselId, design },
    });
    images = data.images;
    renderImages();
  } catch (err) {
    Toast.show("Render failed: " + err.message, "error");
  } finally {
    hideSpinner();
  }
}

function openEditor(slideIdx) {
  const modal = document.getElementById("editor-modal");
  const textarea = document.getElementById("editor-textarea");
  const title = document.getElementById("editor-title");
  title.textContent = slideLabels[slideIdx];
  textarea.value = getSlideText(slideIdx);
  textarea.dataset.slideIdx = slideIdx;
  modal.classList.remove("hidden");
  setTimeout(() => textarea.focus(), 50);
}

function closeEditor() {
  document.getElementById("editor-modal").classList.add("hidden");
}

async function saveEditorAndRerender() {
  const textarea = document.getElementById("editor-textarea");
  const idx = parseInt(textarea.dataset.slideIdx);
  const key = slideKeys[idx];
  draft[key] = textarea.value;

  // Persist to backend
  await apiFetch(`/api/drafts/${carouselId}`, { method: "POST", body: draft });
  closeEditor();
  await renderCarousel();
}

function openDesignPanel() {
  document.getElementById("design-modal").classList.remove("hidden");
}

function closeDesignPanel() {
  document.getElementById("design-modal").classList.add("hidden");
}

async function applyDesign() {
  // Collect design values from UI
  design.theme = document.querySelector('.option-chip[data-group="theme"].selected')?.dataset.value || design.theme;
  design.font = document.querySelector('.option-chip[data-group="font"].selected')?.dataset.value || design.font;
  design.text_align = document.querySelector('.option-chip[data-group="align"].selected')?.dataset.value || design.text_align;
  const size = document.querySelector('.option-chip[data-group="size"].selected')?.dataset.value;
  if (size === "small") { design.font_size_body = 42; design.font_size_large = 64; }
  else if (size === "large") { design.font_size_body = 56; design.font_size_large = 80; }
  else { design.font_size_body = 48; design.font_size_large = 72; }

  // Apply theme colors
  if (design.theme === "light") {
    design.background_color = "#fafafa";
    design.text_color = "#1a1a1a";
    design.accent_color = "#7c3aed";
  } else {
    design.background_color = "#0d0d0d";
    design.text_color = "#f5f5f5";
    design.accent_color = "#a78bfa";
  }

  // Save design to draft
  draft.design = { ...design };
  await apiFetch(`/api/drafts/${carouselId}`, { method: "POST", body: draft });

  closeDesignPanel();
  await renderCarousel();
}

function initChips() {
  document.querySelectorAll(".option-chip").forEach(chip => {
    chip.addEventListener("click", () => {
      const group = chip.dataset.group;
      document.querySelectorAll(`.option-chip[data-group="${group}"]`).forEach(c => c.classList.remove("selected"));
      chip.classList.add("selected");
    });
  });
}

async function exportAll() {
  Toast.show("Preparing your ZIP...", "info");
  window.location.href = `/api/export/${carouselId}`;
}

function initHammer() {
  const screen = document.getElementById("phone-screen");
  if (!screen || !window.Hammer) return;
  hammer = new Hammer(screen);
  hammer.on("swipeleft", () => goToSlide(currentSlide + 1));
  hammer.on("swiperight", () => goToSlide(currentSlide - 1));
}

function renderCaptionSection() {
  if (!draft) return;
  const captionEl = document.getElementById("caption-text");
  const hashtagsEl = document.getElementById("hashtags-row");
  if (captionEl) captionEl.textContent = draft.caption || "";
  if (hashtagsEl) {
    hashtagsEl.innerHTML = (draft.hashtags || [])
      .map(h => `<span class="hashtag-chip">#${h}</span>`)
      .join("");
  }
}

document.addEventListener("DOMContentLoaded", async () => {
  const params = new URLSearchParams(window.location.search);
  carouselId = params.get("id");
  if (!carouselId) {
    window.location.href = "/";
    return;
  }

  showSpinner("Loading...");
  try {
    draft = await apiFetch(`/api/drafts/${carouselId}`);
    const settings = await apiFetch("/api/settings");
    design.handle = settings.instagram_handle || "";
    if (draft.design) Object.assign(design, draft.design);

    document.getElementById("page-mood").textContent = draft.mood || "";
    renderCaptionSection();
    initChips();

    // Set initial chip states based on current design
    const themeChip = document.querySelector(`.option-chip[data-group="theme"][data-value="${design.theme}"]`);
    if (themeChip) { document.querySelectorAll('.option-chip[data-group="theme"]').forEach(c=>c.classList.remove("selected")); themeChip.classList.add("selected"); }
    const fontChip = document.querySelector(`.option-chip[data-group="font"][data-value="${design.font}"]`);
    if (fontChip) { document.querySelectorAll('.option-chip[data-group="font"]').forEach(c=>c.classList.remove("selected")); fontChip.classList.add("selected"); }

  } catch (err) {
    hideSpinner();
    Toast.show("Failed to load draft", "error");
    return;
  }

  await renderCarousel();

  // Dot clicks
  document.querySelectorAll(".dot").forEach((d, i) => {
    d.addEventListener("click", () => goToSlide(i));
  });

  // Editor
  document.getElementById("editor-save-btn").addEventListener("click", saveEditorAndRerender);
  document.getElementById("editor-close-btn").addEventListener("click", closeEditor);
  document.getElementById("editor-modal").addEventListener("click", e => {
    if (e.target === e.currentTarget) closeEditor();
  });

  // Design panel
  document.getElementById("design-btn").addEventListener("click", openDesignPanel);
  document.getElementById("design-apply-btn").addEventListener("click", applyDesign);
  document.getElementById("design-close-btn").addEventListener("click", closeDesignPanel);
  document.getElementById("design-modal").addEventListener("click", e => {
    if (e.target === e.currentTarget) closeDesignPanel();
  });

  // Export
  document.getElementById("export-btn").addEventListener("click", exportAll);

  initHammer();
});
