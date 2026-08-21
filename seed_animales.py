# Carga la categoría "Animales" y sus palabras en la base de datos.
# Correr UNA VEZ (o cuando agreguen palabras/categorías nuevas) desde la raíz del proyecto: python seed_animales.py

from app import app
from models.db import db
from models.category import Category
from models.word import Word

PALABRAS_ANIMALES = [
    {"word": "PERRO", "articulo": "EL", "image_file": "perro.png"},
    {"word": "GATO", "articulo": "EL", "image_file": "gato.png"},
    {"word": "PEZ", "articulo": "EL", "image_file": "pez.png"},
    {"word": "PÁJARO", "articulo": "EL", "image_file": "pajarito.png"},
    {"word": "VACA", "articulo": "LA", "image_file": "vaca.png"},
]


def seed():
    with app.app_context():
        categoria = Category.query.filter_by(slug="animales").first()

        if categoria is None:
            categoria = Category(slug="animales", name="Animales")
            db.session.add(categoria)
            db.session.commit()
            print("Categoría 'Animales' creada.")
        else:
            print("Categoría 'Animales' ya existía, la reuso.")

        for item in PALABRAS_ANIMALES:
            existe = Word.query.filter_by(
                word=item["word"], id_category=categoria.id_category
            ).first()

            if existe:
                print(f"  {item['word']} ya existía, la salteo.")
                continue

            palabra = Word(
                word=item["word"],
                articulo=item["articulo"],
                image_file=item["image_file"],
                id_category=categoria.id_category,
            )
            db.session.add(palabra)
            print(f"  {item['word']} agregada.")

        db.session.commit()
        print("Listo.")


if __name__ == "__main__":
    seed()