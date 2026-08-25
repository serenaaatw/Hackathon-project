(function () {

    "use strict";

    const state = {
        index: 0,
        orden: [],
        palabraArmada: [],
        tutorialActivo: false,
        tutorialTimers: []
    };

    const els = {

        imagen:
            document.getElementById("imagenPalabra"),

        palabraArmada:
            document.getElementById("palabraArmada"),

        letras:
            document.getElementById("letras"),

        feedback:
            document.getElementById("feedback"),

        progreso:
            document.getElementById("progreso")

    };

    if (
        !Array.isArray(PALABRAS) ||
        PALABRAS.length === 0
    ) {

        console.error(
            "Juego 3: no se recibieron palabras."
        );

        return;
    }

    function shuffle(array) {

        const copia = [...array];

        for (
            let i = copia.length - 1;
            i > 0;
            i--
        ) {

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

    function registrarResultado(
        idWord,
        correcto
    ) {

        return fetch(
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
        .then(response => {

            if (!response.ok) {

                throw new Error(
                    "No se pudo registrar el resultado"
                );

            }

            return response.json();

        });

    }

    function obtenerPalabraActual() {

        const posicion =
            state.orden[state.index];

        return PALABRAS[posicion];
    }

    function iniciar() {

        state.orden =
            shuffle(
                PALABRAS.map(
                    (_, index) => index
                )
            );

        crearProgreso();

        mostrarPalabra();
    }

    function crearProgreso() {

        if (!els.progreso) {
            return;
        }

        els.progreso.innerHTML = "";

        PALABRAS.forEach(() => {

            const punto =
                document.createElement("div");

            punto.className =
                "juego3__progreso-punto";

            els.progreso.appendChild(
                punto
            );

        });

        actualizarProgreso();
    }

    function actualizarProgreso() {

        if (!els.progreso) {
            return;
        }

        [
            ...els.progreso.children
        ].forEach(
            (punto, index) => {

                punto.classList.toggle(
                    "completado",
                    index < state.index
                );

                punto.classList.toggle(
                    "actual",
                    index === state.index
                );

            }
        );

    }

    function mostrarPalabra() {

        const item =
            obtenerPalabraActual();

        if (!item) {
            finalizarJuego();
            return;
        }

        state.palabraArmada = [];

        if (els.feedback) {

            els.feedback.textContent = "";

            els.feedback.className =
                "juego3__feedback";

        }

        if (els.imagen) {

            els.imagen.src =
                item.image_url;

            els.imagen.alt =
                item.word;

            els.imagen.style.display =
                "block";

        }

        mostrarPalabraArmada();

        crearLetras(item);

        actualizarProgreso();

    }

    function crearLetras(item) {

        if (!els.letras) {
            return;
        }

        els.letras.innerHTML = "";

        const palabra =
            item.word
                .toUpperCase()
                .split("");

        const letrasDesordenadas =
            shuffle(palabra);

        letrasDesordenadas.forEach(
            (letra, index) => {

                const boton =
                    document.createElement(
                        "button"
                    );

                boton.type = "button";

                boton.className =
                    "juego3__letra";

                boton.textContent =
                    letra;

                boton.dataset.index =
                    index;

                boton.addEventListener(
                    "click",
                    function () {

                        seleccionarLetra(
                            boton,
                            letra
                        );

                    }
                );

                els.letras.appendChild(
                    boton
                );

            }
        );

    }

    function seleccionarLetra(
        boton,
        letra
    ) {

        if (
            boton.classList.contains(
                "usada"
            )
        ) {
            return;
        }

        boton.classList.add(
            "usada"
        );

        state.palabraArmada.push(
            letra
        );

        mostrarPalabraArmada();

        const item =
            obtenerPalabraActual();

        if (
            state.palabraArmada.length ===
            item.word.length
        ) {

            comprobarPalabra();

        }

    }

    function mostrarPalabraArmada() {

        if (!els.palabraArmada) {
            return;
        }

        els.palabraArmada.innerHTML = "";

        state.palabraArmada.forEach(
            letra => {

                const elemento =
                    document.createElement(
                        "div"
                    );

                elemento.className =
                    "juego3__letra-armada";

                elemento.textContent =
                    letra;

                els.palabraArmada.appendChild(
                    elemento
                );

            }
        );

    }

    function comprobarPalabra() {

        const item =
            obtenerPalabraActual();

        const respuesta =
            state.palabraArmada.join("");

        const correcta =
            item.word.toUpperCase();

        const esCorrecta =
            respuesta === correcta;

        registrarResultado(
            item.id_word,
            esCorrecta
        )
        .then(() => {

            if (esCorrecta) {

                mostrarCorrecto();

            } else {

                mostrarIncorrecto();

            }

        })
        .catch(error => {

            console.error(
                "Error al registrar progreso:",
                error
            );

        });

    }

    function mostrarCorrecto() {

        if (!els.feedback) {
            return;
        }

        els.feedback.textContent =
            "¡MUY BIEN!";

        els.feedback.className =
            "juego3__feedback correcto";

        setTimeout(
            siguientePalabra,
            1000
        );

    }

    function mostrarIncorrecto() {

        if (!els.feedback) {
            return;
        }

        els.feedback.textContent =
            "PROBÁ DE NUEVO";

        els.feedback.className =
            "juego3__feedback incorrecto";

        setTimeout(
            () => {

                state.palabraArmada = [];

                mostrarPalabraArmada();

                if (els.letras) {

                    [
                        ...els.letras.children
                    ].forEach(
                        boton => {

                            boton.classList.remove(
                                "usada"
                            );

                        }
                    );

                }

                els.feedback.textContent =
                    "";

                els.feedback.className =
                    "juego3__feedback";

            },
            800
        );

    }

    function siguientePalabra() {

        state.index++;

        if (
            state.index >=
            state.orden.length
        ) {

            finalizarJuego();

            return;
        }

        mostrarPalabra();

    }

    function finalizarJuego() {

        if (els.feedback) {

            els.feedback.textContent =
                "¡MUY BIEN!";

            els.feedback.className =
                "juego3__feedback correcto";

        }

        fetch(
            "/juego/completar",
            {
                method: "POST",
                headers: {
                    "Content-Type":
                        "application/json"
                },
                body: JSON.stringify({
                    numero_juego: 3
                })
            }
        )
        .then(response => {

            if (!response.ok) {

                throw new Error(
                    "No se pudo completar el juego"
                );

            }

            return response.json();

        })
        .then(data => {

            if (!data.ok) {

                throw new Error(
                    data.error ||
                    "No se pudo continuar"
                );

            }

            if (data.ronda_completada) {

                window.location.href =
                    "/aprender";

                return;
            }

            window.location.assign(
                "/juego/4"
            );

        })
        .catch(error => {

            console.error(
                "Error al completar juego 3:",
                error
            );

        });

    }

    function limpiarTimersTutorial() {

        state.tutorialTimers.forEach(
            timer => {
                clearTimeout(timer);
            }
        );

        state.tutorialTimers = [];

    }

    function crearTutorial() {

        const tutorial =
            document.createElement("div");

        tutorial.id =
            "tutorialJuego3";

        tutorial.className =
            "juego3__tutorial";

        tutorial.innerHTML = `

            <div class="juego3__tutorial-contenido">

                <button
                    type="button"
                    class="juego3__tutorial-cerrar"
                    id="cerrarTutorialJuego3"
                    aria-label="Cerrar tutorial"
                >
                    ×
                </button>

                <div class="juego3__tutorial-imagen">

                    <img
                        id="tutorialImagenJuego3"
                        src=""
                        alt=""
                    >

                </div>

                <div
                    class="juego3__tutorial-palabra"
                    id="tutorialPalabraJuego3"
                >
                </div>

                <div
                    class="juego3__tutorial-letras"
                    id="tutorialLetrasJuego3"
                >
                </div>

                <div class="juego3__tutorial-controles">

                    <button
                        type="button"
                        class="juego3__tutorial-reiniciar"
                        id="reiniciarTutorialJuego3"
                        aria-label="Repetir tutorial"
                        title="Repetir"
                    >
                        ↻
                    </button>

                    <button
                        type="button"
                        class="juego3__tutorial-continuar"
                        id="continuarTutorialJuego3"
                        aria-label="Continuar"
                        title="Continuar"
                    >
                        →
                    </button>

                </div>

            </div>
        `;

        document.body.appendChild(
            tutorial
        );

        const item =
            obtenerPalabraActual();

        if (item) {

            const imagen =
                document.getElementById(
                    "tutorialImagenJuego3"
                );

            if (imagen) {

                imagen.src =
                    item.image_url;

                imagen.alt =
                    item.word;

            }

            crearLetrasTutorial(item);

        }

        const cerrar =
            document.getElementById(
                "cerrarTutorialJuego3"
            );

        if (cerrar) {

            cerrar.addEventListener(
                "click",
                cerrarTutorial
            );

        }

        const continuar =
            document.getElementById(
                "continuarTutorialJuego3"
            );

        if (continuar) {

            continuar.addEventListener(
                "click",
                cerrarTutorial
            );

        }

        const reiniciar =
            document.getElementById(
                "reiniciarTutorialJuego3"
            );

        if (reiniciar) {

            reiniciar.addEventListener(
                "click",
                () => {

                    const item =
                        obtenerPalabraActual();

                    if (item) {

                        crearLetrasTutorial(
                            item
                        );

                    }

                }
            );

        }

    }

    function crearLetrasTutorial(item) {

        limpiarTimersTutorial();

        const contenedor =
            document.getElementById(
                "tutorialLetrasJuego3"
            );

        const palabra =
            document.getElementById(
                "tutorialPalabraJuego3"
            );

        if (
            !contenedor ||
            !palabra
        ) {
            return;
        }

        contenedor.innerHTML = "";

        palabra.innerHTML = "";

        const letras =
            item.word
                .toUpperCase()
                .split("");

        const letrasDesordenadas =
            shuffle(letras);

        letrasDesordenadas.forEach(
            letra => {

                const elemento =
                    document.createElement(
                        "div"
                    );

                elemento.className =
                    "juego3__tutorial-letra";

                elemento.textContent =
                    letra;

                contenedor.appendChild(
                    elemento
                );

            }
        );

        const timerInicial =
            setTimeout(
                () => {

                    letras.forEach(
                        (letra, index) => {

                            const timer =
                                setTimeout(
                                    () => {

                                        const elemento =
                                            document.createElement(
                                                "div"
                                            );

                                        elemento.className =
                                            "juego3__tutorial-letra-armada";

                                        elemento.textContent =
                                            letra;

                                        palabra.appendChild(
                                            elemento
                                        );

                                        const letrasTutorial =
                                            document.querySelectorAll(
                                                "#tutorialLetrasJuego3 .juego3__tutorial-letra"
                                            );

                                        if (
                                            letrasTutorial[index]
                                        ) {

                                            letrasTutorial[
                                                index
                                            ].classList.add(
                                                "usada"
                                            );

                                        }

                                    },
                                    index * 450
                                );

                            state.tutorialTimers.push(
                                timer
                            );

                        }
                    );

                },
                1000
            );

        state.tutorialTimers.push(
            timerInicial
        );

    }

    function cerrarTutorial() {

        limpiarTimersTutorial();

        const tutorial =
            document.getElementById(
                "tutorialJuego3"
            );

        if (!tutorial) {
            return;
        }

        tutorial.classList.add(
            "oculto"
        );

        setTimeout(
            () => {

                if (tutorial) {
                    tutorial.remove();
                }

            },
            400
        );

        state.tutorialActivo =
            false;

    }

    function mostrarTutorial() {

        if (
            state.tutorialActivo
        ) {
            return;
        }

        state.tutorialActivo =
            true;

        crearTutorial();

    }

    iniciar();

    setTimeout(
        mostrarTutorial,
        300
    );

})();