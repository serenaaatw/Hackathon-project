(function () {

    const state = {
        wordIndex: 0,
        visited: new Set()
    };


    const elements = {

        video: document.getElementById("lsaVideo"),

        videoPlaceholder:
            document.getElementById("videoPlaceholder"),

        image:
            document.getElementById("wordImage"),

        word:
            document.getElementById("wordText"),

        progress:
            document.getElementById("learningProgress"),

        next:
            document.getElementById("btnNext"),

        prev:
            document.getElementById("btnPrev")

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

        const item =
            PALABRAS[state.wordIndex];


        if (!item) {
            return;
        }


        // IMAGEN

        elements.image.src =
            IMG_BASE + item.image_file;

        elements.image.alt =
            item.word;


        // PALABRA

        elements.word.textContent =
            item.word.toUpperCase();


        // VIDEO LSA

        if (item.lsa_video_file) {

            elements.video.src =
                VIDEO_BASE + item.lsa_video_file;

            elements.video.hidden = false;

            elements.videoPlaceholder.hidden = true;

            elements.video.load();

        } else {

            elements.video.removeAttribute("src");

            elements.video.hidden = true;

            elements.videoPlaceholder.hidden = false;

        }


        // GUARDAR COMO VISTA

        state.visited.add(
            state.wordIndex
        );


        renderProgress();

    }

    function nextWord() {

        if (
            state.wordIndex <
            PALABRAS.length - 1
        ) {

            state.wordIndex++;

            renderWord();

        } else {

            // Terminó todos los conceptos.
            // Continúa automáticamente al juego.

            window.location.href =
                URL_JUEGO;

        }

    }



    function previousWord() {

        if (state.wordIndex > 0) {

            state.wordIndex--;

            renderWord();

        }

    }

    function init() {

        if (
            !PALABRAS ||
            PALABRAS.length === 0
        ) {

            return;

        }


        renderWord();


        elements.next.addEventListener(
            "click",
            nextWord
        );


        // BOTÓN <

        elements.prev.addEventListener(
            "click",
            previousWord
        );

    }


    init();

})();