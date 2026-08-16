// static/javascript/reconocer.js
// Fase de reconocimiento: cada pantalla muestra foto + seña + palabra
// juntos, para un mismo animal. La flecha derecha avanza al siguiente
// animal (no a un "paso" separado). Repetible, 100% visual.
// Depende de las variables globales PALABRAS, IMG_BASE y URL_JUEGO
// que se definen inline en templates/child/reconocer.html

(function () {
  // Paleta que va rotando para que cada palabra se sienta "viva" y llame la atención.
  const PALETA = ["var(--coral)", "var(--turquoise-dark)", "var(--ink)", "#E0A100"];

  const state = {
    wordIndex: 0,
    visited: new Set(), // índices de animales ya vistos al menos una vez
  };

  const els = {
    sticker: document.getElementById("promptSticker"),
    wordText: document.getElementById("wordText"),
    dots: document.getElementById("reconDots"),
    btnPrev: document.getElementById("btnPrev"),
    btnNext: document.getElementById("btnNext"),
    btnJugar: document.getElementById("btnJugar"),
  };

  function renderDots() {
    els.dots.innerHTML = "";
    PALABRAS.forEach(() => {
      const dot = document.createElement("div");
      dot.className = "recon-dots__dot";
      els.dots.appendChild(dot);
    });
  }

  function updateDots() {
    [...els.dots.children].forEach((dot, i) => {
      dot.classList.toggle("is-current", i === state.wordIndex);
      dot.classList.toggle("is-done", state.visited.has(i) && i !== state.wordIndex);
    });
  }

  function updatePlayButton() {
    if (state.visited.size >= PALABRAS.length) {
      els.btnJugar.hidden = false;
    }
  }

  function render() {
    const item = PALABRAS[state.wordIndex];

    els.sticker.innerHTML = `<img src="${IMG_BASE}${item.image_file}" alt="${item.word}" class="prompt-img">`;

    els.wordText.textContent = item.word;
    els.wordText.style.color = PALETA[state.wordIndex % PALETA.length];

    state.visited.add(state.wordIndex);
    updateDots();
    updatePlayButton();
  }

  function next() {
    state.wordIndex = (state.wordIndex + 1) % PALABRAS.length;
    render();
  }

  function prev() {
    state.wordIndex = (state.wordIndex - 1 + PALABRAS.length) % PALABRAS.length;
    render();
  }

  function init() {
    if (!PALABRAS || PALABRAS.length === 0) return;
    renderDots();
    render();
    els.btnNext.addEventListener("click", next);
    els.btnPrev.addEventListener("click", prev);
    els.btnJugar.addEventListener("click", () => {
      window.location.href = URL_JUEGO;
    });
  }

  init();
})();