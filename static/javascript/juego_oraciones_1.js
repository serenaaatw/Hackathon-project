(function () {

    "use strict";

    const state = {
        mode: "A",
        index: 0,
        order: [],
        answered: false,
        block: []
    };

    const tutorialState = {
        timer: null,
        mode: "A"
    };

    const els = {
        tutorial:
            document.getElementById("tutorial"),

        tutorialImage:
            document.getElementById("tutorialImage"),

        tutorialImageContainer:
            document.getElementById("tutorialImageContainer"),

        tutorialVideoContainer:
            document.getElementById("tutorialVideoContainer"),

        tutorialVideo:
            document.getElementById("tutorialVideo"),

        btnTutorialVideoPlay:
            document.getElementById("btnTutorialVideoPlay"),

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

        partIndicator:
            document.getElementById("partIndicator"),

        imageContainer:
            document.getElementById("imageContainer"),

        questionImage:
            document.getElementById("questionImage"),

        videoContainer:
            document.getElementById("videoContainer"),

        questionVideo:
            document.getElementById("questionVideo"),

        btnVideoPlay:
            document.getElementById("btnVideoPlay"),

        questionInstruction:
            document.getElementById("questionInstruction"),

        options:
            document.getElementById("options"),

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

            return oracion &&
                oracion.id_sentence;

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

        els.partIndicator.textContent =
            state.mode === "A"
                ? "PARTE A"
                : "PARTE B";
    }

    function detenerVideo() {

        const video =
            els.questionVideo;

        video.pause();

        video.removeAttribute("src");

        video.load();

        els.btnVideoPlay.textContent = "▶";

        els.btnVideoPlay.hidden = false;
    }

    function cargarVideo(sentence) {

        const video =
            els.questionVideo;

        detenerVideo();

        if (!sentence || !sentence.lsa_video_url) {
            return;
        }

        video.src =
            sentence.lsa_video_url;

        video.load();

        els.btnVideoPlay.hidden = false;
        els.btnVideoPlay.textContent = "▶";
    }

    function renderPregunta() {

        const sentence =
            currentSentence();

        if (!sentence) {
            return;
        }

        actualizarProgresoVisual();

        if (state.mode === "A") {

            detenerVideo();

            els.imageContainer.hidden = false;
            els.videoContainer.hidden = true;

            els.questionImage.src =
                sentence.image_url || "";

            els.questionImage.alt =
                sentence.text || "";

            els.questionInstruction.textContent =
                "TOCÁ LA ORACIÓN QUE CORRESPONDE";

        } else {

            els.imageContainer.hidden = true;
            els.videoContainer.hidden = false;

            els.questionImage.removeAttribute("src");

            els.questionInstruction.textContent =
                "MIRÁ LA SEÑA Y ELEGÍ LA ORACIÓN";

            cargarVideo(sentence);
        }
    }

    function renderOpciones() {

        els.options.innerHTML = "";

        els.feedback.textContent = "";
        els.feedback.className = "feedback";

        state.answered = false;

        const sentence =
            currentSentence();

        if (!sentence) {
            return;
        }

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

        const opciones =
            shuffle([
                sentence,
                ...distractores
            ]);

        opciones.forEach(function (opcion) {

            const button =
                document.createElement("button");

            button.type = "button";

            button.className =
                "sentence-option";

            button.textContent =
                opcion.text.toUpperCase();

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

            els.options.appendChild(button);
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
                ...els.options.children
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

                    els.feedback.textContent =
                        "";

                    els.feedback.className =
                        "feedback";

                    state.answered = false;

                },
                750
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
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({
                    id_sentence:
                        idSentence,

                    correcto:
                        correcto,

                    juego: 1
                })
            }
        )
        .catch(function (error) {

            console.error(
                "Error registrando progreso:",
                error
            );

        });
    }

    function avanzar() {

        state.index++;

        if (
            state.index <
            state.block.length
        ) {

            renderPregunta();
            renderOpciones();

            return;
        }

        if (state.mode === "A") {

            state.mode = "B";
            state.index = 0;

            state.order =
                shuffle(
                    state.block.map(
                        function (_, index) {
                            return index;
                        }
                    )
                );

            renderPregunta();
            renderOpciones();

            setTimeout(
                function () {
                    mostrarTutorial("B");
                },
                350
            );

            return;
        }

        terminarJuego1();
    }

    function terminarJuego1() {

        fetch(
            URL_COMPLETAR_JUEGO,
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({
                    oraciones:
                        state.block.map(
                            function (sentence) {
                                return sentence.id_sentence;
                            }
                        )
                })
            }
        )
        .then(function (response) {

            if (!response.ok) {

                throw new Error(
                    "No se pudo completar el juego"
                );

            }

            return response.json();

        })
        .then(function (data) {

            if (
                data &&
                data.siguiente
            ) {

                window.location.assign(
                    data.siguiente
                );

                return;
            }

            window.location.assign(
                URL_JUEGO_ORACIONES_2
            );

        })
        .catch(function (error) {

            console.error(
                "Error al finalizar Juego 1:",
                error
            );

            window.location.assign(
                URL_JUEGO_ORACIONES_2
            );

        });
    }

    function limpiarTutorial() {

        if (tutorialState.timer) {

            clearTimeout(
                tutorialState.timer
            );

            tutorialState.timer = null;
        }

        els.tutorialOptions.innerHTML = "";

        els.tutorialImage.removeAttribute(
            "src"
        );

        els.tutorialVideo.pause();

        els.tutorialVideo.removeAttribute(
            "src"
        );

        els.tutorialVideo.load();

        els.btnTutorialVideoPlay.hidden = false;

        els.btnTutorialVideoPlay.textContent =
            "▶";
    }

    function crearTutorial(mode) {

        limpiarTutorial();

        tutorialState.mode = mode;

        const sentence =
            state.block[0];

        if (!sentence) {
            return;
        }

        if (mode === "A") {

            els.tutorialImageContainer.hidden = false;
            els.tutorialVideoContainer.hidden = true;

            els.tutorialImage.hidden = false;

            els.tutorialImage.src =
                sentence.image_url || "";

            els.tutorialImage.alt =
                sentence.text || "";

        } else {

            els.tutorialImageContainer.hidden = true;
            els.tutorialVideoContainer.hidden = false;

            els.tutorialImage.hidden = true;

            if (sentence.lsa_video_url) {

                els.tutorialVideo.src =
                    sentence.lsa_video_url;

                els.tutorialVideo.load();

                els.btnTutorialVideoPlay.hidden =
                    false;

                els.btnTutorialVideoPlay.textContent =
                    "▶";
            }
        }

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

        const opciones =
            shuffle([
                sentence,
                ...distractores
            ]);

        opciones.forEach(function (opcion) {

            const option =
                document.createElement("div");

            option.className =
                "tutorial-option";

            option.textContent =
                opcion.text.toUpperCase();

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

    function mostrarTutorial(mode) {

        if (!els.tutorial) {
            return;
        }

        crearTutorial(mode);

        els.tutorial.hidden = false;

        requestAnimationFrame(
            function () {

                els.tutorial.classList.add(
                    "is-visible"
                );

            }
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

        crearTutorial(
            tutorialState.mode
        );
    }

    function iniciarJuego() {

        const oraciones =
            obtenerOraciones();

        if (oraciones.length < 3) {

            els.questionInstruction.textContent =
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
        state.mode = "A";

        renderPregunta();
        renderOpciones();

        setTimeout(
            function () {
                mostrarTutorial("A");
            },
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

        els.btnVideoPlay.addEventListener(
            "click",
            function () {

                const video =
                    els.questionVideo;

                if (video.paused) {

                    video.play()
                        .then(function () {

                            els.btnVideoPlay.hidden =
                                true;

                        })
                        .catch(function () {});

                } else {

                    video.pause();

                    els.btnVideoPlay.hidden =
                        false;

                    els.btnVideoPlay.textContent =
                        "▶";
                }
            }
        );

        els.questionVideo.addEventListener(
            "play",
            function () {

                els.btnVideoPlay.hidden = true;

            }
        );

        els.questionVideo.addEventListener(
            "pause",
            function () {

                els.btnVideoPlay.hidden = false;

                els.btnVideoPlay.textContent =
                    "▶";

            }
        );

        els.questionVideo.addEventListener(
            "ended",
            function () {

                els.btnVideoPlay.hidden = false;

                els.btnVideoPlay.textContent =
                    "↻";

            }
        );

        els.btnTutorialVideoPlay.addEventListener(
            "click",
            function () {

                const video =
                    els.tutorialVideo;

                if (video.paused) {

                    video.play()
                        .then(function () {

                            els.btnTutorialVideoPlay.hidden =
                                true;

                        })
                        .catch(function () {});

                }
            }
        );

        els.tutorialVideo.addEventListener(
            "play",
            function () {

                els.btnTutorialVideoPlay.hidden =
                    true;

            }
        );

        els.tutorialVideo.addEventListener(
            "pause",
            function () {

                if (!els.tutorialVideo.ended) {

                    els.btnTutorialVideoPlay.hidden =
                        false;

                    els.btnTutorialVideoPlay.textContent =
                        "▶";
                }

            }
        );

        els.tutorialVideo.addEventListener(
            "ended",
            function () {

                els.btnTutorialVideoPlay.hidden =
                    false;

                els.btnTutorialVideoPlay.textContent =
                    "↻";

            }
        );
    }

    configurarEventos();
    iniciarJuego();

})();
