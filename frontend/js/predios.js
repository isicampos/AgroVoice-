// ==========================================
// CARGAR PRODUCTORES
// ==========================================

async function cargarProductores() {

    try {

        const respuesta = await fetch("/productores");

        if (!respuesta.ok) {
            throw new Error("No se pudieron cargar los productores");
        }

        const datos = await respuesta.json();

        const combo = document.getElementById("productor");

        combo.innerHTML = "";

        datos.forEach(p => {

            combo.innerHTML += `
                <option value="${p.id}">
                    ${p.nombre}
                </option>
            `;

        });

    } catch (error) {

        console.error("Error cargando productores:", error);

        alert("No se pudieron cargar los productores.");

    }
}


// ==========================================
// CARGAR PREDIOS
// ==========================================

async function cargarPredios() {

    try {

        const respuesta = await fetch("/predios");

        if (!respuesta.ok) {
            throw new Error("No se pudieron cargar los predios");
        }

        const datos = await respuesta.json();

        const tabla = document.getElementById("tabla");

        tabla.innerHTML = `
            <tr>
                <th>ID</th>
                <th>Predio</th>
                <th>Productor</th>
                <th>Superficie</th>
                <th>Región</th>
                <th>Comuna</th>
            </tr>
        `;

        datos.forEach(p => {

            tabla.innerHTML += `
                <tr>
                    <td>${p.id}</td>
                    <td>${p.nombre}</td>
                    <td>${p.productor}</td>
                    <td>${p.superficie}</td>
                    <td>${p.region}</td>
                    <td>${p.comuna}</td>
                </tr>
            `;

        });

    } catch (error) {

        console.error("Error cargando predios:", error);

        alert("No se pudieron cargar los predios.");

    }
}


// ==========================================
// GUARDAR PREDIO
// ==========================================

async function guardarPredio() {

    try {

        const nombre = document.getElementById("nombre").value.trim();
        const productor = document.getElementById("productor").value;
        const superficie = document.getElementById("superficie").value;
        const region = document.getElementById("region").value.trim();
        const comuna = document.getElementById("comuna").value.trim();

        if (!nombre || !productor || !superficie || !region || !comuna) {

            alert("Completa todos los campos.");

            return;
        }

        const respuesta = await fetch("/predios", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({

                nombre: nombre,

                productor_id: Number(productor),

                superficie: Number(superficie),

                region: region,

                comuna: comuna

            })

        });

        if (!respuesta.ok) {

            const errorTexto = await respuesta.text();

            console.error("Error del servidor:", errorTexto);

            throw new Error("El servidor rechazó el predio.");

        }

        const resultado = await respuesta.json();

        console.log("Predio guardado:", resultado);

        alert("¡Predio guardado correctamente! 🌱");

        // Limpiar campos
        document.getElementById("nombre").value = "";
        document.getElementById("superficie").value = "";
        document.getElementById("region").value = "";
        document.getElementById("comuna").value = "";

        // Actualizar tabla
        cargarPredios();

    } catch (error) {

        console.error("Error guardando predio:", error);

        alert(
            "No se pudo guardar el predio.\n\n" +
            "Revisa la consola para ver el error."
        );

    }

}


// ==========================================
// INICIAR
// ==========================================

window.onload = function () {

    cargarProductores();

    cargarPredios();

};