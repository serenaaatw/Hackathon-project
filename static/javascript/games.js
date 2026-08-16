// static/js/game.js
// Juego 1 (Emparejar): Imagen -> Palabra  /  Video LSA -> Imagen
// Mezcla las palabras de la misma categoría como distractores.
// Depende de las variables globales PALABRAS e IMG_BASE
// que se definen inline en templates/games/juego1.html

(function () {
  const state = { mode: "A", order: [], index: 0, answered: false };

  const els = {
    trail: document.getElementById("trail"),
    promptImageCard: document.getElementById("promptImageCard"),
    promptVideoCard: document.getElementById("promptVideoCard"),
    promptSticker: document.getElementById("promptSticker"),
    instruction: document.getElementById("instruction"),
    options: document.getElementById("options"),
    feedback: document.getElementById("feedback"),
    modeToggle: document.getElementById("modeToggle"),
    modeLabel: document.getElementById("modeLabel"),
  };

  function shuffle(arr) {
    const a = [...arr];
    for (let i = a.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
  }

  function currentWord() {
    return PALABRAS[state.order[state.index]];
  }

  function buildTrail() {
    els.trail.innerHTML = "";
    PALABRAS.forEach(() => {
      const dot = document.createElement("div");
      dot.className = "trail__step";
      els.trail.appendChild(dot);
    });
  }

  function updateTrail() {
    [...els.trail.children].forEach((dot, i) => {
      dot.classList.toggle("is-done", i < state.index);
      dot.classList.toggle("is-current", i === state.index);
    });
  }

  function renderPrompt() {
    const item = currentWord();

    if (state.mode === "A") {
      els.promptImageCard.hidden = false;
      els.promptVideoCard.hidden = true;
      els.promptSticker.innerHTML = `<img src="${IMG_BASE}${item.image_file}" alt="${item.word}" class="prompt-img">`;
      els.instruction.textContent = "Tocá la palabra que corresponde";
    } else {
      els.promptImageCard.hidden = true;
      els.promptVideoCard.hidden = false;
      els.instruction.textContent = "Mirá la seña y tocá la imagen que corresponde";
    }
  }

  function renderOptions() {
    els.options.innerHTML = "";
    els.feedback.textContent = "";
    els.feedback.className = "feedback";
    state.answered = false;

    const item = currentWord();
    const distractores = shuffle(PALABRAS.filter((w) => w.word !== item.word)).slice(0, 2);
    const opciones = shuffle([item, ...distractores]);

    opciones.forEach((opcion) => {
      const btn = document.createElement("button");
      btn.type = "button";

      if (state.mode === "A") {
        btn.className = "option";
        btn.textContent = opcion.word;
      } else {
        btn.className = "option option--image";
        btn.innerHTML = `<img src="${IMG_BASE}${opcion.image_file}" alt="${opcion.word}" class="option-img">`;
        btn.setAttribute("aria-label", opcion.word);
      }

      btn.addEventListener("click", () => handleAnswer(btn, opcion.word === item.word));
      els.options.appendChild(btn);
    });
  }

  function handleAnswer(btn, correcto) {
    if (state.answered) return;
    state.answered = true;

    [...els.options.children].forEach((b) => b.classList.add("is-disabled"));

    if (correcto) {
      btn.classList.remove("is-disabled");
      btn.classList.add("is-correct");
      els.feedback.textContent = "¡Muy bien! 🎉";
      els.feedback.classList.add("is-success");
      setTimeout(nextWord, 1100);
    } else {
      btn.classList.remove("is-disabled");
      btn.classList.add("is-wrong");
      els.feedback.textContent = "Probemos de nuevo";
      els.feedback.classList.add("is-retry");
      setTimeout(() => {
        [...els.options.children].forEach((b) => {
          b.classList.remove("is-disabled", "is-wrong");
        });
        els.feedback.textContent = "";
        els.feedback.className = "feedback";
        state.answered = false;
      }, 900);
    }
  }

  function nextWord() {
    state.index += 1;

    if (state.index >= state.order.length) {
      state.order = shuffle(PALABRAS.map((_, i) => i));
      state.index = 0;
    }

    updateTrail();
    renderPrompt();
    renderOptions();
  }

  function toggleMode() {
    state.mode = state.mode === "A" ? "B" : "A";
    els.modeLabel.textContent = state.mode === "A" ? "Imagen → Palabra" : "Seña LSA → Imagen";
    renderPrompt();
    renderOptions();
  }

  function init() {
    if (!PALABRAS || PALABRAS.length < 3) {
      els.instruction.textContent = "Esta categoría todavía no tiene suficientes palabras cargadas.";
      return;
    }
    state.order = shuffle(PALABRAS.map((_, i) => i));
    buildTrail();
    updateTrail();
    renderPrompt();
    renderOptions();
    els.modeToggle.addEventListener("click", toggleMode);
  }

  init();
})();