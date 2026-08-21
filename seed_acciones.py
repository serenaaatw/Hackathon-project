# Carga la categoría "Acciones" (verbos) en la base de datos.
# Pensada para más adelante poder combinar Animal + Acción (ej: "EL PERRO COME").
# Correr UNA VEZ (o cuando agreguen palabras nuevas) desde la raíz del proyecto: python seed_acciones.py

from app import app
from models.db import db
from models.category import Category
from models.word import Word

# Mismo criterio que Animales: sin artículo (los verbos no llevan EL/LA).
# image_file: todavía faltan generar estas imágenes (ver prompt sugerido).
PALABRAS_ACCIONES = [
    {"word": "COMER", "image_file": "comer.png"},
    {"word": "DORMIR", "image_file": "dormir.png"},
    {"word": "JUGAR", "image_file": "jugar.png"},
    {"word": "CORRER", "image_file": "correr.png"},
    {"word": "NADAR", "image_file": "nadar.png"},
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
                print(f"  {item['word']} ya existía, la salteo.")
                continue

            palabra = Word(
                word=item["word"],
                articulo=None,
                image_file=item["image_file"],
                id_category=categoria.id_category,
            )
            db.session.add(palabra)
            print(f"  {item['word']} agregada.")

        db.session.commit()
        print("Listo.")


if __name__ == "__main__":
    seed()