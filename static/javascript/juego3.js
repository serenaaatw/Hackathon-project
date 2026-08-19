console.log("🔥 JUEGO 3 JS CARGADO 🔥");

(function () {

    console.log("🔥 JUEGO 3 EJECUTANDO 🔥");

    const state = {

        index: 0,

        orden: [],

        palabraArmada: []

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
            ] =
            [
                copia[j],
                copia[i]
            ];

        }

        return copia;
    }


    function iniciar() {

        console.log("JUEGO 3 INICIADO");

        console.log("PALABRAS:", PALABRAS);

        console.log("IMG_BASE:", IMG_BASE);


        if (
            !PALABRAS ||
            PALABRAS.length === 0
        ) {

            els.feedback.textContent =
                "NO HAY PALABRAS DISPONIBLES.";

            return;

        }


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


    function obtenerPalabraActual() {

        const posicion =
            state.orden[state.index];

        return PALABRAS[posicion];

    }


    function mostrarPalabra() {

        const item =
            obtenerPalabraActual();


        if (!item) {
            return;
        }


        console.log(
            "PALABRA ACTUAL:",
            item
        );


        state.palabraArmada = [];


        // Limpiar feedback

        els.feedback.textContent = "";

        els.feedback.className =
            "juego3__feedback";


        const imagen =
            `${IMG_BASE}${item.image_file}`;

        console.log(
            "IMAGEN:",
            imagen
        );


        els.imagen.src = imagen;

        els.imagen.alt =
            item.word;


        // Si la imagen falla

        els.imagen.onerror =
            function () {

                console.error(
                    "NO SE PUDO CARGAR:",
                    imagen
                );

            };


        mostrarPalabraArmada();


        crearLetras(item);


        actualizarProgreso();

    }


    function crearLetras(item) {

        els.letras.innerHTML = "";


        const palabra =
            item.word
                .toUpperCase()
                .trim();


        console.log(
            "CREANDO LETRAS:",
            palabra
        );


        const letras =
            shuffle(
                palabra.split("")
            );


        letras.forEach(
            (letra) => {

                const boton =
                    document.createElement(
                        "button"
                    );


                boton.type =
                    "button";


                boton.className =
                    "juego3__letra";


                boton.textContent =
                    letra;


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

        els.palabraArmada.innerHTML =
            "";


        state.palabraArmada.forEach(
            (letra) => {

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
            item.word
                .toUpperCase()
                .trim();


        console.log(
            "RESPUESTA:",
            respuesta
        );

        console.log(
            "CORRECTA:",
            correcta
        );


        if (
            respuesta === correcta
        ) {

            mostrarCorrecto();

        } else {

            mostrarIncorrecto();

        }

    }


    function mostrarCorrecto() {

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

        els.feedback.textContent =
            "PROBÁ DE NUEVO";


        els.feedback.className =
            "juego3__feedback incorrecto";


        setTimeout(
            () => {

                state.palabraArmada = [];


                mostrarPalabraArmada();


                [
                    ...els.letras.children
                ].forEach(
                    (boton) => {

                        boton.classList.remove(
                            "usada"
                        );

                    }
                );


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

            state.index = 0;


            state.orden =
                shuffle(
                    PALABRAS.map(
                        (_, index) => index
                    )
                );

        }


        mostrarPalabra();

    }


    iniciar();

})();