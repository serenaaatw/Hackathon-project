from app import app
from models.db import db
from models.fonemas import Fonema

FONEMAS = [
    {
        "fonema": "A",
        "imagen": "a.png",
        "sonido": "a.wav"
    },
    {
        "fonema": "E",
        "imagen": "e.png",
        "sonido": "e.wav"
    },
    {
        "fonema": "I",
        "imagen": "i.png",
        "sonido": "i.wav"
    },
    {
        "fonema": "O",
        "imagen": "o.png",
        "sonido": "o.wav"
    },
    {
        "fonema": "U",
        "imagen": "u.png",
        "sonido": "u.wav"
    },
    {
        "fonema": "P",
        "imagen": "p.png",
        "sonido": "p.wav"
    },
    {
        "fonema": "B",
        "imagen": "b.png",
        "sonido": "b.wav"
    },
    {
        "fonema": "T",
        "imagen": "t.png",
        "sonido": "t.wav"
    },
    {
        "fonema": "D",
        "imagen": "d.png",
        "sonido": "d.wav"
    },
    {
        "fonema": "K",
        "imagen": "k.png",
        "sonido": "k.wav"
    },
    {
        "fonema": "G",
        "imagen": "g.png",
        "sonido": "g.wav"
    },
    {
        "fonema": "F",
        "imagen": "f.png",
        "sonido": "f.wav"
    },
    {
        "fonema": "S",
        "imagen": "s.png",
        "sonido": "s.wav"
    },
    {
        "fonema": "J",
        "imagen": "j.png",
        "sonido": "j.wav"
    },
    {
        "fonema": "CH",
        "imagen": "ch.png",
        "sonido": "ch.wav"
    },
    {
        "fonema": "M",
        "imagen": "m.png",
        "sonido": "m.wav"
    },
    {
        "fonema": "N",
        "imagen": "n.png",
        "sonido": "n.wav"
    },
    {
        "fonema": "Ñ",
        "imagen": "ñ.png",
        "sonido": "ñ.wav"
    },
    {
        "fonema": "L",
        "imagen": "l.png",
        "sonido": "l.wav"
    },
    {
        "fonema": "LL",
        "imagen": "ll.png",
        "sonido": "ll.wav"
    },
    {
        "fonema": "R",
        "imagen": "r.png",
        "sonido": "r.wav"
    },
    {
        "fonema": "RR",
        "imagen": "rr.png",
        "sonido": "rr.wav"
    },
    {
        "fonema": "Y",
        "imagen": "y.png",
        "sonido": "y.wav"
    },
    {
        "fonema": "W",
        "imagen": "w.png",
        "sonido": "w.wav"
    }
]


def seed():
    with app.app_context():

        for item in FONEMAS:

            existe = Fonema.query.filter_by(
                fonema=item["fonema"]
            ).first()

            if existe:

                existe.imagen = item["imagen"]
                existe.sonido = item["sonido"]

                print(
                    f"  {item['fonema']} actualizado "
                    f"(sonido: {item['sonido']})"
                )

            else:

                fonema = Fonema(
                    fonema=item["fonema"],
                    imagen=item["imagen"],
                    sonido=item["sonido"]
                )

                db.session.add(fonema)

                print(
                    f"  {item['fonema']} agregado "
                    f"(sonido: {item['sonido']})"
                )

        db.session.commit()
        print("Listo.")


if __name__ == "__main__":
    seed()
