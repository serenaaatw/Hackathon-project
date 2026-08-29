
console.log("🔥 CAMARA.JS - SISTEMA DE LETRAS 🔥");

const video = document.getElementById("video");
const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

let handLandmarker = null;
let lastVideoTime = -1;

let estado = "ESPERANDO";
let puntosDibujo = [];

let ultimoX = null;
let ultimoY = null;

const SUAVIZADO = 0.50;
const DISTANCIA_MINIMA = 3;

const letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".split("");

let indiceLetra = 0;
let letraObjetivo = letras[indiceLetra];

/* =========================================================
   VIDEOS LSA
   ========================================================= */

const videoLSA =
    document.getElementById("videoLSA");

const lsaLetra =
    document.getElementById("lsaLetra");

function actualizarVideoLSA() {

    if (!videoLSA) {
        return;
    }

    if (!letraObjetivo) {

        videoLSA.removeAttribute("src");
        videoLSA.load();

        if (lsaLetra) {
            lsaLetra.textContent = "✓";
        }

        return;
    }

    const letra =
        letraObjetivo.toUpperCase();

    videoLSA.src =
        `/static/videos/lsa/${letra}.mp4`;

    videoLSA.load();

    videoLSA.play().catch(() => {});

    if (lsaLetra) {
        lsaLetra.textContent = letra;
    }
}

let intentos = 0;
let buenos = 0;

const MAX_INTENTOS = 10;
const BUENOS_NECESARIOS = 3;

let ejercicioTerminado = false;
let procesando = false;


/* =========================================================
   CÁMARA
   ========================================================= */

async function iniciarCamara() {

    try {

        console.log("Iniciando cámara...");

        const stream =
            await navigator.mediaDevices.getUserMedia({

                video: {
                    width: { ideal: 1280 },
                    height: { ideal: 720 },
                    facingMode: "user"
                },

                audio: false
            });

        video.srcObject = stream;
        video.style.display = "block";

        await new Promise((resolve) => {
            video.onloadedmetadata = resolve;
        });

        await video.play();

        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;

        actualizarInterfaz();

        await cargarMediaPipe();

        detectarMano();

    } catch (error) {

        console.error(
            "Error con la cámara:",
            error
        );

        alert(
            "No se pudo acceder a la cámara."
        );
    }
}


/* =========================================================
   MEDIA PIPE
   ========================================================= */

async function cargarMediaPipe() {

    const vision =
        await FilesetResolver.forVisionTasks(
            "/static/wasm"
        );

    handLandmarker =
        await HandLandmarker.createFromOptions(
            vision,
            {

                baseOptions: {
                    modelAssetPath:
                        "/static/hand_landmarker.task"
                },

                runningMode: "VIDEO",

                numHands: 1,

                minHandDetectionConfidence: 0.5,

                minHandPresenceConfidence: 0.5,

                minTrackingConfidence: 0.5
            }
        );

    console.log(
        "MediaPipe listo"
    );
}


/* =========================================================
   DETECCIÓN DE MANO
   ========================================================= */

async function detectarMano() {

    if (!handLandmarker) {

        requestAnimationFrame(
            detectarMano
        );

        return;
    }

    if (
        video.readyState >= 2 &&
        video.currentTime !== lastVideoTime
    ) {

        lastVideoTime =
            video.currentTime;

        const resultado =
            handLandmarker.detectForVideo(
                video,
                performance.now()
            );

        dibujarInterfaz(
            resultado
        );
    }

    requestAnimationFrame(
        detectarMano
    );
}


/* =========================================================
   INTERFAZ DE CÁMARA
   ========================================================= */

function dibujarInterfaz(resultado) {

    ctx.clearRect(
        0,
        0,
        canvas.width,
        canvas.height
    );

    if (
        !resultado.landmarks ||
        resultado.landmarks.length === 0
    ) {
        return;
    }

    const mano =
        resultado.landmarks[0];

    const indice =
        mano[8];

    const xReal =
        (1 - indice.x) *
        canvas.width;

    const yReal =
        indice.y *
        canvas.height;

    let xIndice =
        xReal;

    let yIndice =
        yReal;

    if (ultimoX !== null) {

        xIndice =
            ultimoX +
            (xReal - ultimoX) *
            SUAVIZADO;

        yIndice =
            ultimoY +
            (yReal - ultimoY) *
            SUAVIZADO;
    }

    const abierta =
        manoAbierta(mano);

    const cerrada =
        punoCerrado(mano);


    /* PUNTO ROJO DEL ÍNDICE */

    ctx.beginPath();

    ctx.arc(
        xReal,
        yReal,
        12,
        0,
        Math.PI * 2
    );

    ctx.fillStyle =
        "#ff3b30";

    ctx.fill();


    ctx.beginPath();

    ctx.arc(
        xReal,
        yReal,
        17,
        0,
        Math.PI * 2
    );

    ctx.strokeStyle =
        "#ffffff";

    ctx.lineWidth = 4;

    ctx.stroke();


    /* ESTADOS */

    if (!ejercicioTerminado) {

        if (
            estado === "ESPERANDO"
        ) {

            if (abierta) {

                estado =
                    "LISTO";

                puntosDibujo =
                    [];

                ultimoX =
                    xIndice;

                ultimoY =
                    yIndice;
            }
        }

        else if (
            estado === "LISTO"
        ) {

            if (cerrada) {

                estado =
                    "ESPERANDO";

                puntosDibujo =
                    [];

                ultimoX =
                    null;

                ultimoY =
                    null;

            }

            else if (abierta) {

                const distancia =
                    calcularDistancia(
                        xReal,
                        yReal,
                        ultimoX,
                        ultimoY
                    );

                if (
                    distancia >=
                    DISTANCIA_MINIMA
                ) {

                    estado =
                        "DIBUJANDO";

                    puntosDibujo =
                        [
                            []
                        ];

                    puntosDibujo[0].push({
                        x: xIndice,
                        y: yIndice
                    });

                    ultimoX =
                        xIndice;

                    ultimoY =
                        yIndice;
                }
            }
        }

        else if (
            estado === "DIBUJANDO"
        ) {

            if (cerrada) {

                console.log(
                    "DIBUJO TERMINADO",
                    puntosDibujo
                );

                estado =
                    "ESPERANDO";

                ultimoX =
                    null;

                ultimoY =
                    null;

                procesarDibujo();

            }

            else if (abierta) {

                const ultimoPunto =
                    puntosDibujo[
                        puntosDibujo.length - 1
                    ]?.slice(-1)[0];

                let distancia =
                    999;

                if (ultimoPunto) {

                    distancia =
                        calcularDistancia(
                            xIndice,
                            yIndice,
                            ultimoPunto.x,
                            ultimoPunto.y
                        );
                }

                if (
                    distancia >=
                    DISTANCIA_MINIMA
                ) {

                    if (
                        puntosDibujo.length === 0
                    ) {

                        puntosDibujo.push([]);
                    }

                    puntosDibujo[
                        puntosDibujo.length - 1
                    ].push({

                        x: xIndice,

                        y: yIndice
                    });

                    ultimoX =
                        xIndice;

                    ultimoY =
                        yIndice;
                }
            }
        }
    }

    dibujarTrazos();

    ultimoX =
        xIndice;

    ultimoY =
        yIndice;
}


/* =========================================================
   PROCESAR DIBUJO
   ========================================================= */

async function procesarDibujo() {

    if (
        procesando ||
        ejercicioTerminado
    ) {
        return;
    }

    if (
        !puntosDibujo ||
        puntosDibujo.length === 0
    ) {
        return;
    }

    procesando =
        true;

    const dibujoEnviar =
        JSON.parse(
            JSON.stringify(
                puntosDibujo
            )
        );

    console.log(
        "📤 Enviando dibujo a Python..."
    );

    try {

        const respuesta =
            await fetch(
                "/procesar_dibujo",
                {

                    method:
                        "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify({

                            puntos_dibujo:
                                dibujoEnviar,

                            letra_objetivo:
                                letraObjetivo
                        })
                }
            );

        const resultado =
            await respuesta.json();

        console.log(
            "📥 Resultado recibido:",
            resultado
        );

        if (!respuesta.ok) {

            throw new Error(
                resultado.error ||
                "Error del servidor"
            );
        }

        const similitud =
            Number(
                resultado.similitud
            );

        const confianza =
            Number(
                resultado.confianza
            );

        const calificacion =
            resultado.calificacion;

        intentos++;

        if (
            calificacion ===
                "BUENO" ||
            calificacion ===
                "MEDIO"
        ) {

            buenos++;
        }

        actualizarInterfaz();

        console.log(
            `Letra: ${letraObjetivo} | ` +
            `Intento: ${intentos}/${MAX_INTENTOS} | ` +
            `Buenos: ${buenos}/${BUENOS_NECESARIOS} | ` +
            `Detectada: ${resultado.letra_detectada} | ` +
            `Confianza: ${confianza.toFixed(2)}% | ` +
            `Similitud: ${similitud.toFixed(2)}% | ` +
            `Resultado: ${calificacion}`
        );

        if (
            buenos >=
            BUENOS_NECESARIOS
        ) {

            cambiarSiguienteLetra();

            return;
        }

        if (
            intentos >=
            MAX_INTENTOS
        ) {

            cambiarSiguienteLetra();

            return;
        }

    } catch (error) {

        console.error(
            "❌ Error procesando dibujo:",
            error
        );

    } finally {

        procesando =
            false;

        puntosDibujo =
            [];

        estado =
            "ESPERANDO";

        ultimoX =
            null;

        ultimoY =
            null;
    }
}


/* =========================================================
   ACTUALIZAR INTERFAZ
   ========================================================= */

function actualizarInterfaz() {

    const buenosElemento =
        document.getElementById(
            "buenos"
        );

    const intentosElemento =
        document.getElementById(
            "intentos"
        );

    const letraElemento =
        document.getElementById(
            "letraObjetivo"
        );

    const estrellasElemento =
        document.querySelector(
            ".mini-stars"
        );


    if (buenosElemento) {

        buenosElemento.textContent =
            `${buenos} / ${BUENOS_NECESARIOS}`;
    }


    if (intentosElemento) {

        intentosElemento.textContent =
            `${intentos} / ${MAX_INTENTOS}`;
    }


    if (letraElemento) {

        letraElemento.textContent =
            letraObjetivo || "✓";
    }


    if (estrellasElemento) {

        const estrellasLlenas =
            "⭐".repeat(
                buenos
            );

        const estrellasVacias =
            "☆".repeat(
                Math.max(
                    0,
                    BUENOS_NECESARIOS -
                    buenos
                )
            );

        estrellasElemento.textContent =
            estrellasLlenas +
            estrellasVacias;
    }


    /* ACTUALIZAR VIDEO LSA */

    actualizarVideoLSA();
}


/* =========================================================
   SIGUIENTE LETRA
   ========================================================= */

function cambiarSiguienteLetra() {

    indiceLetra++;

    intentos =
        0;

    buenos =
        0;

    puntosDibujo =
        [];

    estado =
        "ESPERANDO";

    ultimoX =
        null;

    ultimoY =
        null;


    if (
        indiceLetra >=
        letras.length
    ) {

        ejercicioTerminado =
            true;

        letraObjetivo =
            null;

        actualizarInterfaz();

        console.log(
            "🎉 TODAS LAS LETRAS TERMINADAS"
        );

        return;
    }


    letraObjetivo =
        letras[indiceLetra];

    actualizarInterfaz();

    console.log(
        `➡️ Siguiente letra: ${letraObjetivo}`
    );
}


/* =========================================================
   DIBUJAR TRAZOS
   ========================================================= */

function dibujarTrazos() {

    ctx.save();

    for (
        const trazo
        of puntosDibujo
    ) {

        if (
            trazo.length < 2
        ) {
            continue;
        }

        ctx.beginPath();

        ctx.moveTo(
            trazo[0].x,
            trazo[0].y
        );

        for (
            let i = 1;
            i < trazo.length;
            i++
        ) {

            ctx.lineTo(
                trazo[i].x,
                trazo[i].y
            );
        }

        ctx.strokeStyle =
            "#00e5ff";

        ctx.lineWidth =
            8;

        ctx.lineCap =
            "round";

        ctx.lineJoin =
            "round";

        ctx.shadowColor =
            "#00e5ff";

        ctx.shadowBlur =
            12;

        ctx.stroke();
    }

    ctx.restore();
}


/* =========================================================
   MANO ABIERTA
   ========================================================= */

function manoAbierta(mano) {

    const indice =
        mano[8].y <
        mano[6].y;

    const medio =
        mano[12].y <
        mano[10].y;

    const anular =
        mano[16].y <
        mano[14].y;

    const menique =
        mano[20].y <
        mano[18].y;

    return (
        indice &&
        medio &&
        anular &&
        menique
    );
}


/* =========================================================
   PUÑO CERRADO
   ========================================================= */

function punoCerrado(mano) {

    const indice =
        mano[8].y >
        mano[6].y;

    const medio =
        mano[12].y >
        mano[10].y;

    const anular =
        mano[16].y >
        mano[14].y;

    const menique =
        mano[20].y >
        mano[18].y;

    return (
        indice &&
        medio &&
        anular &&
        menique
    );
}


/* =========================================================
   DISTANCIA
   ========================================================= */

function calcularDistancia(
    x1,
    y1,
    x2,
    y2
) {

    if (
        x2 === null ||
        y2 === null
    ) {
        return 999;
    }

    return Math.sqrt(

        Math.pow(
            x1 - x2,
            2
        ) +

        Math.pow(
            y1 - y2,
            2
        )
    );
}


/* =========================================================
   LIMPIAR DIBUJO
   ========================================================= */

function limpiarDibujo() {

    puntosDibujo =
        [];

    estado =
        "ESPERANDO";

    ultimoX =
        null;

    ultimoY =
        null;
}


/* =========================================================
   SALIR
   ========================================================= */

function salirCamara() {

    if (video.srcObject) {

        const tracks =
            video.srcObject.getTracks();

        tracks.forEach(
            track =>
                track.stop()
        );

        video.srcObject =
            null;
    }

    window.location.href =
        "/reconocer_mano";
}


/* =========================================================
   TECLADO
   ========================================================= */

document.addEventListener(
    "keydown",
    (event) => {

        if (
            event.key === "c" ||
            event.key === "C"
        ) {

            limpiarDibujo();
        }

        if (
            event.key === "q" ||
            event.key === "Q"
        ) {

            salirCamara();
        }
    }
);


/* =========================================================
   INICIO
   ========================================================= */

console.log(
    "🔥 VOY A INICIAR LA CÁMARA 🔥"
);

iniciarCamara();
