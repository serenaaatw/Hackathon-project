(function () {

    "use strict";


    const state = {
        index: 0,
        orden: [],
        palabraArmada: [],
        tutorialActivo: false
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


    

    if (!Array.isArray(PALABRAS) || PALABRAS.length === 0) {

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

            els.progreso.appendChild(punto);

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

            console.error(
                "No se pudo obtener la palabra actual."
            );

            return;

        }


        console.log(
            "Juego 3 - palabra:",
            item
        );


        state.palabraArmada = [];


        if (els.feedback) {

            els.feedback.textContent = "";

            els.feedback.className =
                "juego3__feedback";

        }


       
        if (els.imagen) {

            const imagen =
                `${IMG_BASE}${CATEGORIA_SLUG}/${item.image_file}`;

            console.log(
                "Juego 3 - imagen:",
                imagen
            );

            els.imagen.src = imagen;

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
                    document.createElement("button");


                boton.type =
                    "button";


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
            boton.classList.contains("usada")
        ) {
            return;
        }


        boton.classList.add("usada");


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
                    document.createElement("div");


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


        if (respuesta === correcta) {

            mostrarCorrecto();

        } else {

            mostrarIncorrecto();

        }

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


                els.feedback.textContent = "";


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


            imagen.src =
                `${IMG_BASE}${CATEGORIA_SLUG}/${item.image_file}`;


            imagen.alt =
                item.word;


            crearLetrasTutorial(item);

        }


        document
            .getElementById(
                "cerrarTutorialJuego3"
            )
            .addEventListener(
                "click",
                cerrarTutorial
            );


        document
            .getElementById(
                "continuarTutorialJuego3"
            )
            .addEventListener(
                "click",
                cerrarTutorial
            );


        document
            .getElementById(
                "reiniciarTutorialJuego3"
            )
            .addEventListener(
                "click",
                () => {

                    const item =
                        obtenerPalabraActual();

                    if (item) {
                        crearLetrasTutorial(item);
                    }

                }
            );

    }


    
    function crearLetrasTutorial(item) {

        const contenedor =
            document.getElementById(
                "tutorialLetrasJuego3"
            );


        if (!contenedor) {
            return;
        }


        contenedor.innerHTML = "";


        const letras =
            item.word
                .toUpperCase()
                .split("");


        shuffle(letras).forEach(
            letra => {

                const elemento =
                    document.createElement("div");


                elemento.className =
                    "juego3__tutorial-letra";


                elemento.textContent =
                    letra;


                contenedor.appendChild(
                    elemento
                );

            }
        );


        // Después de un momento,
        // mostramos cómo se ordena.

        setTimeout(
            () => {

                const palabra =
                    document.getElementById(
                        "tutorialPalabraJuego3"
                    );


                if (!palabra) {
                    return;
                }


                palabra.innerHTML = "";


                letras.forEach(
                    (letra, index) => {

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
                                        ".juego3__tutorial-letra"
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

                    }
                );

            },
            1000
        );

    }


   
    function cerrarTutorial() {

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

                tutorial.remove();

            },
            400
        );


        state.tutorialActivo =
            false;

    }


   
    function mostrarTutorial() {

        if (state.tutorialActivo) {
            return;
        }


        state.tutorialActivo =
            true;


        crearTutorial();

    }



    iniciar();


    // Mostrar tutorial después
    // de cargar el juego.

    setTimeout(
        mostrarTutorial,
        300
    );


})();