(function () {

    "use strict";

    const state = {
        wordIndex: 0,
        visited: new Set()
    };

    const elements = {
        video: document.getElementById("lsaVideo"),
        videoPlaceholder: document.getElementById("videoPlaceholder"),
        image: document.getElementById("wordImage"),
        word: document.getElementById("wordText"),
        progress: document.getElementById("learningProgress"),
        next: document.getElementById("btnNext"),
        prev: document.getElementById("btnPrev")
    };

    function renderProgress() {

        elements.progress.innerHTML = "";

        PALABRAS.forEach(function (_, index) {

            const dot = document.createElement("div");

            dot.className = "learning-dot";

            if (index === state.wordIndex) {
                dot.classList.add("current");
            }

            if (
                state.visited.has(index) &&
                index !== state.wordIndex
            ) {
                dot.classList.add("done");
            }

            elements.progress.appendChild(dot);

        });

    }

    function renderWord() {

        const item = PALABRAS[state.wordIndex];

        if (!item) {
            return;
        }

        elements.image.src =
            IMG_BASE + item.image_file;

        elements.image.alt =
            item.word;

        elements.word.textContent =
            item.word.toUpperCase();

        if (item.lsa_video_file) {

            elements.video.src =
                VIDEO_BASE + item.lsa_video_file;

            elements.video.hidden = false;
            elements.videoPlaceholder.hidden = true;

            elements.video.load();

        } else {

            elements.video.pause();
            elements.video.removeAttribute("src");
            elements.video.load();

            elements.video.hidden = true;
            elements.videoPlaceholder.hidden = false;

        }

        state.visited.add(
            state.wordIndex
        );

        renderProgress();

    }

    function iniciarEjercicios() {

        fetch(
            "/aprender/iniciar-ejercicios",
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
                    "No se pudieron iniciar los ejercicios"
                );
            }

            return response.json();

        })
        .then(function (data) {

            if (
                data &&
                data.ok &&
                Number(data.juego_actual) === 1
            ) {

                window.location.assign(
                    "/juego/1"
                );

                return;
            }

            throw new Error(
                "El backend no inició el Juego 1"
            );

        })
        .catch(function (error) {

            console.error(
                "Error al iniciar el Juego 1:",
                error
            );

        });

    }

    function nextWord() {

        if (
            state.wordIndex <
            PALABRAS.length - 1
        ) {

            state.wordIndex++;

            renderWord();

            return;
        }

        iniciarEjercicios();

    }

    function previousWord() {

        if (state.wordIndex > 0) {

            state.wordIndex--;

            renderWord();

        }

    }

    function init() {

        if (
            !Array.isArray(PALABRAS) ||
            PALABRAS.length === 0
        ) {

            return;
        }

        renderWord();

        elements.next.addEventListener(
            "click",
            nextWord
        );

        elements.prev.addEventListener(
            "click",
            previousWord
        );

    }

    init();

})();