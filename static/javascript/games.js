(function () {

    const state = {
        mode: "A",
        order: [],
        index: 0,
        answered: false
    };

    const tutorialState = {
        active: false,
        timer: null,
        mode: "A"
    };

    const els = {

        trail: document.getElementById("trail"),

        promptImageCard:
            document.getElementById("promptImageCard"),

        promptVideoCard:
            document.getElementById("promptVideoCard"),

        promptSticker:
            document.getElementById("promptSticker"),

        instruction:
            document.getElementById("instruction"),

        options:
            document.getElementById("options"),

        feedback:
            document.getElementById("feedback"),

        lsaVideo:
            document.getElementById("lsaVideo"),

        videoPlaceholder:
            document.getElementById("videoPlaceholder"),

        tutorial:
            document.getElementById("tutorial"),

        tutorialContent:
            document.getElementById("tutorialContent"),

        tutorialImage:
            document.getElementById("tutorialImage"),

        tutorialOptions:
            document.getElementById("tutorialOptions"),

        tutorialRepeat:
            document.getElementById("tutorialRepeat"),

        tutorialNext:
            document.getElementById("tutorialNext"),

        tutorialClose:
            document.getElementById("tutorialClose"),

        tutorialDots:
            document.querySelectorAll(".tutorial-dot")

    };


    function shuffle(arr) {

        const a = [...arr];

        for (let i = a.length - 1; i > 0; i--) {

            const j =
                Math.floor(
                    Math.random() * (i + 1)
                );

            [a[i], a[j]] =
                [a[j], a[i]];

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


    function currentWord() {

        return PALABRAS[
            state.order[state.index]
        ];

    }


    function buildTrail() {

        els.trail.innerHTML = "";

        PALABRAS.forEach(() => {

            const dot =
                document.createElement("div");

            dot.className =
                "trail__step";

            els.trail.appendChild(dot);

        });

    }


    function updateTrail() {

        [...els.trail.children].forEach(
            (dot, i) => {

                dot.classList.toggle(
                    "is-done",
                    i < state.index
                );

                dot.classList.toggle(
                    "is-current",
                    i === state.index
                );

            }
        );

    }


    function renderPrompt() {

        const item = currentWord();

        if (!item) return;


        if (state.mode === "A") {

            els.promptImageCard.hidden = false;
            els.promptVideoCard.hidden = true;

            els.promptSticker.innerHTML = `
                <img
                    src="${IMG_BASE}${item.image_file}"
                    alt="${item.word}"
                    class="prompt-img"
                >
            `;

            els.instruction.textContent =
                "TOCÁ LA PALABRA QUE CORRESPONDE";

        } else {

            els.promptImageCard.hidden = true;
            els.promptVideoCard.hidden = false;

            els.instruction.textContent =
                "MIRÁ LA SEÑA Y TOCÁ LA IMAGEN QUE CORRESPONDE";

            renderLSAVideo(item);

        }

    }


    function renderLSAVideo(item) {

        if (!els.lsaVideo || !els.videoPlaceholder) {
            return;
        }

        const videoFile =
            item.video_file ||
            item.lsa_video ||
            item.video ||
            "";

        if (!videoFile) {

            els.lsaVideo.hidden = true;
            els.videoPlaceholder.hidden = false;

            return;
        }

        els.lsaVideo.src =
            `${VIDEO_BASE}${videoFile}`;

        els.lsaVideo.hidden = false;
        els.videoPlaceholder.hidden = true;

        els.lsaVideo.currentTime = 0;

        els.lsaVideo.play().catch(() => {});

    }


    function renderOptions() {

        els.options.innerHTML = "";

        els.feedback.textContent = "";

        els.feedback.className =
            "feedback";

        state.answered = false;


        const item = currentWord();

        const distractores =
            shuffle(
                PALABRAS.filter(
                    w => w.word !== item.word
                )
            ).slice(0, 2);


        const opciones =
            shuffle([
                item,
                ...distractores
            ]);


        opciones.forEach(opcion => {

            const btn =
                document.createElement("button");

            btn.type = "button";


            if (state.mode === "A") {

                btn.className =
                    "option";

                btn.textContent =
                    opcion.word.toUpperCase();

            } else {

                btn.className =
                    "option option--image";

                btn.innerHTML = `
                    <img
                        src="${IMG_BASE}${opcion.image_file}"
                        alt="${opcion.word}"
                        class="option-img"
                    >
                `;

            }


            btn.addEventListener(
                "click",
                () => {

                    handleAnswer(
                        btn,
                        opcion.word === item.word, item.id_word
                    );

                }
            );


            els.options.appendChild(btn);

        });

    }


    function handleAnswer(btn, correcto, idWord) {

        if (state.answered) {
            return;
        }

        state.answered = true;

        registrarResultado(idWord, correcto);


        [...els.options.children].forEach(
            b => b.classList.add("is-disabled")
        );


        if (correcto) {

            btn.classList.remove(
                "is-disabled"
            );

            btn.classList.add(
                "is-correct"
            );

            els.feedback.textContent =
                "¡MUY BIEN!";

            els.feedback.classList.add(
                "is-success"
            );


            setTimeout(
                nextWord,
                1100
            );

        } else {

            btn.classList.remove(
                "is-disabled"
            );

            btn.classList.add(
                "is-wrong"
            );

            els.feedback.textContent =
                "PROBEMOS DE NUEVO";

            els.feedback.classList.add(
                "is-retry"
            );


            setTimeout(() => {

                [...els.options.children].forEach(
                    b => {

                        b.classList.remove(
                            "is-disabled",
                            "is-wrong"
                        );

                    }
                );

                els.feedback.textContent = "";

                els.feedback.className =
                    "feedback";

                state.answered = false;

            }, 900);

        }

    }


    function nextWord() {

        state.index++;


        if (
            state.index >=
            state.order.length
        ) {

            if (state.mode === "A") {

                state.mode = "B";

                state.order =
                    shuffle(
                        PALABRAS.map(
                            (_, i) => i
                        )
                    );

                state.index = 0;

                updateTrail();
                renderPrompt();
                renderOptions();

                showTutorial("B");

                return;

            } else {

                state.order =
                    shuffle(
                        PALABRAS.map(
                            (_, i) => i
                        )
                    );

                state.index = 0;

            }

        }


        updateTrail();
        renderPrompt();
        renderOptions();

    }


    function clearTutorialTimer() {

        if (tutorialState.timer) {

            clearTimeout(
                tutorialState.timer
            );

            tutorialState.timer = null;

        }

    }


    function clearTutorialAnimation() {

        clearTutorialTimer();

        [...els.tutorialOptions.children].forEach(
            option => {

                option.classList.remove(
                    "tutorial-option--highlight",
                    "tutorial-option--success",
                    "tutorial__fake-word--pop"
                );

            }
        );

    }


    function createTutorialOptions(item) {

        els.tutorialOptions.innerHTML = "";

        const distractores =
            shuffle(
                PALABRAS.filter(
                    w => w.word !== item.word
                )
            ).slice(0, 2);


        const opciones =
            shuffle([
                item,
                ...distractores
            ]);


        opciones.forEach(opcion => {

            const option =
                document.createElement("div");


            option.className =
                "tutorial__fake-word";


            if (tutorialState.mode === "A") {

                option.textContent =
                    opcion.word.toUpperCase();

            } else {

                option.innerHTML = `
                    <img
                        src="${IMG_BASE}${opcion.image_file}"
                        alt=""
                    >
                `;

            }


            option.dataset.correct =
                opcion.word === item.word
                    ? "true"
                    : "false";


            els.tutorialOptions.appendChild(
                option
            );

        });

    }


    function createTutorialVideo(item) {

        const existingVideo =
            document.getElementById(
                "tutorialLsaVideo"
            );

        if (existingVideo) {
            existingVideo.remove();
        }


        const videoFile =
            item.video_file ||
            item.lsa_video ||
            item.video ||
            "";


        if (!videoFile) {
            return;
        }


        const video =
            document.createElement("video");

        video.id =
            "tutorialLsaVideo";

        video.className =
            "tutorial__video";

        video.setAttribute(
            "playsinline",
            ""
        );

        video.muted = true;

        video.autoplay = true;

        video.loop = true;

        video.src =
            `${VIDEO_BASE}${videoFile}`;


        els.tutorialContent.insertBefore(
            video,
            els.tutorialImage
        );


        video.play().catch(() => {});

    }


    function showCorrectAnimation() {

        clearTutorialTimer();

        const opciones =
            [...els.tutorialOptions.children];

        const correcta =
            opciones.find(
                option =>
                    option.dataset.correct === "true"
            );

        if (!correcta) {
            return;
        }

        tutorialState.timer = setTimeout(() => {

            correcta.classList.add(
                "tutorial-option--highlight"
            );

            tutorialState.timer = setTimeout(() => {

                correcta.classList.remove(
                    "tutorial-option--highlight"
                );

                correcta.classList.add(
                    "tutorial-option--success"
                );

                correcta.classList.add(
                    "tutorial__fake-word--pop"
                );

            }, 2500);

        }, 900);

    }


    function renderTutorial() {

        clearTutorialAnimation();


        const item =
            PALABRAS[0];


        if (!item) {
            return;
        }


        els.tutorialImage.src =
            `${IMG_BASE}${item.image_file}`;


        createTutorialOptions(item);


        const existingVideo =
            document.getElementById(
                "tutorialLsaVideo"
            );


        if (existingVideo) {
            existingVideo.remove();
        }


        if (tutorialState.mode === "B") {

            els.tutorialImage.style.display =
                "none";

            createTutorialVideo(item);

        } else {

            els.tutorialImage.style.display =
                "flex";

        }


        showCorrectAnimation();

    }


    function showTutorial(mode) {

        clearTutorialTimer();

        tutorialState.mode = mode;

        tutorialState.active = true;


        els.tutorial.hidden = false;


        requestAnimationFrame(() => {

            els.tutorial.classList.add(
                "tutorial--visible"
            );

        });


        renderTutorial();

    }


    function closeTutorial() {

        clearTutorialTimer();

        tutorialState.active = false;


        els.tutorial.classList.remove(
            "tutorial--visible"
        );


        setTimeout(() => {

            els.tutorial.hidden = true;

        }, 450);

    }


    function repeatTutorial() {

        clearTutorialAnimation();

        renderTutorial();

    }


    function initTutorial() {

        if (!els.tutorial) {
            return;
        }

        if (els.tutorialRepeat) {
            els.tutorialRepeat.addEventListener(
                "click",
                function (e) {
                    e.preventDefault();
                    repeatTutorial();
                }
            );
        }

        if (els.tutorialNext) {
            els.tutorialNext.addEventListener(
                "click",
                function (e) {
                    e.preventDefault();
                    closeTutorial();
                }
            );
        }

        if (els.tutorialClose) {
            els.tutorialClose.addEventListener(
                "click",
                function (e) {
                    e.preventDefault();
                    closeTutorial();
                }
            );
        }

        setTimeout(() => {
            showTutorial("A");
        }, 700);
    }

    function init() {

        if (
            !PALABRAS ||
            PALABRAS.length < 3
        ) {

            els.instruction.textContent =
                "ESTA CATEGORÍA TODAVÍA NO TIENE SUFICIENTES PALABRAS.";

            return;

        }


        state.order =
            shuffle(
                PALABRAS.map(
                    (_, i) => i
                )
            );


        buildTrail();

        updateTrail();

        renderPrompt();

        renderOptions();

        initTutorial();

    }


    init();

})();