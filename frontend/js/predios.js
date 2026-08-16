cargarProductores();
cargarPredios();

async function cargarProductores() {

    try {

        const r = await fetch("/productores");

        if (!r.ok) {
            throw new Error("No se pudieron cargar los productores");
        }

        const datos = await r.json();

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


async function cargarPredios() {

    try {

        const r = await fetch("/predios");

        if (!r.ok) {
            throw new Error("Error al cargar predios");
        }

        const datos = await r.json();

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
                    <td>${p.productor || ""}</td>
                    <td>${p.superficie || ""}</td>
                    <td>${p.region || ""}</td>
                    <td>${p.comuna || ""}</td>
                </tr>
            `;

        });

    } catch (error) {

        console.error("Error cargando predios:", error);

        alert("No se pudieron cargar los predios.");

    }

}


async function guardarPredio() {

    const nombre = document.getElementById("nombre").value.trim();
    const productor = document.getElementById("productor").value;
    const superficie = document.getElementById("superficie").value;
    const region = document.getElementById("region").value.trim();
    const comuna = document.getElementById("comuna").value.trim();


    // Validar campos

    if (!nombre || !productor || !superficie || !region || !comuna) {

        alert("Completa todos los campos antes de guardar.");

        return;
    }


    try {

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


        // Obtener respuesta del servidor

        const texto = await respuesta.text();

        console.log("Respuesta del servidor:", texto);


        if (!respuesta.ok) {

            alert(
                "No se pudo guardar el predio.\n\n" +
                "Error: " + texto
            );

            return;
        }


        alert("✓ Predio guardado correctamente");


        // Limpiar formulario

        document.getElementById("nombre").value = "";
        document.getElementById("superficie").value = "";
        document.getElementById("region").value = "";
        document.getElementById("comuna").value = "";


        // Recargar tabla

        cargarPredios();


    } catch (error) {

        console.error("Error guardando predio:", error);

        alert(
            "No se pudo conectar con AgroVoice.\n\n" +
            error
        );

    }

}