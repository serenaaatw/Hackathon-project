import os
import cv2
import numpy as np

CARPETA = "dataset_no_letras"

os.makedirs(CARPETA, exist_ok=True)

cantidad = 5000

for i in range(cantidad):

    imagen = np.zeros(
        (28, 28),
        dtype=np.uint8
    )

    tipo = np.random.randint(0, 6)

    if tipo == 0:
        x = np.random.randint(2, 26)
        y = np.random.randint(2, 26)

        cv2.circle(
            imagen,
            (x, y),
            np.random.randint(1, 3),
            255,
            -1
        )

    elif tipo == 1:
        x1 = np.random.randint(0, 28)
        y1 = np.random.randint(0, 28)

        x2 = np.random.randint(0, 28)
        y2 = np.random.randint(0, 28)

        cv2.line(
            imagen,
            (x1, y1),
            (x2, y2),
            255,
            np.random.randint(1, 4)
        )

    elif tipo == 2:
        puntos = []

        cantidad_puntos = np.random.randint(
            3,
            10
        )

        for _ in range(cantidad_puntos):

            puntos.append([
                np.random.randint(1, 27),
                np.random.randint(1, 27)
            ])

        puntos = np.array(
            puntos,
            dtype=np.int32
        )

        cv2.polylines(
            imagen,
            [puntos],
            False,
            255,
            np.random.randint(1, 4)
        )

    elif tipo == 3:
        x1 = np.random.randint(3, 15)
        y1 = np.random.randint(3, 15)

        x2 = np.random.randint(
            x1 + 2,
            28
        )

        y2 = np.random.randint(
            y1 + 2,
            28
        )

        cv2.rectangle(
            imagen,
            (x1, y1),
            (x2, y2),
            255,
            np.random.randint(1, 4)
        )

    elif tipo == 4:
        centro = (
            np.random.randint(8, 20),
            np.random.randint(8, 20)
        )

        cv2.circle(
            imagen,
            centro,
            np.random.randint(3, 10),
            255,
            np.random.randint(1, 4)
        )

    else:
        for _ in range(
            np.random.randint(2, 8)
        ):

            x1 = np.random.randint(0, 28)
            y1 = np.random.randint(0, 28)

            x2 = np.random.randint(0, 28)
            y2 = np.random.randint(0, 28)

            cv2.line(
                imagen,
                (x1, y1),
                (x2, y2),
                255,
                np.random.randint(1, 4)
            )

    nombre = os.path.join(
        CARPETA,
        f"no_letra_{i}.png"
    )

    cv2.imwrite(
        nombre,
        imagen
    )

print(
    f"Se crearon {cantidad} imágenes."
)