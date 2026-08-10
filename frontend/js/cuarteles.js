cargarPredios();
cargarCuarteles();

async function cargarPredios() {

    const r = await fetch("/predios");

    const datos = await r.json();

    let combo = document.getElementById("predio");

    combo.innerHTML = "";

    datos.forEach(p => {

        combo.innerHTML += `
        <option value="${p.id}">
            ${p.nombre}
        </option>
        `;

    });

}

async function cargarCuarteles() {

    const r = await fetch("/cuarteles");

    const datos = await r.json();

    let tabla = document.getElementById("tabla");

    tabla.innerHTML = `

    <tr>

        <th>ID</th>

        <th>Nombre</th>

        <th>Predio</th>

        <th>Cultivo</th>

        <th>Variedad</th>

        <th>Superficie</th>

    </tr>

    `;

    datos.forEach(c => {

        tabla.innerHTML += `

        <tr>

            <td>${c.id}</td>

            <td>${c.nombre}</td>

            <td>${c.predio}</td>

            <td>${c.cultivo}</td>

            <td>${c.variedad}</td>

            <td>${c.superficie}</td>

        </tr>

        `;

    });

}

async function guardar() {

    await fetch("/cuarteles", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({

            nombre: document.getElementById("nombre").value,

            predio_id: Number(document.getElementById("predio").value),

            cultivo: document.getElementById("cultivo").value,

            variedad: document.getElementById("variedad").value,

            superficie: Number(document.getElementById("superficie").value)

        })

    });

    document.getElementById("nombre").value = "";
    document.getElementById("cultivo").value = "";
    document.getElementById("variedad").value = "";
    document.getElementById("superficie").value = "";

    cargarCuarteles();

}