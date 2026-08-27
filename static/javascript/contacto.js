(function () {
"use strict";


const els = {

    form:
        document.getElementById("contactForm"),

    motivo:
        document.getElementById("motivo"),

    email:
        document.getElementById("email"),

    mensaje:
        document.getElementById("mensaje"),

    feedback:
        document.getElementById("contactFeedback"),

    boton:
        document.getElementById("btnEnviarContacto")

};


if (!els.form) {
    return;
}


function mostrarFeedback(
    mensaje,
    tipo
) {

    els.feedback.textContent =
        mensaje;

    els.feedback.className =
        "contact-feedback " + tipo;

}


function bloquearFormulario(
    bloqueado
) {

    els.boton.disabled =
        bloqueado;

    els.motivo.disabled =
        bloqueado;

    els.email.disabled =
        bloqueado;

    els.mensaje.disabled =
        bloqueado;

}


els.form.addEventListener(
    "submit",
    function (event) {

        event.preventDefault();


        const motivo =
            els.motivo.value.trim();

        const email =
            els.email.value.trim();

        const mensaje =
            els.mensaje.value.trim();


        if (
            !motivo ||
            !email ||
            !mensaje
        ) {

            mostrarFeedback(
                "COMPLETÁ TODOS LOS CAMPOS.",
                "error"
            );

            return;
        }


        bloquearFormulario(true);


        mostrarFeedback(
            "ENVIANDO MENSAJE...",
            ""
        );


        fetch(
            URL_ENVIAR_CONTACTO,
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({

                    motivo:
                        motivo,

                    email:
                        email,

                    mensaje:
                        mensaje

                })
            }
        )
        .then(function (response) {

            return response.json()
                .then(function (data) {

                    return {
                        ok: response.ok,
                        data: data
                    };

                });

        })
        .then(function (resultado) {

            if (
                !resultado.ok ||
                !resultado.data.ok
            ) {

                throw new Error(
                    resultado.data.mensaje ||
                    "NO SE PUDO ENVIAR EL MENSAJE."
                );

            }


            mostrarFeedback(
                "¡MENSAJE ENVIADO! GRACIAS POR CONTACTARNOS 💚",
                "success"
            );


            els.form.reset();


            setTimeout(
                function () {

                    els.feedback.textContent =
                        "";

                    els.feedback.className =
                        "contact-feedback";

                },
                4000
            );

        })
        .catch(function (error) {

            console.error(
                "Error al enviar contacto:",
                error
            );


            mostrarFeedback(
                error.message ||
                "NO SE PUDO ENVIAR EL MENSAJE.",
                "error"
            );

        })
        .finally(function () {

            bloquearFormulario(false);

        });

    }
);


})();
