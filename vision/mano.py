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


camara = cv2.VideoCapture(0)

camara.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
camara.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)


model_path = os.path.join(
    os.path.dirname(__file__),
    "hand_landmarker.task"
)

with open(model_path, "rb") as archivo:
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


puntos_dibujo = []

estado = "ESPERANDO"

tiempo_mano_abierta = None

ultimo_x = None
ultimo_y = None

SUAVIZADO = 0.50

DISTANCIA_MINIMA = 3

VENTANA_RESULTADO = "Dibujo para IA"


LETRAS_EJERCICIO = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

indice_letra = 0

LETRA_OBJETIVO = LETRAS_EJERCICIO[indice_letra]


intentos = 0

buenos = 0

MAX_INTENTOS = 10

BUENOS_NECESARIOS = 3


resultados_letras = {}

mensaje_resultado = ""

tiempo_mensaje = None


VENTANA = "EduSeñas"

salir = False


def cerrar_programa():
    global salir
    salir = True


def manejar_click(evento, x, y, flags, parametro):

    if evento == cv2.EVENT_LBUTTONDOWN:

        alto, ancho = parametro

        boton_x1 = ancho - 250
        boton_y1 = alto - 75
        boton_x2 = ancho - 40
        boton_y2 = alto - 20

        if (
            boton_x1 <= x <= boton_x2
            and
            boton_y1 <= y <= boton_y2
        ):
            cerrar_programa()


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


    mostrar_dibujo_convertido(
        imagen_ia
    )


    letra_detectada, confianza = reconocer_letra(
        imagen_ia
    )


    similitud = comparar_con_letra(
        imagen_ia,
        LETRA_OBJETIVO
    )


    if similitud >= 70:

        calificacion = "BUENO"

    elif similitud >= 50:

        calificacion = "MEDIO"

    else:

        calificacion = "MALO"


    intentos += 1


    if (
        calificacion == "BUENO"
        or
        calificacion == "MEDIO"
    ):

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

    indice_arriba = mano[8].y < mano[6].y

    medio_arriba = mano[12].y < mano[10].y

    anular_arriba = mano[16].y < mano[14].y

    menique_arriba = mano[20].y < mano[18].y

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

    indice_cerrado = mano[8].y > mano[6].y

    medio_cerrado = mano[12].y > mano[10].y

    anular_cerrado = mano[16].y > mano[14].y

    menique_cerrado = mano[20].y > mano[18].y

    return (
        indice_cerrado
        and
        medio_cerrado
        and
        anular_cerrado
        and
        menique_cerrado
    )


def dibujar_mano(frame, mano, ancho, alto):

    puntos = []

    for punto in mano:

        x = int(punto.x * ancho)
        y = int(punto.y * alto)

        puntos.append([x, y])


    puntos = cv2.convexHull(
        __import__("numpy").array(
            puntos,
            dtype="int32"
        )
    )


    capa = frame.copy()

    cv2.fillConvexPoly(
        capa,
        puntos,
        (255, 190, 0)
    )


    frame[:] = cv2.addWeighted(
        capa,
        0.55,
        frame,
        0.45,
        0
    )


    conexiones = [
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 4),

        (0, 5),
        (5, 6),
        (6, 7),
        (7, 8),

        (5, 9),
        (9, 10),
        (10, 11),
        (11, 12),

        (9, 13),
        (13, 14),
        (14, 15),
        (15, 16),

        (13, 17),
        (17, 18),
        (18, 19),
        (19, 20),

        (0, 17)
    ]


    for inicio, fin in conexiones:

        x1, y1 = puntos_mano_real(
            mano[inicio],
            ancho,
            alto
        )

        x2, y2 = puntos_mano_real(
            mano[fin],
            ancho,
            alto
        )

        cv2.line(
            frame,
            (x1, y1),
            (x2, y2),
            (0, 255, 255),
            4
        )


def puntos_mano_real(punto, ancho, alto):

    return (
        int(punto.x * ancho),
        int(punto.y * alto)
    )


cv2.namedWindow(
    VENTANA,
    cv2.WINDOW_NORMAL
)

cv2.setWindowProperty(
    VENTANA,
    cv2.WND_PROP_FULLSCREEN,
    cv2.WINDOW_FULLSCREEN
)


with vision.HandLandmarker.create_from_options(
    opciones
) as detector:

    tiempo_inicio = time.time()

    while not salir:

        correcto, frame = camara.read()

        if not correcto:
            break


        frame = cv2.flip(
            frame,
            1
        )


        alto, ancho, _ = frame.shape


        fondo = cv2.GaussianBlur(
            frame,
            (51, 51),
            0
        )


        overlay = fondo.copy()


        cv2.rectangle(
            overlay,
            (0, 0),
            (ancho, alto),
            (80, 45, 20),
            -1
        )


        frame = cv2.addWeighted(
            overlay,
            0.35,
            fondo,
            0.65,
            0
        )


        margen_x = int(
            ancho * 0.17
        )

        margen_y = int(
            alto * 0.14
        )


        zona_x1 = margen_x

        zona_y1 = margen_y

        zona_x2 = int(
            ancho * 0.72
        )

        zona_y2 = alto - 120


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
            4
        )


        cv2.rectangle(
            frame,
            (
                zona_x1 + 8,
                zona_y1 + 8
            ),
            (
                zona_x2 - 8,
                zona_y2 - 8
            ),
            (255, 190, 0),
            2
        )


        if not ejercicio_terminado():

            cv2.putText(
                frame,
                f"{LETRA_OBJETIVO}",
                (
                    35,
                    115
                ),
                cv2.FONT_HERSHEY_SIMPLEX,
                3.0,
                (255, 220, 50),
                7
            )


            cv2.putText(
                frame,
                f"BUENOS  {buenos}/{BUENOS_NECESARIOS}",
                (
                    35,
                    alto - 75
                ),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (255, 255, 255),
                3
            )


            cv2.putText(
                frame,
                f"INTENTOS  {intentos}/{MAX_INTENTOS}",
                (
                    330,
                    alto - 75
                ),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (255, 255, 255),
                3
            )


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


        if resultado.hand_landmarks:

            mano = resultado.hand_landmarks[0]


            dibujar_mano(
                frame,
                mano,
                ancho,
                alto
            )


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


            cv2.circle(
                frame,
                (
                    x_real,
                    y_real
                ),
                13,
                (0, 0, 255),
                -1
            )


            cv2.circle(
                frame,
                (
                    x_real,
                    y_real
                ),
                18,
                (255, 255, 255),
                2
            )


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

                if cerrada:

                    procesar_dibujo()


                elif abierta:

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


                    else:

                        cv2.putText(
                            frame,
                            "VOLVE AL CUADRO",
                            (
                                zona_x1,
                                zona_y2 + 45
                            ),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1.0,
                            (0, 80, 255),
                            3
                        )


            for trazo in puntos_dibujo:

                for i in range(
                    1,
                    len(trazo)
                ):

                    cv2.line(
                        frame,
                        trazo[i - 1],
                        trazo[i],
                        (255, 120, 0),
                        7
                    )


            if estado == "PREPARANDO":

                cv2.putText(
                    frame,
                    "PREPARANDO...",
                    (
                        zona_x1,
                        zona_y1 - 20
                    ),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,
                    (255, 255, 255),
                    3
                )


            elif estado == "LISTO":

                cv2.putText(
                    frame,
                    "DIBUJA!",
                    (
                        zona_x1,
                        zona_y1 - 20
                    ),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,
                    (0, 255, 255),
                    3
                )


            elif estado == "DIBUJANDO":

                cv2.putText(
                    frame,
                    "DIBUJANDO...",
                    (
                        zona_x1,
                        zona_y1 - 20
                    ),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,
                    (0, 255, 255),
                    3
                )


        else:

            cv2.putText(
                frame,
                "MOSTRA TU MANO",
                (
                    zona_x1,
                    zona_y1 - 20
                ),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (255, 255, 255),
                3
            )


        if mensaje_resultado:

            cv2.putText(
                frame,
                mensaje_resultado,
                (
                    zona_x1,
                    75
                ),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 120),
                3
            )


        panel_x1 = int(ancho * 0.76)

        panel_y1 = 120

        panel_x2 = ancho - 40

        panel_y2 = 390


        cv2.rectangle(
            frame,
            (
                panel_x1,
                panel_y1
            ),
            (
                panel_x2,
                panel_y2
            ),
            (40, 40, 70),
            -1
        )


        cv2.rectangle(
            frame,
            (
                panel_x1,
                panel_y1
            ),
            (
                panel_x2,
                panel_y2
            ),
            (255, 220, 50),
            4
        )


        cv2.putText(
            frame,
            "VIDEO",
            (
                panel_x1 + 70,
                panel_y1 + 45
            ),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.0,
            (255, 255, 255),
            3
        )


        cv2.putText(
            frame,
            "Mira como",
            (
                panel_x1 + 35,
                panel_y1 + 120
            ),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (255, 255, 255),
            2
        )


        cv2.putText(
            frame,
            "hacer la seña",
            (
                panel_x1 + 20,
                panel_y1 + 155
            ),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (255, 255, 255),
            2
        )


        boton_x1 = ancho - 250
        boton_y1 = alto - 75
        boton_x2 = ancho - 40
        boton_y2 = alto - 20


        cv2.rectangle(
            frame,
            (
                boton_x1,
                boton_y1
            ),
            (
                boton_x2,
                boton_y2
            ),
            (50, 70, 230),
            -1
        )


        cv2.rectangle(
            frame,
            (
                boton_x1,
                boton_y1
            ),
            (
                boton_x2,
                boton_y2
            ),
            (255, 255, 255),
            3
        )


        cv2.putText(
            frame,
            "SALIR",
            (
                boton_x1 + 65,
                boton_y1 + 38
            ),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            3
        )


        cv2.imshow(
            VENTANA,
            frame
        )


        tecla = cv2.waitKey(1) & 0xFF


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


        if (
            tecla == ord("q")
            or
            tecla == ord("Q")
        ):

            break


camara.release()

cv2.destroyAllWindows()