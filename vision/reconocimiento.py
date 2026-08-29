import os
import numpy as np
import tensorflow as tf
import cv2


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

MODELO_PATH = os.path.join(
    BASE_DIR,
    "model_IA",
    "letras.keras"
)


modelo = tf.keras.models.load_model(
    MODELO_PATH
)


LETRAS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
CLASE_NO_LETRA = 26


def preparar_imagen(imagen):

    imagen = np.array(
        imagen,
        dtype=np.float32
    )

    if imagen.ndim == 3:
        imagen = np.squeeze(imagen)

    if imagen.ndim != 2:
        raise ValueError(
            f"Forma incorrecta: {imagen.shape}"
        )

    if imagen.max() > 1:
        imagen = imagen / 255.0

    imagen = np.clip(
        imagen,
        0,
        1
    )

    imagen = cv2.resize(
        imagen,
        (28, 28),
        interpolation=cv2.INTER_AREA
    )

    return imagen.reshape(
        1,
        28,
        28,
        1
    )


def convertir_trazo_a_imagen(
    puntos_dibujo
):

    if not puntos_dibujo:
        return None

    puntos = []

    for trazo in puntos_dibujo:
        for punto in trazo:
            puntos.append(punto)

    if not puntos:
        return None

    puntos = np.array(
        puntos,
        dtype=np.float32
    )

    x_min = np.min(
        puntos[:, 0]
    )

    x_max = np.max(
        puntos[:, 0]
    )

    y_min = np.min(
        puntos[:, 1]
    )

    y_max = np.max(
        puntos[:, 1]
    )

    ancho = max(
        x_max - x_min,
        1
    )

    alto = max(
        y_max - y_min,
        1
    )

    tamaño = 180

    escala = min(
        tamaño / ancho,
        tamaño / alto
    )

    imagen = np.zeros(
        (200, 200),
        dtype=np.uint8
    )

    trazos_nuevos = []

    for trazo in puntos_dibujo:

        nuevo = []

        for x, y in trazo:

            nx = (
                x - x_min
            ) * escala

            ny = (
                y - y_min
            ) * escala

            nuevo.append(
                (
                    int(nx),
                    int(ny)
                )
            )

        trazos_nuevos.append(
            nuevo
        )

    todos = []

    for trazo in trazos_nuevos:
        todos.extend(trazo)

    if todos:

        todos_np = np.array(
            todos
        )

        centro_x = (
            np.min(todos_np[:, 0])
            +
            np.max(todos_np[:, 0])
        ) / 2

        centro_y = (
            np.min(todos_np[:, 1])
            +
            np.max(todos_np[:, 1])
        ) / 2

    else:

        centro_x = 100
        centro_y = 100

    desplazamiento_x = int(
        100 - centro_x
    )

    desplazamiento_y = int(
        100 - centro_y
    )

    for trazo in trazos_nuevos:

        if len(trazo) == 1:

            x, y = trazo[0]

            cv2.circle(
                imagen,
                (
                    x + desplazamiento_x,
                    y + desplazamiento_y
                ),
                5,
                255,
                -1
            )

        else:

            for i in range(
                1,
                len(trazo)
            ):

                p1 = (
                    trazo[i - 1][0]
                    + desplazamiento_x,

                    trazo[i - 1][1]
                    + desplazamiento_y
                )

                p2 = (
                    trazo[i][0]
                    + desplazamiento_x,

                    trazo[i][1]
                    + desplazamiento_y
                )

                cv2.line(
                    imagen,
                    p1,
                    p2,
                    255,
                    8,
                    cv2.LINE_AA
                )

    imagen = cv2.resize(
        imagen,
        (28, 28),
        interpolation=cv2.INTER_AREA
    )

    return imagen


def reconocer_letra(imagen):

    entrada = preparar_imagen(
        imagen
    )

    prediccion = modelo.predict(
        entrada,
        verbose=0
    )[0]

    indice = int(
        np.argmax(
            prediccion
        )
    )

    confianza = (
        float(
            prediccion[indice]
        )
        * 100
    )

    if indice == CLASE_NO_LETRA:

        letra = "NO ES LETRA"

    elif indice < len(LETRAS):

        letra = LETRAS[indice]

    else:

        letra = "NO ES LETRA"

    return letra, confianza


def crear_letra_ideal(
    letra
):

    imagen = np.zeros(
        (200, 200),
        dtype=np.uint8
    )

    letra = letra.upper()

    if letra == "T":

        cv2.line(
            imagen,
            (35, 45),
            (165, 45),
            255,
            12,
            cv2.LINE_AA
        )

        cv2.line(
            imagen,
            (100, 45),
            (100, 165),
            255,
            12,
            cv2.LINE_AA
        )

    elif letra == "O":

        cv2.ellipse(
            imagen,
            (100, 105),
            (65, 75),
            0,
            0,
            360,
            255,
            12,
            cv2.LINE_AA
        )

    elif letra == "A":

        cv2.line(
            imagen,
            (45, 165),
            (100, 40),
            255,
            12,
            cv2.LINE_AA
        )

        cv2.line(
            imagen,
            (100, 40),
            (155, 165),
            255,
            12,
            cv2.LINE_AA
        )

        cv2.line(
            imagen,
            (65, 115),
            (135, 115),
            255,
            12,
            cv2.LINE_AA
        )

    elif letra == "L":

        cv2.line(
            imagen,
            (65, 40),
            (65, 165),
            255,
            12,
            cv2.LINE_AA
        )

        cv2.line(
            imagen,
            (65, 165),
            (160, 165),
            255,
            12,
            cv2.LINE_AA
        )

    elif letra == "E":

        cv2.line(
            imagen,
            (65, 40),
            (65, 165),
            255,
            12,
            cv2.LINE_AA
        )

        cv2.line(
            imagen,
            (65, 40),
            (160, 40),
            255,
            12,
            cv2.LINE_AA
        )

        cv2.line(
            imagen,
            (65, 102),
            (145, 102),
            255,
            12,
            cv2.LINE_AA
        )

        cv2.line(
            imagen,
            (65, 165),
            (160, 165),
            255,
            12,
            cv2.LINE_AA
        )

    else:

        fuente = cv2.FONT_HERSHEY_SIMPLEX

        cv2.putText(
            imagen,
            letra,
            (45, 155),
            fuente,
            4.0,
            255,
            10,
            cv2.LINE_AA
        )

    return imagen


def normalizar_mascara(
    imagen
):

    imagen = np.array(
        imagen,
        dtype=np.uint8
    )

    _, mascara = cv2.threshold(
        imagen,
        40,
        255,
        cv2.THRESH_BINARY
    )

    puntos = cv2.findNonZero(
        mascara
    )

    if puntos is None:

        return np.zeros(
            (28, 28),
            dtype=np.uint8
        )

    x, y, w, h = cv2.boundingRect(
        puntos
    )

    recorte = mascara[
        y:y+h,
        x:x+w
    ]

    tamaño = 22

    escala = min(
        tamaño / max(w, 1),
        tamaño / max(h, 1)
    )

    nuevo_w = max(
        1,
        int(w * escala)
    )

    nuevo_h = max(
        1,
        int(h * escala)
    )

    recorte = cv2.resize(
        recorte,
        (
            nuevo_w,
            nuevo_h
        ),
        interpolation=cv2.INTER_AREA
    )

    salida = np.zeros(
        (28, 28),
        dtype=np.uint8
    )

    inicio_x = (
        28 - nuevo_w
    ) // 2

    inicio_y = (
        28 - nuevo_h
    ) // 2

    salida[
        inicio_y:inicio_y+nuevo_h,
        inicio_x:inicio_x+nuevo_w
    ] = recorte

    return salida


def comparar_forma(
    dibujo,
    letra_objetivo
):

    ideal = crear_letra_ideal(
        letra_objetivo
    )

    dibujo = normalizar_mascara(
        dibujo
    )

    ideal = normalizar_mascara(
        ideal
    )

    dibujo_f = (
        dibujo.astype(
            np.float32
        )
        /
        255.0
    )

    ideal_f = (
        ideal.astype(
            np.float32
        )
        /
        255.0
    )

    diferencia = np.mean(
        np.abs(
            dibujo_f
            -
            ideal_f
        )
    )

    similitud_pixel = (
        1.0
        -
        diferencia
    ) * 100

    contorno_dibujo = cv2.Canny(
        dibujo,
        50,
        150
    )

    contorno_ideal = cv2.Canny(
        ideal,
        50,
        150
    )

    diferencia_contorno = np.mean(
        np.abs(
            contorno_dibujo.astype(
                np.float32
            )
            -
            contorno_ideal.astype(
                np.float32
            )
        )
    ) / 255.0

    similitud_contorno = (
        1.0
        -
        diferencia_contorno
    ) * 100

    similitud = (
        similitud_pixel * 0.55
        +
        similitud_contorno * 0.45
    )

    return max(
        0.0,
        min(
            100.0,
            float(similitud)
        )
    )


def analizar_t(
    imagen
):

    mascara = normalizar_mascara(
        imagen
    )

    puntos = cv2.findNonZero(
        mascara
    )

    if puntos is None:

        return 0.0

    x, y, w, h = cv2.boundingRect(
        puntos
    )

    if w <= 0 or h <= 0:

        return 0.0

    imagen_f = mascara > 40

    altura, anchura = imagen_f.shape

    total_pixeles = np.sum(
        imagen_f
    )

    if total_pixeles < 8:

        return 0.0

    # --------------------------------------------------------
    # Buscar zona horizontal superior
    # --------------------------------------------------------

    zona_superior = imagen_f[
        0:max(
            1,
            int(altura * 0.40)
        ),
        :
    ]

    columnas_superior = np.sum(
        zona_superior,
        axis=0
    )

    columnas_con_trazo = np.where(
        columnas_superior >= 1
    )[0]

    if len(columnas_con_trazo) == 0:

        horizontal_score = 0.0

    else:

        horizontal_ancho = (
            columnas_con_trazo.max()
            -
            columnas_con_trazo.min()
            +
            1
        )

        proporcion_horizontal = (
            horizontal_ancho
            /
            anchura
        )

        horizontal_score = min(
            100.0,
            proporcion_horizontal * 100
        )

    # --------------------------------------------------------
    # Buscar palo vertical central
    # --------------------------------------------------------

    zona_central = imagen_f[
        int(altura * 0.20):,
        :
    ]

    columnas_centrales = np.sum(
        zona_central,
        axis=0
    )

    columna_mas_cargada = int(
        np.argmax(
            columnas_centrales
        )
    )

    centro_esperado = (
        anchura / 2
    )

    distancia_centro = abs(
        columna_mas_cargada
        -
        centro_esperado
    )

    centro_score = max(
        0.0,
        100.0
        -
        (
            distancia_centro
            /
            max(anchura / 2, 1)
            *
            100
        )
    )

    # Cantidad de filas donde aparece
    # el trazo central.

    umbral_vertical = max(
        1,
        int(anchura * 0.08)
    )

    filas_verticales = np.sum(
        zona_central[
            :,
            max(
                0,
                columna_mas_cargada - 1
            ):
            min(
                anchura,
                columna_mas_cargada + 2
            )
        ],
        axis=1
    )

    filas_con_vertical = np.sum(
        filas_verticales >= 1
    )

    proporcion_vertical = (
        filas_con_vertical
        /
        max(
            zona_central.shape[0],
            1
        )
    )

    vertical_score = min(
        100.0,
        proporcion_vertical * 130
    )

    # --------------------------------------------------------
    # Una T necesita DOS partes
    # --------------------------------------------------------

    estructura = (
        horizontal_score * 0.45
        +
        vertical_score * 0.40
        +
        centro_score * 0.15
    )

    # --------------------------------------------------------
    # Si prácticamente es una línea vertical,
    # la penalizamos fuertemente.
    # --------------------------------------------------------

    proporcion_ancho = (
        w /
        max(h, 1)
    )

    if proporcion_ancho < 0.35:

        estructura *= 0.25

    elif proporcion_ancho < 0.50:

        estructura *= 0.50

    elif proporcion_ancho < 0.65:

        estructura *= 0.75

    return max(
        0.0,
        min(
            100.0,
            float(estructura)
        )
    )


def comparar_con_letra(
    imagen,
    letra_objetivo
):

    entrada = preparar_imagen(
        imagen
    )

    imagen_28 = (
        entrada[0, :, :, 0]
        * 255
    ).astype(
        np.uint8
    )

    pixeles = np.sum(
        imagen_28 > 30
    )

    if pixeles < 8:

        return 0.0

    prediccion = modelo.predict(
        entrada,
        verbose=0
    )[0]

    indice_objetivo = LETRAS.index(
        letra_objetivo.upper()
    )

    probabilidad = (
        float(
            prediccion[
                indice_objetivo
            ]
        )
        * 100
    )

    forma = comparar_forma(
        imagen_28,
        letra_objetivo
    )

    ys, xs = np.where(
        imagen_28 > 30
    )

    if len(xs) == 0:

        return 0.0

    ancho = (
        xs.max()
        -
        xs.min()
        +
        1
    )

    alto = (
        ys.max()
        -
        ys.min()
        +
        1
    )

    if (
        ancho <= 4
        and
        alto <= 4
    ):

        return min(
            10.0,
            probabilidad
        )

    # --------------------------------------------------------
    # Para T usamos estructura especial
    # --------------------------------------------------------

    if letra_objetivo.upper() == "T":

        estructura_t = analizar_t(
            imagen_28
        )

        # La estructura manda.
        # La IA ayuda, pero no decide sola.

        similitud = (
            probabilidad * 0.20
            +
            forma * 0.30
            +
            estructura_t * 0.50
        )

        # Una T necesita una barra horizontal.
        # Si no existe, no puede ser buena.

        if estructura_t < 25:

            similitud *= 0.35

        elif estructura_t < 40:

            similitud *= 0.60

        elif estructura_t < 55:

            similitud *= 0.80

    else:

        similitud = (
            probabilidad * 0.35
            +
            forma * 0.65
        )

    indice_mayor = int(
        np.argmax(
            prediccion
        )
    )

    if (
        indice_mayor != indice_objetivo
        and
        indice_mayor != CLASE_NO_LETRA
    ):

        similitud *= 0.70

    similitud = max(
        0.0,
        min(
            100.0,
            similitud
        )
    )

    return float(
        similitud
    )