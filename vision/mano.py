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


# ============================================================
# CÁMARA
# ============================================================

camara = cv2.VideoCapture(0)

camara.set(
    cv2.CAP_PROP_FRAME_WIDTH,
    1280
)

camara.set(
    cv2.CAP_PROP_FRAME_HEIGHT,
    720
)


# ============================================================
# MODELO MEDIAPIPE
# ============================================================

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


# ============================================================
# VARIABLES
# ============================================================

puntos_dibujo = []

estado = "ESPERANDO"

tiempo_mano_abierta = None

ultimo_x = None
ultimo_y = None

SUAVIZADO = 0.50

DISTANCIA_MINIMA = 3

VENTANA_RESULTADO = "Dibujo para IA"

LETRA_OBJETIVO = "T"


# ============================================================
# MOSTRAR DIBUJO
# ============================================================

def mostrar_dibujo_convertido(
    imagen
):

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

    # Lo ponemos a la derecha

    cv2.moveWindow(
        VENTANA_RESULTADO,
        1300,
        150
    )

    cv2.imshow(
        VENTANA_RESULTADO,
        imagen_grande
    )


# ============================================================
# CERRAR RESULTADO
# ============================================================

def cerrar_resultado():

    try:

        cv2.destroyWindow(
            VENTANA_RESULTADO
        )

    except:

        pass


# ============================================================
# PROCESAR DIBUJO
# ============================================================

def procesar_dibujo():

    global puntos_dibujo
    global estado
    global ultimo_x
    global ultimo_y
    global tiempo_mano_abierta


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


    # Reconocimiento

    letra_detectada, confianza = reconocer_letra(
        imagen_ia
    )


    # Similitud con la letra que pedimos

    similitud = comparar_con_letra(
        imagen_ia,
        LETRA_OBJETIVO
    )


    # ========================================================
    # RESULTADO
    # ========================================================
    if similitud >= 70:
        calificacion = "BUENO"
    elif similitud >= 50:
        calificacion = "MEDIO"
    else:
        calificacion = "MALO"
    print(
        f"Similitud: {similitud:.2f}% | Calificación: {calificacion} ")
    #

    puntos_dibujo.clear()

    estado = "ESPERANDO"

    tiempo_mano_abierta = None

    ultimo_x = None
    ultimo_y = None


# ============================================================
# DETECTAR MANO ABIERTA
# ============================================================

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


# ============================================================
# DETECTAR PUÑO
# ============================================================

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


# ============================================================
# INICIAR DETECTOR
# ============================================================

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


        # ====================================================
        # CUADRO DE DIBUJO
        # ====================================================

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


        cv2.putText(
            frame,
            f"Letra: {LETRA_OBJETIVO}",
            (
                30,
                alto - 30
            ),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.0,
            (255, 255, 255),
            2
        )


        # ====================================================
        # MEDIAPIPE
        # ====================================================

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


        # ====================================================
        # MANO DETECTADA
        # ====================================================

        if resultado.hand_landmarks:

            mano = resultado.hand_landmarks[0]


            # -----------------------------------------------
            # PUNTO DEL ÍNDICE
            # -----------------------------------------------

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


            # -----------------------------------------------
            # SUAVIZADO
            # -----------------------------------------------

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


            # -----------------------------------------------
            # PUNTO ROJO
            # -----------------------------------------------

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


            # -----------------------------------------------
            # DENTRO DEL CUADRO
            # -----------------------------------------------

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


            # =================================================
            # ESPERANDO
            # =================================================

            if estado == "ESPERANDO":

                if abierta:

                    cerrar_resultado()

                    estado = "PREPARANDO"

                    tiempo_mano_abierta = time.time()

                    puntos_dibujo.clear()

                    ultimo_x = x_indice

                    ultimo_y = y_indice


            # =================================================
            # PREPARANDO
            # =================================================

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


            # =================================================
            # LISTO
            # =================================================

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


            # =================================================
            # DIBUJANDO
            # =================================================

            elif estado == "DIBUJANDO":

                # ---------------------------------------------
                # PUÑO = TERMINAR
                # ---------------------------------------------

                if cerrada:

                    procesar_dibujo()


                elif abierta:

                    # -----------------------------------------
                    # DENTRO DEL CUADRO
                    # -----------------------------------------

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


                        if (
                            distancia
                            >=
                            DISTANCIA_MINIMA
                        ):

                            puntos_dibujo[-1].append(
                                (
                                    x_indice,
                                    y_indice
                                )
                            )

                            ultimo_x = x_real

                            ultimo_y = y_real


                    # -----------------------------------------
                    # FUERA DEL CUADRO
                    # -----------------------------------------

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


            # =================================================
            # MOSTRAR TRAZO
            # =================================================

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


            # =================================================
            # MENSAJES
            # =================================================

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


        # ====================================================
        # SIN MANO
        # ====================================================

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


        # ====================================================
        # MOSTRAR CÁMARA
        # ====================================================

        cv2.imshow(
            "EduSeñas",
            frame
        )


        tecla = cv2.waitKey(
            1
        ) & 0xFF


        # ====================================================
        # C = LIMPIAR
        # ====================================================

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


        # ====================================================
        # Q = SALIR
        # ====================================================

        if (
            tecla == ord("q")
            or
            tecla == ord("Q")
        ):

            break


# ============================================================
# CERRAR
# ============================================================

camara.release()

cv2.destroyAllWindows()