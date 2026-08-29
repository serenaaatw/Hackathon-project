import tensorflow as tf
import tensorflow_datasets as tfds
import matplotlib.pyplot as plt


# Cargar EMNIST Letters
dataset, info = tfds.load(
    "emnist/letters",
    split="train",
    as_supervised=True,
    with_info=True
)


# Las etiquetas originales de EMNIST van de 1 a 26
# Las convertimos a 0 a 25
def preparar(imagen, etiqueta):

    imagen = tf.cast(
        imagen,
        tf.float32
    ) / 255.0

    etiqueta = etiqueta - 1

    return imagen, etiqueta


dataset = dataset.map(preparar)


# Tomamos algunos ejemplos
ejemplos = []

for imagen, etiqueta in dataset.take(104):

    ejemplos.append(
        (
            imagen.numpy(),
            etiqueta.numpy()
        )
    )


LETRAS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


# Mostrar 104 imágenes
fig, axes = plt.subplots(
    13,
    8,
    figsize=(12, 18)
)


for ax, (imagen, etiqueta) in zip(
    axes.flat,
    ejemplos
):

    ax.imshow(
        imagen,
        cmap="gray"
    )

    ax.set_title(
        f"{LETRAS[etiqueta]} ({etiqueta})"
    )

    ax.axis("off")


plt.tight_layout()

plt.show()