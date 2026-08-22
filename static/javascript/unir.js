// static/javascript/unir.js
// Juego Unir: el niño toca una imagen y después la palabra que le
// corresponde (o al revés). Si coinciden, quedan emparejadas.
// Depende de las variables globales PALABRAS e IMG_BASE
// que se definen inline en templates/games/juego_unir.html

(function () {

    const MAX_RONDAS = 3;

    const state = {
        ronda: 1,
        matched: 0,
        selectedImage: null, // { el, item }
        selectedWord: null,  // { el, item }
        locked: false,       // true mientras se muestra la animación de acierto/error
        terminado: false,
    };

    const els = {
        trail: document.getElementById("trail"),
        roundLabel: document.getElementById("roundLabel"),
        colImagenes: document.getElementById("colImagenes"),
        colPalabras: document.getElementById("colPalabras"),
        feedback: document.getElementById("feedback"),
    };


    function shuffle(arr) {

        const a = [...arr];

        for (let i = a.length - 1; i > 0; i--) {

            const j = Math.floor(Math.random() * (i + 1));

            [a[i], a[j]] = [a[j], a[i]];

        }

        return a;
    }


    function registrarResultado(idWord, correcto) {

        fetch("/juego/registrar-resultado", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ id_word: idWord, correcto: correcto }),
        }).catch(() => {});

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

            dot.classList.toggle("is-done", i < state.matched);

        });

    }


    function clearSelection() {

        if (state.selectedImage) {
            state.selectedImage.el.classList.remove("is-selected");
        }

        if (state.selectedWord) {
            state.selectedWord.el.classList.remove("is-selected");
        }

        state.selectedImage = null;
        state.selectedWord = null;

    }


    function evaluarPar() {

        if (!state.selectedImage || !state.selectedWord) {
            return;
        }

        state.locked = true;

        const imagen = state.selectedImage;
        const palabra = state.selectedWord;

        const correcto = imagen.item.id_word === palabra.item.id_word;

        registrarResultado(imagen.item.id_word, correcto);

        if (correcto) {

            imagen.el.classList.remove("is-selected");
            palabra.el.classList.remove("is-selected");

            imagen.el.classList.add("is-matched");
            palabra.el.classList.add("is-matched");

            state.matched += 1;
            updateTrail();

            state.selectedImage = null;
            state.selectedWord = null;
            state.locked = false;

            if (state.matched >= PALABRAS.length) {

                if (state.ronda >= MAX_RONDAS) {

                    state.terminado = true;

                    els.feedback.textContent = "¡COMPLETASTE EL JUEGO! 🎉";
                    els.feedback.className = "feedback is-success";

                } else {

                    els.feedback.textContent = "¡MUY BIEN! 🎉";
                    els.feedback.className = "feedback is-success";

                    state.ronda += 1;

                    setTimeout(iniciarRonda, 1300);

                }

            }

        } else {

            imagen.el.classList.add("is-wrong");
            palabra.el.classList.add("is-wrong");

            els.feedback.textContent = "PROBEMOS DE NUEVO";
            els.feedback.className = "feedback is-retry";

            setTimeout(() => {

                imagen.el.classList.remove("is-wrong");
                palabra.el.classList.remove("is-wrong");

                els.feedback.textContent = "";
                els.feedback.className = "feedback";

                clearSelection();
                state.locked = false;

            }, 900);

        }

    }


    function onSelect(tipo, el, item) {

        if (state.locked || el.classList.contains("is-matched")) {
            return;
        }

        const actual = tipo === "imagen" ? state.selectedImage : state.selectedWord;

        // Tocar de nuevo lo mismo lo deselecciona.
        if (actual && actual.el === el) {
            el.classList.remove("is-selected");

            if (tipo === "imagen") {
                state.selectedImage = null;
            } else {
                state.selectedWord = null;
            }

            return;
        }

        if (actual) {
            actual.el.classList.remove("is-selected");
        }

        el.classList.add("is-selected");

        if (tipo === "imagen") {
            state.selectedImage = { el, item };
        } else {
            state.selectedWord = { el, item };
        }

        evaluarPar();

    }


    function crearItemImagen(item) {

        const btn = document.createElement("button");
        btn.type = "button";
        btn.className = "unir-item unir-item--image";

        btn.innerHTML = `
            <img
                src="${IMG_BASE}${item.image_file}"
                alt="${item.word}"
                class="unir-item__img"
            >
        `;

        btn.addEventListener("click", () => onSelect("imagen", btn, item));

        return btn;
    }


    function crearItemPalabra(item) {

        const btn = document.createElement("button");
        btn.type = "button";
        btn.className = "unir-item unir-item--word";

        btn.textContent = item.word;

        btn.addEventListener("click", () => onSelect("palabra", btn, item));

        return btn;
    }


    function iniciarRonda() {

        state.matched = 0;
        state.selectedImage = null;
        state.selectedWord = null;
        state.locked = false;

        els.roundLabel.textContent = `RONDA ${state.ronda} DE ${MAX_RONDAS}`;

        els.feedback.textContent = "";
        els.feedback.className = "feedback";

        els.colImagenes.innerHTML = "";
        els.colPalabras.innerHTML = "";

        const imagenes = shuffle(PALABRAS);
        const palabras = shuffle(PALABRAS);

        imagenes.forEach((item) => {
            els.colImagenes.appendChild(crearItemImagen(item));
        });

        palabras.forEach((item) => {
            els.colPalabras.appendChild(crearItemPalabra(item));
        });

        updateTrail();

    }


    function init() {

        if (!PALABRAS || PALABRAS.length < 2) {
            els.feedback.textContent = "ESTA CATEGORÍA TODAVÍA NO TIENE SUFICIENTES PALABRAS.";
            return;
        }

        buildTrail();
        iniciarRonda();
        initTutorial();

    }


    // ---------- Tutorial (demo animada de cómo se juega) ----------

    const tutorialState = { timer: null };

    const tutEls = {
        tutorial: document.getElementById("tutorial"),
        tutorialImgs: document.getElementById("tutorialImgs"),
        tutorialWords: document.getElementById("tutorialWords"),
        tutorialRepeat: document.getElementById("tutorialRepeat"),
        tutorialNext: document.getElementById("tutorialNext"),
        tutorialClose: document.getElementById("tutorialClose"),
    };


    function clearTutorialTimer() {

        if (tutorialState.timer) {
            clearTimeout(tutorialState.timer);
            tutorialState.timer = null;
        }

    }


    function renderTutorialDemo() {

        clearTutorialTimer();

        tutEls.tutorialImgs.innerHTML = "";
        tutEls.tutorialWords.innerHTML = "";

        const demoItems = PALABRAS.slice(0, 2);

        if (demoItems.length < 2) {
            return;
        }

        const imgBtn = document.createElement("div");
        imgBtn.className = "unir-item unir-item--image";
        imgBtn.innerHTML = `<img src="${IMG_BASE}${demoItems[0].image_file}" alt="" class="unir-item__img">`;

        const imgBtnExtra = document.createElement("div");
        imgBtnExtra.className = "unir-item unir-item--image";
        imgBtnExtra.innerHTML = `<img src="${IMG_BASE}${demoItems[1].image_file}" alt="" class="unir-item__img">`;

        tutEls.tutorialImgs.appendChild(imgBtn);
        tutEls.tutorialImgs.appendChild(imgBtnExtra);

        const wordBtnCorrecta = document.createElement("div");
        wordBtnCorrecta.className = "unir-item unir-item--word";
        wordBtnCorrecta.textContent = demoItems[0].word;

        const wordBtnExtra = document.createElement("div");
        wordBtnExtra.className = "unir-item unir-item--word";
        wordBtnExtra.textContent = demoItems[1].word;

        tutEls.tutorialWords.appendChild(wordBtnExtra);
        tutEls.tutorialWords.appendChild(wordBtnCorrecta);

        // Animación: "toca" la imagen, después la palabra correcta, y quedan emparejadas.
        tutorialState.timer = setTimeout(() => {

            imgBtn.classList.add("is-selected");

            tutorialState.timer = setTimeout(() => {

                wordBtnCorrecta.classList.add("is-selected");

                tutorialState.timer = setTimeout(() => {

                    imgBtn.classList.remove("is-selected");
                    wordBtnCorrecta.classList.remove("is-selected");

                    imgBtn.classList.add("is-matched");
                    wordBtnCorrecta.classList.add("is-matched");

                }, 700);

            }, 900);

        }, 700);

    }


    function showTutorial() {

        tutEls.tutorial.hidden = false;

        requestAnimationFrame(() => {
            tutEls.tutorial.classList.add("tutorial--visible");
        });

        renderTutorialDemo();

    }


    function closeTutorial() {

        clearTutorialTimer();

        tutEls.tutorial.classList.remove("tutorial--visible");

        setTimeout(() => {
            tutEls.tutorial.hidden = true;
        }, 450);

    }


    function repeatTutorial() {
        renderTutorialDemo();
    }


    function initTutorial() {

        if (!tutEls.tutorial) {
            return;
        }

        tutEls.tutorialRepeat.addEventListener("click", (e) => {
            e.preventDefault();
            repeatTutorial();
        });

        tutEls.tutorialNext.addEventListener("click", (e) => {
            e.preventDefault();
            closeTutorial();
        });

        tutEls.tutorialClose.addEventListener("click", (e) => {
            e.preventDefault();
            closeTutorial();
        });

        setTimeout(showTutorial, 700);

    }


    init();

})();