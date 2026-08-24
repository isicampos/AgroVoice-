async function login() {

    const mensaje = document.getElementById("mensaje");

    const correo = document.getElementById("correo").value.trim().toLowerCase();
    const password = document.getElementById("password").value;

    if (!correo || !password) {
        mensaje.innerHTML = "⚠️ Ingresa correo y contraseña.";
        return;
    }

    mensaje.innerHTML = "⏳ Ingresando...";

    try {

        const respuesta = await fetch("/login", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            credentials: "include",

            body: JSON.stringify({
                correo: correo,
                password: password
            })

        });

        const texto = await respuesta.text();

        console.log("RESPUESTA LOGIN:", respuesta.status, texto);

        let datos;

        try {
            datos = JSON.parse(texto);
        } catch (error) {
            mensaje.innerHTML =
                "❌ El servidor respondió con un error.";
            console.error("Respuesta no JSON:", texto);
            return;
        }

        if (respuesta.ok && datos.ok) {

            mensaje.innerHTML = "✅ Acceso correcto. Entrando...";

            window.location.href = "/dashboard";

        } else {

            mensaje.innerHTML =
                "❌ " + (datos.mensaje || "Correo o contraseña incorrectos.");

        }

    } catch (error) {

        console.error("ERROR LOGIN:", error);

        mensaje.innerHTML =
            "❌ No se pudo conectar con AgroVoice.";

    }
}