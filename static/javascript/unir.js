(function () {

    "use strict";

    const MAX_RONDAS = 3;
    const PALABRAS_POR_RONDA = 3;
    const NUMERO_JUEGO = 2;

    const state = {
        ronda: 1,
        matched: 0,
        palabrasRonda: [],
        selectedImage: null,
        selectedWord: null,
        locked: false,
        terminado: false
    };

    const els = {
        trail: document.getElementById("trail"),
        roundLabel: document.getElementById("roundLabel"),
        colImagenes: document.getElementById("colImagenes"),
        colPalabras: document.getElementById("colPalabras"),
        feedback: document.getElementById("feedback")
    };

    function shuffle(array) {

        const copia = [...array];

        for (
            let i = copia.length - 1;
            i > 0;
            i--
        ) {

            const j = Math.floor(
                Math.random() * (i + 1)
            );

            [
                copia[i],
                copia[j]
            ] = [
                copia[j],
                copia[i]
            ];
        }

        return copia;
    }

    function obtenerIdWord(item) {

        return (
            item.id_word ??
            item.idWord ??
            item.id
        );
    }

    function registrarResultado(
        idWord,
        correcto
    ) {

        if (!idWord) {
            return;
        }

        fetch(
            "/juego/registrar-resultado",
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({
                    id_word: idWord,
                    correcto: correcto
                })
            }
        )
        .catch(error => {

            console.warn(
                "Error guardando progreso:",
                error
            );

        });
    }

    function completarJuego() {

        fetch(
            "/juego/completar",
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({
                    numero_juego: NUMERO_JUEGO
                })
            }
        )
        .then(response => {

            if (!response.ok) {

                throw new Error(
                    "No se pudo completar el juego."
                );

            }

            return response.json();

        })
        .then(data => {

            if (!data.ok) {
                return;
            }

            window.location.href =
                "/juego/3";

        })
        .catch(error => {

            console.warn(
                "Error completando juego:",
                error
            );

        });
    }

    function buildTrail() {

        if (!els.trail) {
            return;
        }

        els.trail.innerHTML = "";

        for (
            let i = 0;
            i < PALABRAS_POR_RONDA;
            i++
        ) {

            const dot =
                document.createElement(
                    "div"
                );

            dot.className =
                "trail__step";

            els.trail.appendChild(
                dot
            );
        }
    }

    function updateTrail() {

        if (!els.trail) {
            return;
        }

        [
            ...els.trail.children
        ].forEach(
            (dot, index) => {

                dot.classList.toggle(
                    "is-done",
                    index < state.matched
                );

            }
        );
    }

    function clearSelection() {

        if (state.selectedImage) {

            state.selectedImage.el
                .classList.remove(
                    "is-selected"
                );
        }

        if (state.selectedWord) {

            state.selectedWord.el
                .classList.remove(
                    "is-selected"
                );
        }

        state.selectedImage = null;
        state.selectedWord = null;
    }

    function evaluarPar() {

        if (
            !state.selectedImage ||
            !state.selectedWord
        ) {

            return;
        }

        state.locked = true;

        const imagen =
            state.selectedImage;

        const palabra =
            state.selectedWord;

        const correcto =
            obtenerIdWord(
                imagen.item
            ) ===
            obtenerIdWord(
                palabra.item
            );

        registrarResultado(
            obtenerIdWord(
                imagen.item
            ),
            correcto
        );

        if (correcto) {

            imagen.el.classList.remove(
                "is-selected"
            );

            palabra.el.classList.remove(
                "is-selected"
            );

            imagen.el.classList.add(
                "is-matched"
            );

            palabra.el.classList.add(
                "is-matched"
            );

            state.matched += 1;

            updateTrail();

            state.selectedImage = null;
            state.selectedWord = null;
            state.locked = false;

            if (
                state.matched >=
                state.palabrasRonda.length
            ) {

                finalizarRonda();

            }

            return;
        }

        imagen.el.classList.add(
            "is-wrong"
        );

        palabra.el.classList.add(
            "is-wrong"
        );

        if (els.feedback) {

            els.feedback.textContent =
                "PROBÁ DE NUEVO";

            els.feedback.className =
                "feedback is-retry";
        }

        setTimeout(
            () => {

                imagen.el.classList.remove(
                    "is-wrong"
                );

                palabra.el.classList.remove(
                    "is-wrong"
                );

                if (els.feedback) {

                    els.feedback.textContent =
                        "";

                    els.feedback.className =
                        "feedback";
                }

                clearSelection();

                state.locked = false;

            },
            900
        );
    }

    function onSelect(
        tipo,
        el,
        item
    ) {

        if (
            state.locked ||
            el.classList.contains(
                "is-matched"
            )
        ) {

            return;
        }

        const actual =
            tipo === "imagen"
                ? state.selectedImage
                : state.selectedWord;

        if (
            actual &&
            actual.el === el
        ) {

            el.classList.remove(
                "is-selected"
            );

            if (
                tipo === "imagen"
            ) {

                state.selectedImage =
                    null;

            } else {

                state.selectedWord =
                    null;

            }

            return;
        }

        if (actual) {

            actual.el.classList.remove(
                "is-selected"
            );
        }

        el.classList.add(
            "is-selected"
        );

        if (
            tipo === "imagen"
        ) {

            state.selectedImage = {
                el: el,
                item: item
            };

        } else {

            state.selectedWord = {
                el: el,
                item: item
            };
        }

        evaluarPar();
    }

    function crearItemImagen(item) {

        const btn =
            document.createElement(
                "button"
            );

        btn.type = "button";

        btn.className =
            "unir-item unir-item--image";

        btn.innerHTML = `
            <img
                src="${IMG_BASE}${item.image_file}"
                alt="${item.word}"
                class="unir-item__img"
            >
        `;

        btn.addEventListener(
            "click",
            () => {

                onSelect(
                    "imagen",
                    btn,
                    item
                );

            }
        );

        return btn;
    }

    function crearItemPalabra(item) {

        const btn =
            document.createElement(
                "button"
            );

        btn.type = "button";

        btn.className =
            "unir-item unir-item--word";

        btn.textContent =
            item.word;

        btn.addEventListener(
            "click",
            () => {

                onSelect(
                    "palabra",
                    btn,
                    item
                );

            }
        );

        return btn;
    }

    function iniciarRonda() {

        state.matched = 0;
        state.selectedImage = null;
        state.selectedWord = null;
        state.locked = false;

        state.palabrasRonda =
            PALABRAS.slice(
                0,
                PALABRAS_POR_RONDA
            );

        if (els.roundLabel) {

            els.roundLabel.textContent =
                `RONDA ${state.ronda} DE ${MAX_RONDAS}`;

        }

        if (els.feedback) {

            els.feedback.textContent = "";

            els.feedback.className =
                "feedback";
        }

        els.colImagenes.innerHTML = "";
        els.colPalabras.innerHTML = "";

        const imagenes =
            shuffle(
                state.palabrasRonda
            );

        const palabras =
            shuffle(
                state.palabrasRonda
            );

        imagenes.forEach(
            item => {

                els.colImagenes.appendChild(
                    crearItemImagen(item)
                );

            }
        );

        palabras.forEach(
            item => {

                els.colPalabras.appendChild(
                    crearItemPalabra(item)
                );

            }
        );

        updateTrail();
    }

    function finalizarRonda() {

        state.locked = true;

        if (
            state.ronda >=
            MAX_RONDAS
        ) {

            if (els.feedback) {

                els.feedback.textContent =
                    "¡MUY BIEN!";

                els.feedback.className =
                    "feedback is-success";

            }

            setTimeout(
                completarJuego,
                1000
            );

            return;
        }

        if (els.feedback) {

            els.feedback.textContent =
                "¡MUY BIEN!";

            els.feedback.className =
                "feedback is-success";
        }

        setTimeout(
            () => {

                state.ronda += 1;

                iniciarRonda();

            },
            1200
        );
    }

    function finalizarJuego() {

        state.terminado = true;

        if (els.feedback) {

            els.feedback.textContent =
                "¡TERMINASTE!";

            els.feedback.className =
                "feedback is-success";
        }

        if (els.roundLabel) {

            els.roundLabel.textContent =
                "¡MUY BIEN!";

        }
    }

    const tutorialState = {
        timer: null
    };

    const tutEls = {

        tutorial:
            document.getElementById(
                "tutorial"
            ),

        tutorialImgs:
            document.getElementById(
                "tutorialImgs"
            ),

        tutorialWords:
            document.getElementById(
                "tutorialWords"
            ),

        tutorialRepeat:
            document.getElementById(
                "tutorialRepeat"
            ),

        tutorialNext:
            document.getElementById(
                "tutorialNext"
            ),

        tutorialClose:
            document.getElementById(
                "tutorialClose"
            )
    };

    function clearTutorialTimer() {

        if (
            tutorialState.timer
        ) {

            clearTimeout(
                tutorialState.timer
            );

            tutorialState.timer = null;
        }
    }

    function renderTutorialDemo() {

        clearTutorialTimer();

        if (
            !tutEls.tutorialImgs ||
            !tutEls.tutorialWords
        ) {

            return;
        }

        tutEls.tutorialImgs.innerHTML = "";
        tutEls.tutorialWords.innerHTML = "";

        const demoItems =
            PALABRAS.slice(
                0,
                2
            );

        if (
            demoItems.length < 2
        ) {

            return;
        }

        const imgCorrecta =
            document.createElement(
                "div"
            );

        imgCorrecta.className =
            "unir-item unir-item--image";

        imgCorrecta.innerHTML = `
            <img
                src="${IMG_BASE}${demoItems[0].image_file}"
                alt=""
                class="unir-item__img"
            >
        `;

        const imgExtra =
            document.createElement(
                "div"
            );

        imgExtra.className =
            "unir-item unir-item--image";

        imgExtra.innerHTML = `
            <img
                src="${IMG_BASE}${demoItems[1].image_file}"
                alt=""
                class="unir-item__img"
            >
        `;

        tutEls.tutorialImgs.appendChild(
            imgCorrecta
        );

        tutEls.tutorialImgs.appendChild(
            imgExtra
        );

        const palabraExtra =
            document.createElement(
                "div"
            );

        palabraExtra.className =
            "unir-item unir-item--word";

        palabraExtra.textContent =
            demoItems[1].word;

        const palabraCorrecta =
            document.createElement(
                "div"
            );

        palabraCorrecta.className =
            "unir-item unir-item--word";

        palabraCorrecta.textContent =
            demoItems[0].word;

        tutEls.tutorialWords.appendChild(
            palabraExtra
        );

        tutEls.tutorialWords.appendChild(
            palabraCorrecta
        );

        tutorialState.timer =
            setTimeout(
                () => {

                    imgCorrecta.classList.add(
                        "is-selected"
                    );

                    tutorialState.timer =
                        setTimeout(
                            () => {

                                palabraCorrecta
                                    .classList.add(
                                        "is-selected"
                                    );

                                tutorialState.timer =
                                    setTimeout(
                                        () => {

                                            imgCorrecta
                                                .classList
                                                .remove(
                                                    "is-selected"
                                                );

                                            palabraCorrecta
                                                .classList
                                                .remove(
                                                    "is-selected"
                                                );

                                            imgCorrecta
                                                .classList
                                                .add(
                                                    "is-matched"
                                                );

                                            palabraCorrecta
                                                .classList
                                                .add(
                                                    "is-matched"
                                                );

                                        },
                                        700
                                    );

                            },
                            900
                        );

                },
                700
            );
    }

    function showTutorial() {

        if (
            !tutEls.tutorial
        ) {

            return;
        }

        tutEls.tutorial.hidden = false;

        requestAnimationFrame(
            () => {

                tutEls.tutorial.classList.add(
                    "tutorial--visible"
                );

            }
        );

        renderTutorialDemo();
    }

    function closeTutorial() {

        clearTutorialTimer();

        if (
            !tutEls.tutorial
        ) {

            return;
        }

        tutEls.tutorial.classList.remove(
            "tutorial--visible"
        );

        setTimeout(
            () => {

                tutEls.tutorial.hidden = true;

            },
            450
        );
    }

    function repeatTutorial() {

        renderTutorialDemo();
    }

    function initTutorial() {

        if (
            !tutEls.tutorial
        ) {

            return;
        }

        if (
            tutEls.tutorialRepeat
        ) {

            tutEls.tutorialRepeat
                .addEventListener(
                    "click",
                    event => {

                        event.preventDefault();

                        repeatTutorial();

                    }
                );
        }

        if (
            tutEls.tutorialNext
        ) {

            tutEls.tutorialNext
                .addEventListener(
                    "click",
                    event => {

                        event.preventDefault();

                        closeTutorial();

                    }
                );
        }

        if (
            tutEls.tutorialClose
        ) {

            tutEls.tutorialClose
                .addEventListener(
                    "click",
                    event => {

                        event.preventDefault();

                        closeTutorial();

                    }
                );
        }

        setTimeout(
            showTutorial,
            700
        );
    }

    function init() {

        if (
            !Array.isArray(PALABRAS) ||
            PALABRAS.length <
            PALABRAS_POR_RONDA
        ) {

            if (els.feedback) {

                els.feedback.textContent =
                    "NO HAY SUFICIENTES PALABRAS";

            }

            return;
        }

        buildTrail();

        iniciarRonda();

        initTutorial();
    }

    init();

})();