async function registrarResultado(idWord, correcto) {
    try {
        const respuesta = await fetch("/juego/registrar-resultado", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                id_word: idWord,
                correcto: correcto
            })
        });

        const datos = await respuesta.json();

        if (!respuesta.ok) {
            console.error("Error registrando progreso:", datos);
            return null;
        }

        return datos.progreso;

    } catch (error) {
        console.error("Error de conexión:", error);
        return null;
    }
}