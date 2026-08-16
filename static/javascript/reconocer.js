// static/js/reconocer.js
// Fase de reconocimiento: foto -> seña -> palabra, repetible, 100% visual.
// Depende de las variables globales PALABRAS, IMG_BASE y URL_JUEGO
// que se definen inline en templates/child/reconocer.html

(function () {
  const STEPS = { FOTO: 0, SENA: 1, PALABRA: 2 };

  const state = {
    wordIndex: 0,
    step: STEPS.FOTO,
    visited: new Set(), // índices de palabras ya vistas completas al menos una vez
  };

  const els = {
    sticker: document.getElementById("promptSticker"),
    dots: document.getElementById("reconDots"),
    btnPrev: document.getElementById("btnPrev"),
    btnNext: document.getElementById("btnNext"),
    btnJugar: document.getElementById("btnJugar"),
  };

  function senaPlaceholderSVG() {
    return `
      <div class="sena-placeholder" aria-label="Seña en LSA, video pendiente">
        <svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
          <path d="M22 52c-6-1-11-7-11-15V26a4 4 0 0 1 8 0v8" stroke="var(--turquoise-dark)" stroke-width="3" stroke-linecap="round"/>
          <rect x="20" y="14" width="8" height="22" rx="4" fill="var(--turquoise)" stroke="var(--turquoise-dark)" stroke-width="3"/>
          <rect x="29" y="10" width="8" height="26" rx="4" fill="var(--yellow)" stroke="var(--turquoise-dark)" stroke-width="3"/>
          <rect x="38" y="14" width="8" height="22" rx="4" fill="var(--coral)" stroke="var(--turquoise-dark)" stroke-width="3"/>
          <path d="M11 32v8c0 7 6 13 13 13h10c7 0 13-6 13-13v-8" stroke="var(--turquoise-dark)" stroke-width="3" stroke-linecap="round" fill="#fff"/>
        </svg>
        <span class="sena-placeholder__label">Seña en LSA</span>
      </div>
    `;
  }

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

  function renderStep() {
    const item = PALABRAS[state.wordIndex];

    if (state.step === STEPS.FOTO) {
      els.sticker.innerHTML = `<img src="${IMG_BASE}${item.image_file}" alt="${item.word}" class="prompt-img">`;
    } else if (state.step === STEPS.SENA) {
      els.sticker.innerHTML = senaPlaceholderSVG();
    } else {
      els.sticker.innerHTML = `<span class="prompt-word">${item.word}</span>`;
      state.visited.add(state.wordIndex);
    }

    updateDots();
    updatePlayButton();
  }

  function next() {
    state.step += 1;
    if (state.step > STEPS.PALABRA) {
      state.step = STEPS.FOTO;
      state.wordIndex = (state.wordIndex + 1) % PALABRAS.length;
    }
    renderStep();
  }

  function prev() {
    state.step -= 1;
    if (state.step < STEPS.FOTO) {
      state.step = STEPS.PALABRA;
      state.wordIndex = (state.wordIndex - 1 + PALABRAS.length) % PALABRAS.length;
    }
    renderStep();
  }

  function init() {
    if (!PALABRAS || PALABRAS.length === 0) return;
    renderDots();
    renderStep();
    els.btnNext.addEventListener("click", next);
    els.btnPrev.addEventListener("click", prev);
    els.btnJugar.addEventListener("click", () => {
      window.location.href = URL_JUEGO;
    });
  }

  init();
})();