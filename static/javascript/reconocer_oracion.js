(function () {

    "use strict";


    /*
     * ESTADO
     */

    const state = {

        sentenceIndex: 0,

        visited: new Set()

    };


    /*
     * ELEMENTOS HTML
     */

    const elements = {

        video:
            document.getElementById("lsaVideo"),

        videoPlay:
            document.getElementById("btnVideoPlay"),

        videoPlaceholder:
            document.getElementById("videoPlaceholder"),

        sentence:
            document.getElementById("sentenceText"),

        sentenceWords:
            document.getElementById("sentenceWords"),

        sentenceSound:
            document.getElementById("btnSentenceSound"),

        sentenceAudio:
            document.getElementById("sentenceAudio"),

        wordAudio:
            document.getElementById("wordAudio"),

        progress:
            document.getElementById("learningProgress"),

        next:
            document.getElementById("btnNext"),

        prev:
            document.getElementById("btnPrev"),

        step:
            document.getElementById("learningStep"),

        total:
            document.getElementById("learningTotal")

    };


    /*
     * RUTAS DE AUDIO
     */

    const AUDIO_PALABRAS_BASE =
        "/static/audio/palabras/";


    const AUDIO_ORACIONES_BASE =
        "/static/audio/oraciones/";


    /*
     * NORMALIZAR NOMBRE
     *
     * Ejemplo:
     *
     * "PÁJARO" -> "pajaro"
     * "EL PERRO COME" -> "el_perro_come"
     */

    function normalizeAudioName(text) {

        return String(text || "")

            .toLowerCase()

            .normalize("NFD")

            .replace(
                /[\u0300-\u036f]/g,
                ""
            )

            .replace(
                /\s+/g,
                "_"
            );

    }


    /*
     * REPRODUCIR AUDIO
     */

    function playAudio(
        audioElement,
        src
    ) {

        if (
            !audioElement ||
            !src
        ) {

            return;

        }


        try {

            audioElement.pause();

            audioElement.currentTime = 0;

            audioElement.src = src;


            const promise =
                audioElement.play();


            if (
                promise &&
                typeof promise.catch === "function"
            ) {

                promise.catch(
                    function () {}
                );

            }

        }

        catch (error) {

            console.error(
                "No se pudo reproducir el audio:",
                error
            );

        }

    }


    /*
     * OBTENER TEXTO DE LA ORACIÓN
     */

    function getSentence(item) {

        if (!item) {

            return "";

        }


        return (

            item.text ||

            item.sentence ||

            item.oracion ||

            item.oración ||

            item.full_sentence ||

            item.fullSentence ||

            ""

        );

    }


    /*
     * OBTENER PALABRAS
     */

    function getWords(item) {

        if (!item) {

            return [];

        }


        if (
            Array.isArray(item.words) &&
            item.words.length > 0
        ) {

            return item.words;

        }


        return [];

    }


    /*
     * OBTENER TEXTO DE UNA PALABRA
     */

    function getWordText(word) {

        if (!word) {

            return "";

        }


        if (
            typeof word === "string"
        ) {

            return word;

        }


        return (

            word.text ||

            word.word ||

            word.nombre ||

            word.name ||

            ""

        );

    }


    /*
     * OBTENER AUDIO DE PALABRA
     */

    function getWordAudio(word) {

        if (!word) {

            return "";

        }


        /*
         * Si el backend ya mandó
         * la URL, usamos esa.
         */

        if (word.audio_url) {

            return word.audio_url;

        }


        if (word.word_audio_url) {

            return word.word_audio_url;

        }


        const text =
            getWordText(word);


        if (!text) {

            return "";

        }


        return (

            AUDIO_PALABRAS_BASE +

            normalizeAudioName(text) +

            ".mp3"

        );

    }


    /*
     * OBTENER AUDIO DE ORACIÓN
     */

    function getSentenceAudio(item) {

        if (!item) {

            return "";

        }


        /*
         * Si el backend ya manda
         * la URL, usamos esa.
         */

        if (item.audio_url) {

            return item.audio_url;

        }


        if (item.sentence_audio_url) {

            return item.sentence_audio_url;

        }


        /*
         * Si tenemos audio_file
         * usamos ese nombre.
         */

        if (item.audio_file) {

            return (

                AUDIO_ORACIONES_BASE +

                item.audio_file

            );

        }


        /*
         * Si no existe audio_file,
         * generamos el nombre.
         */

        const sentence =
            getSentence(item);


        if (!sentence) {

            return "";

        }


        return (

            AUDIO_ORACIONES_BASE +

            normalizeAudioName(sentence) +

            ".mp3"

        );

    }


    /*
     * PROGRESO
     */

    function renderProgress() {

        if (!elements.progress) {

            return;

        }


        elements.progress.innerHTML = "";


        ORACIONES.forEach(
            function (_, index) {

                const dot =
                    document.createElement("div");


                dot.className =
                    "learning-dot";


                if (
                    index ===
                    state.sentenceIndex
                ) {

                    dot.classList.add(
                        "current"
                    );

                }


                if (
                    state.visited.has(index) &&
                    index !== state.sentenceIndex
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
                    state.sentenceIndex + 1
                );

        }


        if (elements.total) {

            elements.total.textContent =
                String(
                    ORACIONES.length
                );

        }

    }


    /*
     * RENDERIZAR PALABRAS
     *
     * Cada palabra tiene su
     * propio botón de audio.
     */

    function renderWords(item) {

        if (!elements.sentenceWords) {

            return;

        }


        elements.sentenceWords.innerHTML =
            "";


        const words =
            getWords(item);


        words.forEach(
            function (word) {

                const text =
                    getWordText(word);


                if (!text) {

                    return;

                }


                /*
                 * TARJETA
                 */

                const card =
                    document.createElement("div");


                card.className =
                    "sentence-word-card";


                /*
                 * TEXTO
                 */

                const wordText =
                    document.createElement("span");


                wordText.className =
                    "sentence-word-text";


                wordText.textContent =
                    text.toUpperCase();


                /*
                 * BOTÓN AUDIO
                 */

                const button =
                    document.createElement("button");


                button.type =
                    "button";


                button.className =
                    "word-sound";


                button.setAttribute(
                    "aria-label",
                    "Escuchar " + text
                );


                button.innerHTML =
                    "🔊";


                /*
                 * CLICK
                 */

                button.addEventListener(
                    "click",
                    function () {

                        playAudio(

                            elements.wordAudio,

                            getWordAudio(word)

                        );

                    }
                );


                card.appendChild(
                    wordText
                );


                card.appendChild(
                    button
                );


                elements.sentenceWords.appendChild(
                    card
                );

            }
        );

    }


    /*
     * OCULTAR BOTÓN DEL VIDEO
     */

    function ocultarBotonVideo() {

        if (!elements.videoPlay) {

            return;

        }


        elements.videoPlay.style.display =
            "none";

    }


    /*
     * MOSTRAR BOTÓN DEL VIDEO
     */

    function mostrarBotonVideo() {

        if (!elements.videoPlay) {

            return;

        }


        elements.videoPlay.style.display =
            "grid";

    }


    /*
     * RENDERIZAR VIDEO
     *
     * El video corresponde solamente
     * a la oración en LSA.
     */

    function renderVideo(item) {

        if (!elements.video) {

            return;

        }


        /*
         * IMPORTANTE:
         *
         * usamos únicamente
         * lsa_video_file.
         */

        const videoFile =
            item &&
            item.lsa_video_file;


        /*
         * NO HAY VIDEO
         */

        if (!videoFile) {

            elements.video.pause();


            elements.video.removeAttribute(
                "src"
            );


            elements.video.load();


            elements.video.hidden =
                true;


            if (elements.videoPlay) {

                elements.videoPlay.style.display =
                    "none";

            }


            if (elements.videoPlaceholder) {

                elements.videoPlaceholder.hidden =
                    false;

            }


            return;

        }


        /*
         * OBTENER URL
         */

        let videoUrl = "";


        /*
         * Primero usamos la URL
         * que viene del backend.
         */

        if (item.lsa_video_url) {

            videoUrl =
                item.lsa_video_url;

        }

        /*
         * Si no viene del backend,
         * usamos la carpeta:
         *
         * static/videos/lsa/oraciones/
         */

        else {

            videoUrl =
                "/static/videos/lsa/oraciones/" +
                videoFile;

        }


        /*
         * DETENER VIDEO ANTERIOR
         */

        elements.video.pause();


        /*
         * CARGAR NUEVO VIDEO
         */

        elements.video.src =
            videoUrl;


        elements.video.hidden =
            false;


        /*
         * Nueva oración:
         * el botón vuelve a aparecer.
         */

        mostrarBotonVideo();


        /*
         * Ocultar placeholder
         */

        if (elements.videoPlaceholder) {

            elements.videoPlaceholder.hidden =
                true;

        }


        /*
         * Cargar video
         */

        elements.video.load();

    }


    /*
     * RENDERIZAR ORACIÓN COMPLETA
     */

    function renderSentence() {

        const item =
            ORACIONES[
                state.sentenceIndex
            ];


        if (!item) {

            return;

        }


        const sentence =
            getSentence(item);


        /*
         * TEXTO ORACIÓN
         */

        if (elements.sentence) {

            elements.sentence.textContent =
                sentence.toUpperCase();

        }


        /*
         * PALABRAS
         */

        renderWords(item);


        /*
         * VIDEO
         */

        renderVideo(item);


        /*
         * BOTÓN DE AUDIO
         */

        if (elements.sentenceSound) {

            elements.sentenceSound.setAttribute(
                "aria-label",
                "Escuchar oración " +
                sentence
            );

        }


        /*
         * MARCAR VISITADA
         */

        state.visited.add(
            state.sentenceIndex
        );


        /*
         * ACTUALIZAR PROGRESO
         */

        renderProgress();

    }


    /*
     * REPRODUCIR VIDEO
     */

    function reproducirVideo() {

        if (!elements.video) {

            return;

        }


        if (
            elements.video.hidden ||
            !elements.video.src
        ) {

            return;

        }


        /*
         * SI ESTÁ PAUSADO
         * → reproducir
         */

        if (elements.video.paused) {

            const promise =
                elements.video.play();


            if (
                promise &&
                typeof promise.catch === "function"
            ) {

                promise.catch(
                    function (error) {

                        console.error(
                            "No se pudo reproducir el video:",
                            error
                        );

                    }
                );

            }

        }

        /*
         * SI ESTÁ REPRODUCIENDO
         * → pausar
         */

        else {

            elements.video.pause();

        }

    }


    /*
     * INICIAR JUEGO DE ORACIONES
     */

    function iniciarJuegoOraciones() {

        /*
         * Guardamos las oraciones
         * reconocidas para que el juego
         * pueda utilizarlas.
         */

        sessionStorage.setItem(
            "oracionesReconocidas",
            JSON.stringify(ORACIONES)
        );


        /*
         * Cuando exista la ruta:
         *
         * /oraciones/juego/1
         *
         * se podrá utilizar directamente.
         */

        window.location.href =
            URL_JUEGO_ORACIONES;

    }


    /*
     * SIGUIENTE ORACIÓN
     */

    function nextSentence() {

        if (
            state.sentenceIndex <
            ORACIONES.length - 1
        ) {

            state.sentenceIndex++;

            renderSentence();

            return;

        }


        /*
         * Ya terminó el reconocimiento.
         */

        iniciarJuegoOraciones();

    }


    /*
     * ORACIÓN ANTERIOR
     */

    function previousSentence() {

        if (
            state.sentenceIndex > 0
        ) {

            state.sentenceIndex--;

            renderSentence();

        }

    }


    /*
     * INICIALIZACIÓN
     */

    function init() {

        if (
            !Array.isArray(ORACIONES) ||
            ORACIONES.length === 0
        ) {

            return;

        }


        /*
         * Cargar primera oración
         */

        renderSentence();


        /*
         * SIGUIENTE
         */

        if (elements.next) {

            elements.next.addEventListener(
                "click",
                nextSentence
            );

        }


        /*
         * ANTERIOR
         */

        if (elements.prev) {

            elements.prev.addEventListener(
                "click",
                previousSentence
            );

        }


        /*
         * BOTÓN VIDEO
         */

        if (elements.videoPlay) {

            elements.videoPlay.addEventListener(
                "click",
                reproducirVideo
            );

        }


        /*
         * CUANDO EL VIDEO EMPIEZA
         *
         * → esconder botón
         */

        if (elements.video) {

            elements.video.addEventListener(
                "play",
                function () {

                    ocultarBotonVideo();

                }
            );


            /*
             * CUANDO SE PAUSA
             *
             * → mostrar botón
             */

            elements.video.addEventListener(
                "pause",
                function () {

                    if (
                        !elements.video.ended
                    ) {

                        mostrarBotonVideo();

                    }

                }
            );


            /*
             * CUANDO TERMINA
             *
             * → mostrar botón
             */

            elements.video.addEventListener(
                "ended",
                function () {

                    mostrarBotonVideo();

                }
            );

        }


        /*
         * ORACIÓN COMPLETA
         */

        if (elements.sentenceSound) {

            elements.sentenceSound.addEventListener(
                "click",
                function () {

                    const item =
                        ORACIONES[
                            state.sentenceIndex
                        ];


                    playAudio(

                        elements.sentenceAudio,

                        getSentenceAudio(item)

                    );

                }
            );

        }

    }


    /*
     * ARRANCAR
     */

    init();


})();