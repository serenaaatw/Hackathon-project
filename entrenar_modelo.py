import os
import pandas as pd
import numpy as np
import cv2
import tensorflow as tf


DATASET_PATH = os.path.join(
    os.path.dirname(__file__),
    "dataset_az",
    "A_Z Handwritten Data.csv"
)

NO_LETRAS_PATH = os.path.join(
    os.path.dirname(__file__),
    "dataset_no_letras"
)

MODELO_PATH = os.path.join(
    os.path.dirname(__file__),
    "model_IA",
    "letras.keras"
)


print("Cargando información del dataset A-Z...")

df = pd.read_csv(
    DATASET_PATH
)

print(
    "Cantidad de imágenes A-Z:",
    len(df)
)


etiquetas_az = df.iloc[:, 0].values.astype(
    np.int32
)

imagenes_az = df.iloc[:, 1:].values.astype(
    np.uint8
)


print(
    "Dataset A-Z cargado."
)


print("Cargando imágenes que no son letras...")


archivos_no_letras = os.listdir(
    NO_LETRAS_PATH
)

imagenes_no_letras = []


for archivo in archivos_no_letras:

    if not archivo.lower().endswith(
        (".png", ".jpg", ".jpeg")
    ):
        continue

    ruta = os.path.join(
        NO_LETRAS_PATH,
        archivo
    )

    datos = np.fromfile(
        ruta,
        dtype=np.uint8
    )

    imagen = cv2.imdecode(
        datos,
        cv2.IMREAD_GRAYSCALE
    )

    if imagen is None:
        continue

    if imagen.shape != (28, 28):

        imagen = cv2.resize(
            imagen,
            (28, 28)
        )

    imagenes_no_letras.append(
        imagen
    )


if len(imagenes_no_letras) == 0:

    raise RuntimeError(
        "No se encontraron imágenes en dataset_no_letras"
    )


imagenes_no_letras = np.array(
    imagenes_no_letras,
    dtype=np.uint8
)

etiquetas_no_letras = np.full(
    len(imagenes_no_letras),
    26,
    dtype=np.int32
)


print(
    "No letras cargadas:",
    len(imagenes_no_letras)
)


print(
    "Preparando dataset..."
)


imagenes = np.concatenate(
    [
        imagenes_az,
        imagenes_no_letras.reshape(
            len(imagenes_no_letras),
            784
        )
    ],
    axis=0
)


etiquetas = np.concatenate(
    [
        etiquetas_az,
        etiquetas_no_letras
    ]
)


indices = np.random.permutation(
    len(imagenes)
)


imagenes = imagenes[
    indices
]

etiquetas = etiquetas[
    indices
]


cantidad_entrenamiento = int(
    len(imagenes) * 0.8
)


x_entrenamiento = imagenes[
    :cantidad_entrenamiento
]

y_entrenamiento = etiquetas[
    :cantidad_entrenamiento
]


x_validacion = imagenes[
    cantidad_entrenamiento:
]

y_validacion = etiquetas[
    cantidad_entrenamiento:
]


print(
    "Entrenamiento:",
    len(x_entrenamiento)
)

print(
    "Validación:",
    len(x_validacion)
)


modelo = tf.keras.Sequential([

    tf.keras.layers.Input(
        shape=(28, 28, 1)
    ),

    tf.keras.layers.Conv2D(
        32,
        (3, 3),
        activation="relu"
    ),

    tf.keras.layers.MaxPooling2D(
        (2, 2)
    ),

    tf.keras.layers.Conv2D(
        64,
        (3, 3),
        activation="relu"
    ),

    tf.keras.layers.MaxPooling2D(
        (2, 2)
    ),

    tf.keras.layers.Flatten(),

    tf.keras.layers.Dense(
        128,
        activation="relu"
    ),

    tf.keras.layers.Dropout(
        0.3
    ),

    tf.keras.layers.Dense(
        27,
        activation="softmax"
    )
])


modelo.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)


modelo.summary()


print(
    "\nComenzando entrenamiento...\n"
)


x_entrenamiento = x_entrenamiento.reshape(
    -1,
    28,
    28,
    1
).astype(
    np.float32
) / 255.0


x_validacion = x_validacion.reshape(
    -1,
    28,
    28,
    1
).astype(
    np.float32
) / 255.0


historial = modelo.fit(
    x_entrenamiento,
    y_entrenamiento,
    validation_data=(
        x_validacion,
        y_validacion
    ),
    epochs=10,
    batch_size=128
)


os.makedirs(
    os.path.dirname(MODELO_PATH),
    exist_ok=True
)


modelo.save(
    MODELO_PATH
)


print(
    "\nEntrenamiento terminado"
)

print(
    "Modelo guardado en:",
    MODELO_PATH
)