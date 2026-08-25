(function () {

    "use strict";


    /* =====================================================
       ESTADO
       ===================================================== */

    const state = {

        wordIndex: 0,

        visited: new Set(),

        detailsOpen: false

    };


    /* =====================================================
       ELEMENTOS DEL HTML
       ===================================================== */

    const elements = {

        video:
            document.getElementById("lsaVideo"),

        videoPlaceholder:
            document.getElementById(
                "videoPlaceholder"
            ),

        image:
            document.getElementById(
                "wordImage"
            ),

        word:
            document.getElementById(
                "wordText"
            ),

        progress:
            document.getElementById(
                "learningProgress"
            ),

        next:
            document.getElementById(
                "btnNext"
            ),

        prev:
            document.getElementById(
                "btnPrev"
            ),

        wordSound:
            document.getElementById(
                "btnWordSound"
            ),

        wordAudio:
            document.getElementById(
                "wordAudio"
            ),

        syllables:
            document.getElementById(
                "wordSyllables"
            ),

        letters:
            document.getElementById(
                "wordLetters"
            ),

        moreLearn:
            document.getElementById(
                "btnMoreLearn"
            ),

        details:
            document.getElementById(
                "learningDetails"
            ),

        closeDetails:
            document.getElementById(
                "btnCloseDetails"
            ),

        step:
            document.getElementById(
                "learningStep"
            ),

        total:
            document.getElementById(
                "learningTotal"
            )

    };


    /* =====================================================
       RUTAS DE AUDIO
       ===================================================== */

    const AUDIO_LETRAS_BASE =
        "/static/audio/letras/";


    const AUDIO_PALABRAS_BASE =
        "/static/audio/palabras/";


    const AUDIO_SILABAS_BASE =
        "/static/audio/silabas/";



    /* =====================================================
       SÍLABAS
       
       No necesitamos modificar la base de datos.
       ===================================================== */

    const SILABAS = {

        "PERRO":
            ["PE", "RRO"],

        "GATO":
            ["GA", "TO"],

        "PEZ":
            ["PEZ"],

        "PÁJARO":
            ["PÁ", "JA", "RO"],

        "PAJARO":
            ["PA", "JA", "RO"],

        "VACA":
            ["VA", "CA"],

        "COMER":
            ["CO", "MER"],

        "DORMIR":
            ["DOR", "MIR"],

        "JUGAR":
            ["JU", "GAR"],

        "CORRER":
            ["CO", "RRER"],

        "NADAR":
            ["NA", "DAR"]

    };



    /* =====================================================
       PROGRESO
       ===================================================== */

    function renderProgress() {

        elements.progress.innerHTML = "";


        PALABRAS.forEach(
            function (_, index) {

                const dot =
                    document.createElement(
                        "div"
                    );


                dot.className =
                    "learning-dot";


                if (
                    index ===
                    state.wordIndex
                ) {

                    dot.classList.add(
                        "current"
                    );

                }


                if (
                    state.visited.has(index) &&
                    index !== state.wordIndex
                ) {

                    dot.classList.add(
                        "done"
                    );

                }


                elements.progress.appendChild(
                    dot
                );

            }
        );


        if (elements.step) {

            elements.step.textContent =
                String(
                    state.wordIndex + 1
                );

        }


        if (elements.total) {

            elements.total.textContent =
                String(
                    PALABRAS.length
                );

        }

    }



    /* =====================================================
       REPRODUCIR AUDIO
       ===================================================== */

    function playAudio(src) {

        if (
            !elements.wordAudio ||
            !src
        ) {

            return;

        }


        try {

            elements.wordAudio.pause();

            elements.wordAudio.currentTime =
                0;

            elements.wordAudio.src =
                src;

            const promise =
                elements.wordAudio.play();


            if (
                promise &&
                typeof promise.catch ===
                "function"
            ) {

                promise.catch(
                    function () {}
                );

            }

        } catch (error) {

            console.error(
                "No se pudo reproducir el audio:",
                error
            );

        }

    }



    /* =====================================================
       NORMALIZAR NOMBRES
       ===================================================== */

    function normalizeAudioName(text) {

        return String(text || "")

            .toLowerCase()

            .normalize("NFD")

            .replace(
                /[\u0300-\u036f]/g,
                ""
            );

    }



    /* =====================================================
       AUDIO DE SÍLABA
       
       Primero busca un MP3 real.

       Ejemplo:
       /static/audio/silabas/pe.mp3

       Si todavía no existe,
       usa la voz del navegador.
       ===================================================== */

    function playSyllable(syllable) {

        const normalized =
            normalizeAudioName(
                syllable
            );


        const src =
            AUDIO_SILABAS_BASE +
            normalized +
            ".mp3";


        const audio =
            new Audio();


        let audioStarted = false;


        audio.preload = "auto";


        audio.addEventListener(
            "canplaythrough",
            function () {

                if (audioStarted) {
                    return;
                }

                audioStarted = true;


                audio.currentTime = 0;


                const promise =
                    audio.play();


                if (
                    promise &&
                    typeof promise.catch ===
                    "function"
                ) {

                    promise.catch(
                        function () {}
                    );

                }

            },
            {
                once: true
            }
        );


        audio.addEventListener(
            "error",
            function () {

                if (audioStarted) {
                    return;
                }


                audioStarted = true;


                speakSyllable(
                    syllable
                );

            },
            {
                once: true
            }
        );


        audio.src = src;

        audio.load();

    }



    /* =====================================================
       VOZ DE RESPALDO
       ===================================================== */

    function speakSyllable(
        syllable
    ) {

        if (
            !window.speechSynthesis
        ) {

            return;

        }


        window.speechSynthesis.cancel();


        const utterance =
            new SpeechSynthesisUtterance(
                syllable
            );


        utterance.lang =
            "es-AR";


        utterance.rate =
            0.78;


        utterance.pitch =
            1.05;


        window.speechSynthesis.speak(
            utterance
        );

    }



    /* =====================================================
       AUDIO DE LA PALABRA
       ===================================================== */

    function getWordAudio(item) {

        if (
            item &&
            item.word_audio_url
        ) {

            return item.word_audio_url;

        }


        if (
            !item ||
            !item.word
        ) {

            return "";

        }


        const normalized =
            normalizeAudioName(
                item.word
            );


        return (
            AUDIO_PALABRAS_BASE +
            normalized +
            ".mp3"
        );

    }



    /* =====================================================
       OBTENER SÍLABAS
       ===================================================== */

    function getSyllables(item) {

        if (
            !item ||
            !item.word
        ) {

            return [];

        }


        const word =
            item.word.toUpperCase();


        if (
            SILABAS[word]
        ) {

            return SILABAS[word];

        }


        if (
            item.syllables
        ) {

            return String(
                item.syllables
            )

                .toUpperCase()

                .split(
                    /[-\s]+/
                )

                .filter(
                    Boolean
                );

        }


        return [word];

    }



    /* =====================================================
       CREAR SÍLABAS
       ===================================================== */

    function renderSyllables(item) {

        if (
            !elements.syllables
        ) {

            return;

        }


        elements.syllables.innerHTML =
            "";


        const syllables =
            getSyllables(item);


        syllables.forEach(
            function (
                syl,
                index
            ) {

                const card =
                    document.createElement(
                        "button"
                    );


                card.type =
                    "button";


                card.className =
                    "syllable-card";


                card.setAttribute(
                    "aria-label",
                    "Escuchar la sílaba " +
                    syl
                );


                /* TEXTO */

                const text =
                    document.createElement(
                        "span"
                    );


                text.className =
                    "syllable-card__text";


                text.textContent =
                    syl;



                /* ICONO */

                const sound =
                    document.createElement(
                        "span"
                    );


                sound.className =
                    "syllable-card__sound";


                sound.setAttribute(
                    "aria-hidden",
                    "true"
                );


                sound.textContent =
                    "🔊";



                card.appendChild(
                    text
                );


                card.appendChild(
                    sound
                );



                /* CLICK */

                card.addEventListener(
                    "click",
                    function () {

                        playSyllable(
                            syl
                        );

                    }
                );


                elements.syllables.appendChild(
                    card
                );



                /* FLECHA */

                if (
                    index <
                    syllables.length - 1
                ) {

                    const arrow =
                        document.createElement(
                            "span"
                        );


                    arrow.className =
                        "syllable-arrow";


                    arrow.setAttribute(
                        "aria-hidden",
                        "true"
                    );


                    arrow.textContent =
                        "→";


                    elements.syllables.appendChild(
                        arrow
                    );

                }

            }
        );

    }



    /* =====================================================
       CREAR LETRAS
       ===================================================== */

    function renderLetters(item) {

        if (
            !elements.letters ||
            !item ||
            !item.word
        ) {

            return;

        }


        elements.letters.innerHTML =
            "";


        const letras =
            item.word
                .toUpperCase()
                .split("");



        letras.forEach(
            function (
                letra,
                index
            ) {

                const card =
                    document.createElement(
                        "button"
                    );


                card.type =
                    "button";


                card.className =
                    "letter-card";



                /* LETRA */

                const letterText =
                    document.createElement(
                        "span"
                    );


                letterText.className =
                    "letter-card__text";


                letterText.textContent =
                    letra;



                /* ICONO */

                const letterSound =
                    document.createElement(
                        "span"
                    );


                letterSound.className =
                    "letter-card__sound";


                letterSound.setAttribute(
                    "aria-hidden",
                    "true"
                );


                letterSound.textContent =
                    "🔊";



                card.appendChild(
                    letterText
                );


                card.appendChild(
                    letterSound
                );



                /* ACCESIBILIDAD */

                card.setAttribute(
                    "aria-label",
                    "Escuchar la letra " +
                    letra
                );



                /* CLICK */

                card.addEventListener(
                    "click",
                    function () {

                        const normalized =
                            normalizeAudioName(
                                letra
                            );


                        const src =
                            AUDIO_LETRAS_BASE +
                            normalized +
                            ".mp3";


                        playAudio(src);

                    }
                );



                elements.letters.appendChild(
                    card
                );



                /* FLECHA */

                if (
                    index <
                    letras.length - 1
                ) {

                    const arrow =
                        document.createElement(
                            "span"
                        );


                    arrow.className =
                        "letter-arrow";


                    arrow.setAttribute(
                        "aria-hidden",
                        "true"
                    );


                    arrow.textContent =
                        "→";


                    elements.letters.appendChild(
                        arrow
                    );

                }

            }
        );

    }



    /* =====================================================
       ABRIR / CERRAR MÁS APRENDER
       ===================================================== */

    function setDetails(open) {

        state.detailsOpen =
            open;


        if (
            !elements.details ||
            !elements.moreLearn
        ) {

            return;

        }


        elements.details.hidden =
            !open;


        elements.moreLearn.setAttribute(
            "aria-expanded",
            open
                ? "true"
                : "false"
        );


        if (open) {

            window.requestAnimationFrame(
                function () {

                    elements.details.scrollIntoView(
                        {
                            behavior:
                                "smooth",

                            block:
                                "nearest"
                        }
                    );

                }
            );

        }

    }



    /* =====================================================
       MOSTRAR PALABRA
       ===================================================== */

    function renderWord() {

        const item =
            PALABRAS[
                state.wordIndex
            ];


        if (!item) {

            return;

        }



        /* IMAGEN */

        elements.image.src =
            IMG_BASE +
            item.image_file;


        elements.image.alt =
            item.word;



        /* PALABRA */

        const currentWord =
            item.word.toUpperCase();


        elements.word.textContent =
            currentWord;



        /* AUDIO DE PALABRA */

        if (
            elements.wordSound
        ) {

            elements.wordSound.setAttribute(
                "aria-label",
                "Escuchar la palabra " +
                currentWord
            );

        }



        /* LETRAS */

        renderLetters(item);



        /* SÍLABAS */

        renderSyllables(item);



        /* VIDEO LSA */

        if (
            item.lsa_video_file
        ) {

            elements.video.src =
                VIDEO_BASE +
                item.lsa_video_file;


            elements.video.hidden =
                false;


            elements.videoPlaceholder.hidden =
                true;


            elements.video.load();

        }

        else {

            elements.video.pause();


            elements.video.removeAttribute(
                "src"
            );


            elements.video.load();


            elements.video.hidden =
                true;


            elements.videoPlaceholder.hidden =
                false;

        }



        /* PROGRESO */

        state.visited.add(
            state.wordIndex
        );


        renderProgress();



        /*
         * Cada palabra comienza
         * nuevamente cerrada.
         */

        setDetails(true);

    }



    /* =====================================================
       INICIAR EJERCICIOS
       ===================================================== */

    function iniciarEjercicios() {

        fetch(
            URL_INICIAR_EJERCICIOS,
            {
                method:
                    "POST",

                headers:
                    {
                        "Content-Type":
                            "application/json"
                    }
            }
        )

            .then(
                function (response) {

                    if (
                        !response.ok
                    ) {

                        throw new Error(
                            "No se pudieron iniciar los ejercicios"
                        );

                    }


                    return response.json();

                }
            )

            .then(
                function (data) {

                    if (
                        data &&
                        data.ok &&
                        Number(
                            data.juego_actual
                        ) === 1
                    ) {

                        window.location.assign(
                            "/juego/1"
                        );

                        return;

                    }


                    throw new Error(
                        "El backend no inició el Juego 1"
                    );

                }
            )

            .catch(
                function (error) {

                    console.error(
                        "Error al iniciar el Juego 1:",
                        error
                    );

                }
            );

    }



    /* =====================================================
       SIGUIENTE PALABRA
       ===================================================== */

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



    /* =====================================================
       PALABRA ANTERIOR
       ===================================================== */

    function previousWord() {

        if (
            state.wordIndex >
            0
        ) {

            state.wordIndex--;


            renderWord();

        }

    }



    /* =====================================================
       INICIAR
       ===================================================== */

    function init() {

        if (
            !Array.isArray(
                PALABRAS
            ) ||
            PALABRAS.length === 0
        ) {

            return;

        }



        renderWord();



        /* SIGUIENTE */

        elements.next.addEventListener(
            "click",
            nextWord
        );



        /* ANTERIOR */

        elements.prev.addEventListener(
            "click",
            previousWord
        );



        /* AUDIO DE LA PALABRA */

        if (
            elements.wordSound
        ) {

            elements.wordSound.addEventListener(
                "click",
                function () {

                    const item =
                        PALABRAS[
                            state.wordIndex
                        ];


                    playAudio(
                        getWordAudio(
                            item
                        )
                    );

                }
            );

        }



        /* MÁS APRENDER */

        if (
            elements.moreLearn
        ) {

            elements.moreLearn.addEventListener(
                "click",
                function () {

                    setDetails(
                        !state.detailsOpen
                    );

                }
            );

        }



        /* CERRAR */

        if (
            elements.closeDetails
        ) {

            elements.closeDetails.addEventListener(
                "click",
                function () {

                    setDetails(
                        false
                    );

                }
            );

        }

    }



    /* =====================================================
       EJECUTAR
       ===================================================== */

    init();

})();