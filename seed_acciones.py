# Carga la categoría "Acciones" (verbos) en la base de datos.
# Pensada para más adelante poder combinar Animal + Acción (ej: "EL PERRO COME").
# Correr desde la raíz del proyecto: python seed_acciones.py
# (Se puede correr las veces que haga falta: actualiza los datos si la palabra ya existía.)

from app import app
from models.db import db
from models.category import Category
from models.word import Word

# Sin artículo (los verbos no llevan EL/LA).
# lsa_video_file: None = todavía no está grabado ese video.
PALABRAS_ACCIONES = [
    {
        "word": "COMER",
        "image_file": "comer.png",
        "lsa_video_file": "comer.mp4",
    },
    {
        "word": "DORMIR",
        "image_file": "dormir.png",
        "lsa_video_file": "dormir.mp4",
    },
    {
        "word": "JUGAR",
        "image_file": "jugar.png",
        "lsa_video_file": "jugar.mp4",
    },

]


def seed():
    with app.app_context():
        categoria = Category.query.filter_by(slug="acciones").first()

        if categoria is None:
            categoria = Category(slug="acciones", name="Acciones")
            db.session.add(categoria)
            db.session.commit()
            print("Categoría 'Acciones' creada.")
        else:
            print("Categoría 'Acciones' ya existía, la reuso.")

        for item in PALABRAS_ACCIONES:

            existe = Word.query.filter_by(
                word=item["word"], id_category=categoria.id_category
            ).first()

            if existe:

                # Actualizamos los datos aunque la palabra
                # ya exista en la base de datos.
                existe.image_file = item["image_file"]
                existe.lsa_video_file = item["lsa_video_file"]

                print(
                    f"  {item['word']} actualizada "
                    f"(video: {item['lsa_video_file']})"
                )

            else:

                palabra = Word(
                    word=item["word"],
                    articulo=None,
                    image_file=item["image_file"],
                    lsa_video_file=item["lsa_video_file"],
                    id_category=categoria.id_category,
                )

                db.session.add(palabra)

                print(
                    f"  {item['word']} agregada "
                    f"(video: {item['lsa_video_file']})"
                )

        db.session.commit()
        print("Listo.")


if __name__ == "__main__":
    seed()