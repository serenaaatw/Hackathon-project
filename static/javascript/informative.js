const video = document.getElementById("videoInformativo");
const botonContinuar = document.getElementById("btnContinuar");

video.addEventListener("ended", function () {
    botonContinuar.style.display = "flex";
});