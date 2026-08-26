(function () {

    "use strict";

    const state = {
        index: 0,
        order: [],
        block: [],
        answered: false
    };

    const tutorialState = {
        timer: null
    };

    const els = {
        tutorial:
            document.getElementById("tutorial"),

        tutorialSentence:
            document.getElementById("tutorialSentence"),

        tutorialOptions:
            document.getElementById("tutorialOptions"),

        btnTutorialClose:
            document.getElementById("btnTutorialClose"),

        btnTutorialRepeat:
            document.getElementById("btnTutorialRepeat"),

        btnTutorialNext:
            document.getElementById("btnTutorialNext"),

        gameStep:
            document.getElementById("gameStep"),

        gameTotal:
            document.getElementById("gameTotal"),

        sentenceText:
            document.getElementById("sentenceText"),

        imageOptions:
            document.getElementById("imageOptions"),

        feedback:
            document.getElementById("feedback")
    };

    function shuffle(array) {

        const result = [...array];

        for (
            let i = result.length - 1;
            i > 0;
            i--
        ) {

            const j =
                Math.floor(
                    Math.random() * (i + 1)
                );

            [
                result[i],
                result[j]
            ] = [
                result[j],
                result[i]
            ];
        }

        return result;
    }

    function obtenerOraciones() {

        return ORACIONES.filter(function (oracion) {

            return (
                oracion &&
                oracion.id_sentence &&
                oracion.image_url
            );

        });
    }

    function currentSentence() {

        return state.block[
            state.order[state.index]
        ];
    }

    function actualizarProgresoVisual() {

        els.gameStep.textContent =
            state.index + 1;

        els.gameTotal.textContent =
            state.block.length;
    }

    function renderPregunta() {

        const sentence =
            currentSentence();

        if (!sentence) {
            return;
        }

        actualizarProgresoVisual();

        els.sentenceText.textContent =
            sentence.text.toUpperCase();

    }

    function armarOpciones(sentence) {

        const otras =
            obtenerOraciones()
                .filter(function (oracion) {

                    return (
                        oracion.id_sentence !==
                        sentence.id_sentence
                    );

                });

        const distractores =
            shuffle(otras).slice(0, 2);

        return shuffle([
            sentence,
            ...distractores
        ]);
    }

    function renderOpciones() {

        els.imageOptions.innerHTML = "";

        els.feedback.textContent = "";
        els.feedback.className = "feedback";

        state.answered = false;

        const sentence =
            currentSentence();

        if (!sentence) {
            return;
        }

        const opciones =
            armarOpciones(sentence);

        opciones.forEach(function (opcion) {

            const button =
                document.createElement("button");

            button.type = "button";

            button.className =
                "image-option";

            const img =
                document.createElement("img");

            img.src = opcion.image_url;
            img.alt = opcion.text;

            button.appendChild(img);

            button.addEventListener(
                "click",
                function () {

                    responder(
                        button,
                        opcion.id_sentence ===
                            sentence.id_sentence,
                        sentence.id_sentence
                    );

                }
            );

            els.imageOptions.appendChild(button);
        });
    }

    function responder(
        button,
        correcto,
        idSentence
    ) {

        if (state.answered) {
            return;
        }

        state.answered = true;

        registrarResultado(
            idSentence,
            correcto
        );

        const buttons =
            [
                ...els.imageOptions.children
            ];

        buttons.forEach(function (item) {

            item.disabled = true;

        });

        if (correcto) {

            button.classList.add(
                "is-correct"
            );

            els.feedback.textContent =
                "¡MUY BIEN!";

            els.feedback.classList.add(
                "is-success"
            );

            setTimeout(
                avanzar,
                850
            );

        } else {

            button.classList.add(
                "is-wrong"
            );

            els.feedback.textContent =
                "PROBÁ DE NUEVO";

            els.feedback.classList.add(
                "is-retry"
            );

            setTimeout(
                function () {

                    button.classList.remove(
                        "is-wrong"
                    );

                    buttons.forEach(function (item) {

                        item.disabled = false;

                    });

                    els.feedback.textContent = "";

                    els.feedback.className =
                        "feedback";

                    state.answered = false;

                },
                900
            );

        }
    }

    function registrarResultado(
        idSentence,
        correcto
    ) {

        fetch(
            URL_REGISTRAR_PROGRESO,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    id_sentence: idSentence,
                    correcto: correcto,
                    juego: 2
                })
            }
        )
        .catch(function (error) {

            console.error(
                "Error al registrar resultado:",
                error
            );

        });
    }

    function avanzar() {

        if (
            state.index <
            state.block.length - 1
        ) {

            state.index++;

            renderPregunta();
            renderOpciones();

            return;
        }

        finalizarJuego2();
    }

    function finalizarJuego2() {

        els.feedback.textContent =
            "¡TERMINASTE!";

        els.feedback.className =
            "feedback is-success";

        els.imageOptions.innerHTML = "";

        fetch(
            URL_COMPLETAR_JUEGO_2,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                }
            }
        )
        .then(function (response) {

            if (!response.ok) {

                throw new Error(
                    "No se pudo finalizar el Juego 2"
                );
            }

            return response.json();

        })
        .then(function (data) {

            if (
                data &&
                data.ok &&
                data.siguiente
            ) {

                window.location.assign(
                    data.siguiente
                );

                return;
            }

            throw new Error(
                "El backend no indicó el siguiente paso"
            );

        })
        .catch(function (error) {

            console.error(
                "Error al finalizar el Juego 2:",
                error
            );

            els.feedback.textContent =
                "OCURRIÓ UN ERROR";

            els.feedback.className =
                "feedback is-retry";

        });
    }

    function crearTutorial() {

        els.tutorialOptions.innerHTML = "";

        const sentence =
            state.block[0];

        if (!sentence) {
            return;
        }

        els.tutorialSentence.textContent =
            sentence.text.toUpperCase();

        const opciones =
            armarOpciones(sentence);

        opciones.forEach(function (opcion) {

            const option =
                document.createElement("div");

            option.className =
                "tutorial-image-option";

            const img =
                document.createElement("img");

            img.src = opcion.image_url;
            img.alt = opcion.text;

            option.appendChild(img);

            option.dataset.correct =
                opcion.id_sentence ===
                sentence.id_sentence
                    ? "true"
                    : "false";

            els.tutorialOptions.appendChild(
                option
            );

        });

        const correcta =
            [
                ...els.tutorialOptions.children
            ].find(function (option) {

                return (
                    option.dataset.correct ===
                    "true"
                );

            });

        if (!correcta) {
            return;
        }

        tutorialState.timer =
            setTimeout(
                function () {

                    correcta.classList.add(
                        "is-highlighted"
                    );

                    tutorialState.timer =
                        setTimeout(
                            function () {

                                correcta.classList.remove(
                                    "is-highlighted"
                                );

                                correcta.classList.add(
                                    "is-success"
                                );

                            },
                            1500
                        );

                },
                600
            );
    }

    function mostrarTutorial() {

        if (!els.tutorial) {
            return;
        }

        crearTutorial();

        els.tutorial.hidden = false;

        requestAnimationFrame(
            function () {

                els.tutorial.classList.add(
                    "is-visible"
                );

            }
        );
    }

    function limpiarTutorial() {

        clearTimeout(
            tutorialState.timer
        );

    }

    function cerrarTutorial() {

        limpiarTutorial();

        els.tutorial.classList.remove(
            "is-visible"
        );

        setTimeout(
            function () {

                els.tutorial.hidden = true;

            },
            300
        );
    }

    function repetirTutorial() {

        limpiarTutorial();

        crearTutorial();
    }

    function iniciarJuego() {

        const oraciones =
            obtenerOraciones();

        if (oraciones.length < 3) {

            els.sentenceText.textContent =
                "NO HAY SUFICIENTES ORACIONES.";

            return;
        }

        state.block =
            oraciones.slice(0, 3);

        state.order =
            shuffle(
                state.block.map(
                    function (_, index) {
                        return index;
                    }
                )
            );

        state.index = 0;

        renderPregunta();
        renderOpciones();

        setTimeout(
            mostrarTutorial,
            500
        );
    }

    function configurarEventos() {

        els.btnTutorialClose.addEventListener(
            "click",
            cerrarTutorial
        );

        els.btnTutorialRepeat.addEventListener(
            "click",
            repetirTutorial
        );

        els.btnTutorialNext.addEventListener(
            "click",
            cerrarTutorial
        );

    }

    configurarEventos();
    iniciarJuego();

})();