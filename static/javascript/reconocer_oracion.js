(function () {

"use strict";

const state = {
    sentenceIndex: 0,
    visited: new Set()
};

const elements = {
    image:
        document.getElementById("sentenceImage"),

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

const AUDIO_PALABRAS_BASE =
    "/static/audio/palabras/";

const AUDIO_ORACIONES_BASE =
    "/static/audio/oraciones/";

function normalizeAudioName(text) {

    return String(text || "")
        .toLowerCase()
        .normalize("NFD")
        .replace(/[\u0300-\u036f]/g, "")
        .replace(/\s+/g, "_");

}

function playAudio(audioElement, src) {

    if (!audioElement || !src) {
        return;
    }

    try {

        audioElement.pause();
        audioElement.currentTime = 0;
        audioElement.src = src;

        const promise = audioElement.play();

        if (
            promise &&
            typeof promise.catch === "function"
        ) {
            promise.catch(function () {});
        }

    } catch (error) {

        console.error(
            "No se pudo reproducir el audio:",
            error
        );

    }

}

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

function getWords(item) {

    if (
        item &&
        Array.isArray(item.words)
    ) {
        return item.words;
    }

    return [];

}

function getWordText(word) {

    if (!word) {
        return "";
    }

    if (typeof word === "string") {
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

function getWordAudio(word) {

    if (!word) {
        return "";
    }

    if (word.audio_url) {
        return word.audio_url;
    }

    if (word.word_audio_url) {
        return word.word_audio_url;
    }

    const text = getWordText(word);

    if (!text) {
        return "";
    }

    return (
        AUDIO_PALABRAS_BASE +
        normalizeAudioName(text) +
        ".mp3"
    );

}

function getSentenceAudio(item) {

    if (!item) {
        return "";
    }

    if (item.audio_url) {
        return item.audio_url;
    }

    if (item.sentence_audio_url) {
        return item.sentence_audio_url;
    }

    if (item.audio_file) {
        return (
            AUDIO_ORACIONES_BASE +
            item.audio_file
        );
    }

    const sentence = getSentence(item);

    if (!sentence) {
        return "";
    }

    return (
        AUDIO_ORACIONES_BASE +
        normalizeAudioName(sentence) +
        ".mp3"
    );

}

function renderProgress() {

    if (!elements.progress) {
        return;
    }

    elements.progress.innerHTML = "";

    ORACIONES.forEach(function (_, index) {

        const dot =
            document.createElement("div");

        dot.className =
            "learning-dot";

        if (
            index ===
            state.sentenceIndex
        ) {
            dot.classList.add("current");
        }

        if (
            state.visited.has(index) &&
            index !== state.sentenceIndex
        ) {
            dot.classList.add("done");
        }

        elements.progress.appendChild(dot);

    });

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

function renderImage(item) {

    if (!elements.image) {
        return;
    }

    if (
        item &&
        item.image_url
    ) {

        elements.image.src =
            item.image_url;

        elements.image.alt =
            getSentence(item);

        elements.image.style.display =
            "block";

        return;

    }

    elements.image.removeAttribute("src");

    elements.image.alt =
        "No hay imagen disponible";

    elements.image.style.display =
        "none";

}

function renderWords(item) {

    if (!elements.sentenceWords) {
        return;
    }

    elements.sentenceWords.innerHTML = "";

    const words =
        getWords(item);

    words.forEach(function (word) {

        const text =
            getWordText(word);

        if (!text) {
            return;
        }

        const card =
            document.createElement("div");

        card.className =
            "sentence-word-card";

        const wordText =
            document.createElement("span");

        wordText.className =
            "sentence-word-text";

        wordText.textContent =
            text.toUpperCase();

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

    });

}

function ocultarBotonVideo() {

    if (!elements.videoPlay) {
        return;
    }

    elements.videoPlay.style.display =
        "none";

}

function mostrarBotonVideo() {

    if (!elements.videoPlay) {
        return;
    }

    elements.videoPlay.style.display =
        "grid";

}

function renderVideo(item) {

    if (!elements.video) {
        return;
    }

    const videoFile =
        item &&
        item.lsa_video_file;

    if (!videoFile) {

        elements.video.pause();

        elements.video.removeAttribute(
            "src"
        );

        elements.video.load();

        elements.video.hidden =
            true;

        ocultarBotonVideo();

        if (elements.videoPlaceholder) {
            elements.videoPlaceholder.hidden =
                false;
        }

        return;
    }

    let videoUrl = "";

    if (item.lsa_video_url) {

        videoUrl =
            item.lsa_video_url;

    } else {

        videoUrl =
            "/static/videos/lsa/sentences/" +
            videoFile;

    }

    elements.video.pause();

    elements.video.src =
        videoUrl;

    elements.video.hidden =
        false;

    mostrarBotonVideo();

    if (elements.videoPlaceholder) {
        elements.videoPlaceholder.hidden =
            true;
    }

    elements.video.load();

}

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

    if (elements.sentence) {

        elements.sentence.textContent =
            sentence.toUpperCase();

    }

    renderImage(item);
    renderWords(item);
    renderVideo(item);

    if (elements.sentenceSound) {

        elements.sentenceSound.setAttribute(
            "aria-label",
            "Escuchar oración " +
            sentence
        );

    }

    state.visited.add(
        state.sentenceIndex
    );

    renderProgress();

}

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

    if (elements.video.paused) {

        const promise =
            elements.video.play();

        if (
            promise &&
            typeof promise.catch === "function"
        ) {

            promise.catch(function (error) {

                console.error(
                    "No se pudo reproducir el video:",
                    error
                );

            });

        }

    } else {

        elements.video.pause();

    }

}

function iniciarJuegoOraciones() {

    sessionStorage.setItem(
        "oracionesReconocidas",
        JSON.stringify(ORACIONES)
    );

    window.location.href =
        URL_JUEGO_ORACIONES;

}

function nextSentence() {

    if (
        state.sentenceIndex <
        ORACIONES.length - 1
    ) {

        state.sentenceIndex++;

        renderSentence();

        return;
    }

    iniciarJuegoOraciones();

}

function previousSentence() {

    if (
        state.sentenceIndex > 0
    ) {

        state.sentenceIndex--;

        renderSentence();

    }

}

function init() {

    if (
        !Array.isArray(ORACIONES) ||
        ORACIONES.length === 0
    ) {
        return;
    }

    renderSentence();

    if (elements.next) {

        elements.next.addEventListener(
            "click",
            nextSentence
        );

    }

    if (elements.prev) {

        elements.prev.addEventListener(
            "click",
            previousSentence
        );

    }

    if (elements.videoPlay) {

        elements.videoPlay.addEventListener(
            "click",
            reproducirVideo
        );

    }

    if (elements.video) {

        elements.video.addEventListener(
            "play",
            function () {

                ocultarBotonVideo();

            }
        );

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

        elements.video.addEventListener(
            "ended",
            function () {

                mostrarBotonVideo();

            }
        );

    }

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

init();


})();
