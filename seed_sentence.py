from app import app
from models.db import db
from models.word import Word
from models.sentence import Sentence
from models.sentence_word import SentenceWord


ORACIONES = [
    {"animal": "PERRO", "accion": "COMER", "verbo": "COME"},
    {"animal": "PERRO", "accion": "DORMIR", "verbo": "DUERME"},
    {"animal": "PERRO", "accion": "JUGAR", "verbo": "JUEGA"},
    {"animal": "PERRO", "accion": "CORRER", "verbo": "CORRE"},
    {"animal": "PERRO", "accion": "NADAR", "verbo": "NADA"},

    {"animal": "GATO", "accion": "COMER", "verbo": "COME"},
    {"animal": "GATO", "accion": "DORMIR", "verbo": "DUERME"},
    {"animal": "GATO", "accion": "JUGAR", "verbo": "JUEGA"},
    {"animal": "GATO", "accion": "CORRER", "verbo": "CORRE"},
    {"animal": "GATO", "accion": "NADAR", "verbo": "NADA"},

    {"animal": "PÁJARO", "accion": "COMER", "verbo": "COME"},
    {"animal": "PÁJARO", "accion": "DORMIR", "verbo": "DUERME"},
    {"animal": "PÁJARO", "accion": "JUGAR", "verbo": "JUEGA"},
    {"animal": "PÁJARO", "accion": "CORRER", "verbo": "CORRE"},
    {"animal": "PÁJARO", "accion": "NADAR", "verbo": "NADA"},

    {"animal": "PEZ", "accion": "COMER", "verbo": "COME"},
    {"animal": "PEZ", "accion": "DORMIR", "verbo": "DUERME"},
    {"animal": "PEZ", "accion": "JUGAR", "verbo": "JUEGA"},
    {"animal": "PEZ", "accion": "NADAR", "verbo": "NADA"},

    {"animal": "VACA", "accion": "COMER", "verbo": "COME"},
    {"animal": "VACA", "accion": "DORMIR", "verbo": "DUERME"},
    {"animal": "VACA", "accion": "JUGAR", "verbo": "JUEGA"},
    {"animal": "VACA", "accion": "CORRER", "verbo": "CORRE"},
    {"animal": "VACA", "accion": "NADAR", "verbo": "NADA"},
]


def buscar_palabra(nombre):
    return Word.query.filter_by(
        word=nombre
    ).first()


def crear_relacion_palabra(
    id_sentence,
    palabra,
    orden
):
    relacion = SentenceWord(
        id_sentence=id_sentence,
        id_word=palabra.id_word,
        orden=orden
    )

    db.session.add(relacion)


def seed():
    with app.app_context():

        for item in ORACIONES:

            animal = buscar_palabra(
                item["animal"]
            )

            accion = buscar_palabra(
                item["accion"]
            )

            if animal is None:
                print(
                    f"  No se encontró el animal "
                    f"'{item['animal']}', se saltea."
                )
                continue

            if accion is None:
                print(
                    f"  No se encontró la acción "
                    f"'{item['accion']}', se saltea."
                )
                continue

            existe = Sentence.query.filter_by(
                id_subject=animal.id_word,
                id_action=accion.id_word
            ).first()

            if existe:

                print(
                    f"  {item['animal']} "
                    f"{item['verbo']} ya existía, "
                    f"la salteo."
                )

                continue

            articulo = animal.articulo or "EL"

            texto = (
                f"{articulo} "
                f"{item['animal']} "
                f"{item['verbo']}"
            )

            oracion = Sentence(
                text=texto,
                id_subject=animal.id_word,
                id_action=accion.id_word
            )

            db.session.add(oracion)
            db.session.flush()

        

            crear_relacion_palabra(
                oracion.id_sentence,
                animal,
                1
            )

            crear_relacion_palabra(
                oracion.id_sentence,
                accion,
                2
            )

            print(
                f"  {texto} agregada."
            )

        db.session.commit()

        print("Listo.")


if __name__ == "__main__":
    seed()