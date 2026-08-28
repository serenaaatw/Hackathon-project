import cv2
import os
import time
import mediapipe as mp

from mediapipe.tasks import python
from mediapipe.tasks.python import vision

from reconocimiento import (
    convertir_trazo_a_imagen,
    reconocer_letra,
    comparar_con_letra
)


# Cámara

camara = cv2.VideoCapture(0)

camara.set(
    cv2.CAP_PROP_FRAME_WIDTH,
    1280
)

camara.set(
    cv2.CAP_PROP_FRAME_HEIGHT,
    720
)


# Modelo MediaPipe

model_path = os.path.join(
    os.path.dirname(__file__),
    "hand_landmarker.task"
)


with open(
    model_path,
    "rb"
) as archivo:

    modelo = archivo.read()


opciones = vision.HandLandmarkerOptions(

    base_options=python.BaseOptions(
        model_asset_buffer=modelo
    ),

    running_mode=vision.RunningMode.VIDEO,

    num_hands=1,

    min_hand_detection_confidence=0.5,

    min_hand_presence_confidence=0.5,

    min_tracking_confidence=0.5
)


# Variables del dibujo

puntos_dibujo = []

estado = "ESPERANDO"

tiempo_mano_abierta = None

ultimo_x = None
ultimo_y = None

SUAVIZADO = 0.50

DISTANCIA_MINIMA = 3

VENTANA_RESULTADO = "Dibujo para IA"


# Letras que el usuario debe aprender

LETRAS_EJERCICIO = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

indice_letra = 0

LETRA_OBJETIVO = LETRAS_EJERCICIO[indice_letra]


# Progreso de la letra actual

intentos = 0

buenos = 0

MAX_INTENTOS = 10

BUENOS_NECESARIOS = 3


# Resultados finales

resultados_letras = {}


# Mensaje temporal para mostrar el resultado

mensaje_resultado = ""

tiempo_mensaje = None


def mostrar_dibujo_convertido(imagen):

    if imagen is None:
        return

    imagen_grande = cv2.resize(
        imagen,
        (280, 280),
        interpolation=cv2.INTER_NEAREST
    )

    cv2.namedWindow(
        VENTANA_RESULTADO,
        cv2.WINDOW_NORMAL
    )

    cv2.moveWindow(
        VENTANA_RESULTADO,
        1300,
        150
    )

    cv2.imshow(
        VENTANA_RESULTADO,
        imagen_grande
    )


def cerrar_resultado():

    try:

        cv2.destroyWindow(
            VENTANA_RESULTADO
        )

    except:

        pass


def cambiar_a_siguiente_letra():

    global indice_letra
    global LETRA_OBJETIVO
    global intentos
    global buenos
    global mensaje_resultado
    global tiempo_mensaje

    indice_letra += 1

    if indice_letra >= len(LETRAS_EJERCICIO):

        LETRA_OBJETIVO = None

        mensaje_resultado = "EJERCICIO TERMINADO"

        tiempo_mensaje = time.time()

        return

    LETRA_OBJETIVO = LETRAS_EJERCICIO[indice_letra]

    intentos = 0

    buenos = 0

    mensaje_resultado = ""

    tiempo_mensaje = None


def ejercicio_terminado():

    return (
        indice_letra
        >= len(LETRAS_EJERCICIO)
    )


def procesar_dibujo():

    global puntos_dibujo
    global estado
    global ultimo_x
    global ultimo_y
    global tiempo_mano_abierta
    global intentos
    global buenos
    global mensaje_resultado
    global tiempo_mensaje

    if not puntos_dibujo:

        estado = "ESPERANDO"

        return


    imagen_ia = convertir_trazo_a_imagen(
        puntos_dibujo
    )


    if imagen_ia is None:

        puntos_dibujo.clear()

        estado = "ESPERANDO"

        return


    # Mostrar dibujo procesado

    mostrar_dibujo_convertido(
        imagen_ia
    )


    # Reconocimiento de la IA

    letra_detectada, confianza = reconocer_letra(
        imagen_ia
    )


    # Comparación con la letra objetivo

    similitud = comparar_con_letra(
        imagen_ia,
        LETRA_OBJETIVO
    )


    # Determinar la calificación

    if similitud >= 70:

        calificacion = "BUENO"

    elif similitud >= 50:

        calificacion = "MEDIO"

    else:

        calificacion = "MALO"


    # Cada dibujo cuenta como un intento

    intentos += 1


    if calificacion == "BUENO" or calificacion == "MEDIO":

        buenos += 1


    print(
        f"Letra: {LETRA_OBJETIVO} | "
        f"Intento: {intentos}/{MAX_INTENTOS} | "
        f"Buenos: {buenos}/{BUENOS_NECESARIOS} | "
        f"Detectada: {letra_detectada} | "
        f"Confianza: {confianza:.2f}% | "
        f"Similitud: {similitud:.2f}% | "
        f"Resultado: {calificacion}"
    )


    # Si consiguió los 3 buenos,
    # la letra queda aprendida.

    if buenos >= BUENOS_NECESARIOS:

        resultados_letras[
            LETRA_OBJETIVO
        ] = "APRENDIDA"

        mensaje_resultado = (
            f"¡MUY BIEN! "
            f"APRENDISTE LA LETRA {LETRA_OBJETIVO}"
        )

        tiempo_mensaje = time.time()

        print(
            f"LETRA {LETRA_OBJETIVO}: APRENDIDA"
        )

        puntos_dibujo.clear()

        estado = "ESPERANDO"

        tiempo_mano_abierta = None

        ultimo_x = None
        ultimo_y = None

        cerrar_resultado()

        time.sleep(1)

        cambiar_a_siguiente_letra()

        return


    # Si llegó a 10 intentos sin conseguir
    # los 3 buenos, la letra queda como
    # no aprendida.

    if intentos >= MAX_INTENTOS:

        resultados_letras[
            LETRA_OBJETIVO
        ] = "NO APRENDIDA"

        mensaje_resultado = (
            f"LA LETRA {LETRA_OBJETIVO} "
            f"NO FUE APRENDIDA"
        )

        tiempo_mensaje = time.time()

        print(
            f"LETRA {LETRA_OBJETIVO}: NO APRENDIDA"
        )

        puntos_dibujo.clear()

        estado = "ESPERANDO"

        tiempo_mano_abierta = None

        ultimo_x = None
        ultimo_y = None

        cerrar_resultado()

        time.sleep(1)

        cambiar_a_siguiente_letra()

        return


    puntos_dibujo.clear()

    estado = "ESPERANDO"

    tiempo_mano_abierta = None

    ultimo_x = None
    ultimo_y = None


def mano_abierta(mano):

    indice_arriba = (
        mano[8].y
        <
        mano[6].y
    )

    medio_arriba = (
        mano[12].y
        <
        mano[10].y
    )

    anular_arriba = (
        mano[16].y
        <
        mano[14].y
    )

    menique_arriba = (
        mano[20].y
        <
        mano[18].y
    )

    return (
        indice_arriba
        and
        medio_arriba
        and
        anular_arriba
        and
        menique_arriba
    )


def puño_cerrado(mano):

    indice_cerrado = (
        mano[8].y
        >
        mano[6].y
    )

    medio_cerrado = (
        mano[12].y
        >
        mano[10].y
    )

    anular_cerrado = (
        mano[16].y
        >
        mano[14].y
    )

    menique_cerrado = (
        mano[20].y
        >
        mano[18].y
    )

    return (
        indice_cerrado
        and
        medio_cerrado
        and
        anular_cerrado
        and
        menique_cerrado
    )


with vision.HandLandmarker.create_from_options(
    opciones
) as detector:

    tiempo_inicio = time.time()

    while True:

        correcto, frame = camara.read()

        if not correcto:

            break


        # Espejo

        frame = cv2.flip(
            frame,
            1
        )


        alto, ancho, _ = frame.shape


        # Cuadro de dibujo

        margen_x = int(
            ancho * 0.20
        )

        margen_y = int(
            alto * 0.15
        )

        zona_x1 = margen_x

        zona_y1 = margen_y

        zona_x2 = ancho - margen_x

        zona_y2 = alto - margen_y


        cv2.rectangle(
            frame,
            (
                zona_x1,
                zona_y1
            ),
            (
                zona_x2,
                zona_y2
            ),
            (255, 255, 255),
            3
        )


        cv2.putText(
            frame,
            "Dibuja dentro del cuadro",
            (
                zona_x1,
                zona_y1 - 15
            ),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )


        # Mostrar letra actual

        if not ejercicio_terminado():

            cv2.putText(
                frame,
                f"Letra: {LETRA_OBJETIVO}",
                (
                    30,
                    alto - 70
                ),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.0,
                (255, 255, 255),
                2
            )


            cv2.putText(
                frame,
                f"Buenos: {buenos}/{BUENOS_NECESARIOS}",
                (
                    30,
                    alto - 35
                ),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 255),
                2
            )


            cv2.putText(
                frame,
                f"Intentos: {intentos}/{MAX_INTENTOS}",
                (
                    350,
                    alto - 35
                ),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 255),
                2
            )


        # MediaPipe

        frame_rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )


        imagen_mp = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=frame_rgb
        )


        timestamp = int(
            (
                time.time()
                -
                tiempo_inicio
            )
            * 1000
        )


        resultado = detector.detect_for_video(
            imagen_mp,
            timestamp
        )


        # Mano detectada

        if resultado.hand_landmarks:

            mano = resultado.hand_landmarks[0]


            # Punto del índice

            x_real = int(
                mano[8].x
                *
                ancho
            )

            y_real = int(
                mano[8].y
                *
                alto
            )


            # Suavizado

            if ultimo_x is None:

                x_indice = x_real

                y_indice = y_real

            else:

                x_indice = int(
                    ultimo_x
                    +
                    (
                        x_real
                        -
                        ultimo_x
                    )
                    *
                    SUAVIZADO
                )

                y_indice = int(
                    ultimo_y
                    +
                    (
                        y_real
                        -
                        ultimo_y
                    )
                    *
                    SUAVIZADO
                )


            # Punto rojo

            cv2.circle(
                frame,
                (
                    x_real,
                    y_real
                ),
                12,
                (0, 0, 255),
                -1
            )


            # Dentro del cuadro

            dentro_de_zona = (

                zona_x1
                <=
                x_real
                <=
                zona_x2

                and

                zona_y1
                <=
                y_real
                <=
                zona_y2
            )


            abierta = mano_abierta(
                mano
            )


            cerrada = puño_cerrado(
                mano
            )


            # Si ya terminó el ejercicio,
            # no seguimos dibujando.

            if ejercicio_terminado():

                pass


            elif estado == "ESPERANDO":

                if abierta:

                    cerrar_resultado()

                    estado = "PREPARANDO"

                    tiempo_mano_abierta = time.time()

                    puntos_dibujo.clear()

                    ultimo_x = x_indice

                    ultimo_y = y_indice


            elif estado == "PREPARANDO":

                if cerrada:

                    estado = "ESPERANDO"

                    tiempo_mano_abierta = None

                    puntos_dibujo.clear()


                elif abierta:

                    tiempo_transcurrido = (
                        time.time()
                        -
                        tiempo_mano_abierta
                    )


                    # Esperar 1 segundo

                    if tiempo_transcurrido >= 1.0:

                        estado = "LISTO"

                        puntos_dibujo.clear()

                        ultimo_x = x_indice

                        ultimo_y = y_indice


            elif estado == "LISTO":

                if cerrada:

                    estado = "ESPERANDO"

                    puntos_dibujo.clear()


                elif abierta:

                    distancia = (

                        (
                            x_real
                            -
                            ultimo_x
                        ) ** 2

                        +

                        (
                            y_real
                            -
                            ultimo_y
                        ) ** 2

                    ) ** 0.5


                    if (

                        distancia
                        >=
                        DISTANCIA_MINIMA

                        and

                        dentro_de_zona

                    ):

                        estado = "DIBUJANDO"

                        puntos_dibujo.clear()

                        puntos_dibujo.append([])

                        puntos_dibujo[-1].append(
                            (
                                x_indice,
                                y_indice
                            )
                        )

                        ultimo_x = x_real

                        ultimo_y = y_real


            elif estado == "DIBUJANDO":

                # Puño = terminar dibujo

                if cerrada:

                    procesar_dibujo()


                elif abierta:

                    # Dentro del cuadro

                    if dentro_de_zona:

                        if not puntos_dibujo:

                            puntos_dibujo.append([])


                        if puntos_dibujo[-1]:

                            ultimo_punto = (
                                puntos_dibujo[-1][-1]
                            )


                            distancia = (

                                (
                                    x_indice
                                    -
                                    ultimo_punto[0]
                                ) ** 2

                                +

                                (
                                    y_indice
                                    -
                                    ultimo_punto[1]
                                ) ** 2

                            ) ** 0.5

                        else:

                            distancia = (
                                DISTANCIA_MINIMA
                            )


                        if distancia >= DISTANCIA_MINIMA:

                            puntos_dibujo[-1].append(
                                (
                                    x_indice,
                                    y_indice
                                )
                            )

                            ultimo_x = x_real

                            ultimo_y = y_real


                    # Fuera del cuadro

                    else:

                        cv2.putText(
                            frame,
                            "VOLVE AL CUADRO",
                            (
                                zona_x1,
                                zona_y2 + 40
                            ),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1.0,
                            (0, 0, 255),
                            3
                        )


            # Mostrar trazo

            for trazo in puntos_dibujo:

                for i in range(
                    1,
                    len(trazo)
                ):

                    cv2.line(
                        frame,
                        trazo[i - 1],
                        trazo[i],
                        (255, 0, 0),
                        5
                    )


            # Mensajes

            if estado == "PREPARANDO":

                cv2.putText(
                    frame,
                    "Preparando...",
                    (
                        30,
                        55
                    ),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.0,
                    (255, 255, 255),
                    2
                )


            elif estado == "LISTO":

                cv2.putText(
                    frame,
                    "Listo para dibujar",
                    (
                        30,
                        55
                    ),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.0,
                    (0, 255, 0),
                    2
                )


            elif estado == "DIBUJANDO":

                if dentro_de_zona:

                    cv2.putText(
                        frame,
                        "DIBUJANDO",
                        (
                            30,
                            55
                        ),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.2,
                        (0, 255, 0),
                        3
                    )

                else:

                    cv2.putText(
                        frame,
                        "VOLVE AL CUADRO",
                        (
                            30,
                            55
                        ),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.0,
                        (0, 0, 255),
                        3
                    )


        else:

            cv2.putText(
                frame,
                "MANO NO DETECTADA",
                (
                    30,
                    55
                ),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (0, 0, 255),
                2
            )


        # Mostrar resultado temporal

        if mensaje_resultado:

            cv2.putText(
                frame,
                mensaje_resultado,
                (
                    30,
                    100
                ),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (0, 255, 0),
                2
            )


        # Mostrar cámara

        cv2.imshow(
            "EduSeñas",
            frame
        )


        tecla = cv2.waitKey(
            1
        ) & 0xFF


        # C = limpiar el intento actual

        if (
            tecla == ord("c")
            or
            tecla == ord("C")
        ):

            puntos_dibujo.clear()

            estado = "ESPERANDO"

            tiempo_mano_abierta = None

            ultimo_x = None

            ultimo_y = None

            cerrar_resultado()


        # Q = salir

        if (
            tecla == ord("q")
            or
            tecla == ord("Q")
        ):

            break


camara.release()

cv2.destroyAllWindows()