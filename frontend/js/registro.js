async function registrar() {

    const nombre = document.getElementById("nombre").value.trim();
    const correo = document.getElementById("correo").value.trim();
    const password = document.getElementById("password").value.trim();
    const rol = document.getElementById("rol").value;

    const mensaje = document.getElementById("mensaje");


    // Limpiar mensaje
    mensaje.textContent = "";


    // Validaciones
    if (!nombre || !correo || !password) {

        mensaje.style.color = "#c62828";

        mensaje.textContent =
            "Por favor completa todos los campos.";

        return;
    }


    try {

        const respuesta = await fetch("/usuarios", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({

                nombre: nombre,

                correo: correo,

                password: password,

                rol: rol

            })

        });


        const datos = await respuesta.json();


        if (!respuesta.ok) {

            mensaje.style.color = "#c62828";

            mensaje.textContent =
                datos.detail ||
                datos.mensaje ||
                "No fue posible crear la cuenta.";

            return;
        }


        // Cuenta creada correctamente

        mensaje.style.color = "#2e7d32";

        mensaje.textContent =
            "✓ Cuenta creada correctamente. Redirigiendo...";


        // Esperar un momento y volver al login

        setTimeout(() => {

            window.location.href = "/login_web";

        }, 1500);


    } catch (error) {

        console.error(error);

        mensaje.style.color = "#c62828";

        mensaje.textContent =
            "No se pudo conectar con AgroVoice.";

    }

}