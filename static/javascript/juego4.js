document.addEventListener("DOMContentLoaded", () => {

    const juego = document.getElementById("juego4");
    const tutorial = document.getElementById("tutorial");
    const cerrarTutorial = document.getElementById("cerrarTutorial");
    const avanzarTutorial = document.getElementById("avanzarTutorial");
    const btnRepetirTutorial = document.getElementById("repetirTutorial");

    if (!juego) {
        console.error("No se encontró #juego4");
        return;
    }

    const dificultad = parseInt(
        juego.dataset.dificultad || "1"
    );

    const imagen = document.getElementById("imagenPalabra");
    const palabra = document.getElementById("palabra");
    const opciones = document.getElementById("opciones");
    const feedback = document.getElementById("feedback");
    const progreso = document.getElementById("progreso");

    const PALABRAS_JUEGO =
        Array.isArray(window.PALABRAS)
            ? window.PALABRAS
            : [];

    const state = {
        palabras: [],
        indice: 0,
        palabraActual: null,
        posicionesOcultas: [],
        letrasColocadas: [],
        letrasDisponibles: [],
        bloqueado: false
    };

    let tutorialTimer = null;

    function shuffle(array) {

        const copia = [...array];

        for (let i = copia.length - 1; i > 0; i--) {

            const j =
                Math.floor(
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



    function registrarResultado(idWord, correcto) {

        if (!idWord) {
            return Promise.resolve();
        }

        return fetch("/juego/registrar-resultado", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                id_word: idWord,
                correcto: correcto
            })
        })
        .then(response => {

            if (!response.ok) {
                throw new Error(
                    "No se pudo guardar el resultado"
                );
            }

            return response.json();
        })
        .catch(error => {

            console.error(
                "Error al guardar progreso:",
                error
            );

            throw error;
        });
    }

    function completarJuego4() {

        return fetch("/juego/completar", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                numero_juego: 4
            })
        })
        .then(response => {

            if (!response.ok) {

                throw new Error(
                    "No se pudo completar el Juego 4"
                );
            }

            return response.json();
        });
    }

    function procesarDecision(data) {

        if (!data || !data.ok) {

            throw new Error(
                "La decisión no fue confirmada por el servidor"
            );
        }

        const decision =
            data.decision;

        if (decision === "repetir") {

            window.location.href =
                "/aprender";

            return;
        }

        if (decision === "aprender") {

            window.location.href =
                "/aprender";

            return;
        }

        if (decision === "oracion") {

            window.location.href =
                "/oraciones/reconocer";

            return;
        }

        if (
            data.juego_actual !== null &&
            data.juego_actual !== undefined
        ) {

            if (data.juego_actual === 1) {

                window.location.href =
                    "/juego/1";

                return;
            }

            if (data.juego_actual === 2) {

                window.location.href =
                    "/juego/unir";

                return;
            }

            window.location.href =
                `/juego/${data.juego_actual}`;

            return;
        }

        finalizarPantalla();
    }

    function cantidadLetrasOcultas(texto) {

        const longitud = texto.length;

        let cantidad;

        if (dificultad === 1) {

            cantidad = Math.max(
                1,
                Math.floor(longitud * 0.25)
            );

        } else if (dificultad === 2) {

            cantidad = Math.max(
                2,
                Math.floor(longitud * 0.40)
            );

        } else {

            cantidad = Math.max(
                2,
                Math.floor(longitud * 0.55)
            );
        }

        return Math.min(
            cantidad,
            longitud - 1
        );
    }

    function crearPosicionesOcultas(texto) {

        const cantidad =
            cantidadLetrasOcultas(texto);

        const posiciones = Array.from(
            {
                length: texto.length
            },
            (_, index) => index
        );

        return shuffle(posiciones)
            .slice(0, cantidad)
            .sort((a, b) => a - b);
    }

    function crearLetrasDisponibles() {

        const texto =
            state.palabraActual.word.toUpperCase();

        const letrasCorrectas =
            state.posicionesOcultas.map(
                posicion => texto[posicion]
            );

        // OJO: usamos un array, NO un Set. Un Set elimina letras
        // repetidas, y si la palabra tiene una letra que se repite
        // entre los huecos (ej. la R de DORMIR), hace falta un
        // botón por cada hueco aunque la letra sea la misma, o el
        // juego queda imposible de completar.
        const letras =
            [...letrasCorrectas];

        const abecedario =
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

        while (letras.length < 8) {

            const letra =
                abecedario[
                    Math.floor(
                        Math.random() *
                        abecedario.length
                    )
                ];

            letras.push(letra);
        }

        state.letrasDisponibles =
            shuffle(letras);
    }

    function actualizarProgreso() {

        if (!progreso) {
            return;
        }

        progreso.innerHTML = "";

        state.palabras.forEach((_, index) => {

            const punto =
                document.createElement("div");

            punto.className =
                "juego4__progreso-punto";

            if (index < state.indice) {

                punto.classList.add(
                    "completado"
                );
            }

            if (index === state.indice) {

                punto.classList.add(
                    "actual"
                );
            }

            progreso.appendChild(punto);
        });
    }

    function mostrarPalabra() {

        const texto =
            state.palabraActual.word.toUpperCase();

        palabra.innerHTML = "";

        for (
            let i = 0;
            i < texto.length;
            i++
        ) {

            const elemento =
                document.createElement("span");

            elemento.className =
                "juego4__letra";

            if (
                !state.posicionesOcultas.includes(i)
            ) {

                elemento.textContent =
                    texto[i];

            } else {

                const colocada =
                    state.letrasColocadas.find(
                        item =>
                            item.posicion === i
                    );

                elemento.classList.add("oculta");

                elemento.dataset.posicion = i;

                if (colocada) {

                    elemento.textContent =
                        colocada.letra;

                    elemento.classList.add(
                        "colocada"
                    );

                } else {

                    elemento.textContent = "_";
                }

                elemento.addEventListener(
                    "click",
                    () => {
                        eliminarLetra(i);
                    }
                );
            }

            palabra.appendChild(elemento);
        }
    }

    function mostrarOpciones() {

        opciones.innerHTML = "";

        state.letrasDisponibles.forEach(
            letra => {

                const boton =
                    document.createElement("button");

                boton.type = "button";

                boton.className =
                    "juego4__opcion";

                boton.textContent = letra;

                boton.addEventListener(
                    "click",
                    () => {

                        seleccionarLetra(
                            letra,
                            boton
                        );
                    }
                );

                opciones.appendChild(boton);
            }
        );
    }

    function seleccionarLetra(
        letra,
        boton
    ) {

        if (state.bloqueado) {
            return;
        }

        const posicionDisponible =
            state.posicionesOcultas.find(
                posicion => {

                    return !state.letrasColocadas.some(
                        item =>
                            item.posicion === posicion
                    );
                }
            );

        if (
            posicionDisponible === undefined
        ) {
            return;
        }

        state.letrasColocadas.push({
            posicion: posicionDisponible,
            letra: letra,
            boton: boton
        });

        boton.classList.add("usada");
        boton.disabled = true;

        mostrarPalabra();

        if (
            state.letrasColocadas.length ===
            state.posicionesOcultas.length
        ) {

            comprobarPalabra();
        }
    }

    function eliminarLetra(posicion) {

        if (state.bloqueado) {
            return;
        }

        const index =
            state.letrasColocadas.findIndex(
                item =>
                    item.posicion === posicion
            );

        if (index === -1) {
            return;
        }

        const item =
            state.letrasColocadas[index];

        item.boton.disabled = false;

        item.boton.classList.remove("usada");

        state.letrasColocadas.splice(
            index,
            1
        );

        mostrarPalabra();
    }

    function comprobarPalabra() {

        const textoCorrecto =
            state.palabraActual.word.toUpperCase();

        let respuesta = "";

        for (
            let i = 0;
            i < textoCorrecto.length;
            i++
        ) {

            const colocada =
                state.letrasColocadas.find(
                    item =>
                        item.posicion === i
                );

            if (colocada) {

                respuesta +=
                    colocada.letra;

            } else {

                respuesta +=
                    textoCorrecto[i];
            }
        }

        const esCorrecta =
            respuesta === textoCorrecto;

        registrarResultado(
            state.palabraActual.id_word,
            esCorrecta
        ).then(() => {

            if (esCorrecta) {

                mostrarCorrecto();

            } else {

                mostrarIncorrecto();
            }

        }).catch(() => {

            feedback.textContent =
                "OCURRIÓ UN ERROR";

            feedback.className =
                "juego4__feedback incorrecto";

            state.bloqueado = false;
        });
    }

    function mostrarCorrecto() {

        state.bloqueado = true;

        feedback.textContent =
            "¡MUY BIEN!";

        feedback.className =
            "juego4__feedback correcto";

        setTimeout(
            siguientePalabra,
            1000
        );
    }

    function mostrarIncorrecto() {

        state.bloqueado = true;

        feedback.textContent =
            "PROBÁ DE NUEVO";

        feedback.className =
            "juego4__feedback incorrecto";

        setTimeout(() => {

            state.letrasColocadas.forEach(
                item => {

                    item.boton.disabled = false;

                    item.boton.classList.remove(
                        "usada"
                    );
                }
            );

            state.letrasColocadas = [];

            state.bloqueado = false;

            feedback.textContent = "";

            feedback.className =
                "juego4__feedback";

            mostrarPalabra();

        }, 1000);
    }

    function siguientePalabra() {

        state.indice++;

        if (
            state.indice >=
            state.palabras.length
        ) {

            finalizarJuego4();

            return;
        }

        cargarPalabra();
    }

    function cargarPalabra() {

        state.bloqueado = false;

        state.palabraActual =
            state.palabras[state.indice];

        state.letrasColocadas = [];

        state.posicionesOcultas =
            crearPosicionesOcultas(
                state.palabraActual.word.toUpperCase()
            );

        crearLetrasDisponibles();

        imagen.src =
            state.palabraActual.image_url;

        imagen.alt =
            state.palabraActual.word;

        imagen.onerror = () => {

            console.error(
                "No se pudo cargar:",
                imagen.src
            );
        };

        feedback.textContent = "";

        feedback.className =
            "juego4__feedback";

        mostrarPalabra();

        mostrarOpciones();

        actualizarProgreso();
    }

    function finalizarJuego4() {

        state.bloqueado = true;

        feedback.textContent =
            "¡TERMINASTE!";

        feedback.className =
            "juego4__feedback correcto";

        opciones.innerHTML = "";

        completarJuego4()
            .then(data => {

                procesarDecision(data);

            })
            .catch(error => {

                console.error(
                    "Error al finalizar Juego 4:",
                    error
                );

                feedback.textContent =
                    "OCURRIÓ UN ERROR";

                state.bloqueado = false;
            });
    }

    function finalizarPantalla() {

        feedback.textContent =
            "¡TERMINASTE!";

        feedback.className =
            "juego4__feedback correcto";

        opciones.innerHTML = "";
    }

    function limpiarAnimacionesTutorial() {

        if (!tutorial) {
            return;
        }

        const elementos =
            tutorial.querySelectorAll(
                ".tutorial-animando, .tutorial-correcta, .tutorial-palabra-animada"
            );

        elementos.forEach(elemento => {

            elemento.classList.remove(
                "tutorial-animando",
                "tutorial-correcta",
                "tutorial-palabra-animada"
            );
        });
    }

    function ejecutarTutorial() {

        if (!tutorial) {
            return;
        }

        clearTimeout(tutorialTimer);

        limpiarAnimacionesTutorial();

        const faltante =
            tutorial.querySelector(
                ".tutorial-faltante"
            );

        const correcta =
            tutorial.querySelector(
                "#tutorialOpciones button:nth-child(2)"
            );

        const texto =
            document.getElementById(
                "tutorialTexto"
            );

        if (!faltante || !correcta) {
            return;
        }

        faltante.textContent = "_";

        faltante.classList.remove(
            "tutorial-animando",
            "tutorial-correcta"
        );

        correcta.classList.remove(
            "tutorial-letra-correcta"
        );

        void correcta.offsetWidth;

        correcta.classList.add(
            "tutorial-letra-correcta"
        );

        if (texto) {

            texto.textContent =
                "ELEGÍ LA LETRA QUE FALTA";
        }

        tutorialTimer =
            setTimeout(() => {

                correcta.classList.remove(
                    "tutorial-letra-correcta"
                );

                faltante.classList.add(
                    "tutorial-animando"
                );

            }, 900);

        tutorialTimer =
            setTimeout(() => {

                faltante.classList.remove(
                    "tutorial-animando"
                );

                faltante.textContent = "E";

                faltante.classList.add(
                    "tutorial-correcta"
                );

                if (texto) {

                    texto.textContent =
                        "¡ASÍ SE COMPLETA!";
                }

            }, 1800);

        tutorialTimer =
            setTimeout(() => {

                const palabraTutorial =
                    document.getElementById(
                        "tutorialPalabra"
                    );

                if (palabraTutorial) {

                    palabraTutorial.classList.add(
                        "tutorial-palabra-animada"
                    );
                }

            }, 2200);
    }

    function mostrarTutorial() {

        if (!tutorial) {
            return;
        }

        tutorial.classList.add("visible");

        ejecutarTutorial();
    }

    function cerrarTutorialFuncion() {

        if (!tutorial) {
            return;
        }

        clearTimeout(tutorialTimer);

        tutorial.classList.remove("visible");
    }

    function repetirTutorialFuncion() {

        if (!tutorial) {
            return;
        }

        clearTimeout(tutorialTimer);

        ejecutarTutorial();
    }

    if (cerrarTutorial) {

        cerrarTutorial.addEventListener(
            "click",
            cerrarTutorialFuncion
        );
    }

    if (avanzarTutorial) {

        avanzarTutorial.addEventListener(
            "click",
            cerrarTutorialFuncion
        );
    }

    if (btnRepetirTutorial) {

        btnRepetirTutorial.addEventListener(
            "click",
            event => {

                event.preventDefault();
                event.stopPropagation();

                repetirTutorialFuncion();
            }
        );
    }

    if (PALABRAS_JUEGO.length === 0) {

        console.error(
            "No hay palabras disponibles."
        );

        feedback.textContent =
            "NO HAY PALABRAS DISPONIBLES";

        return;
    }

    state.palabras =
        shuffle(PALABRAS_JUEGO);

    cargarPalabra();

    setTimeout(
        mostrarTutorial,
        300
    );
});