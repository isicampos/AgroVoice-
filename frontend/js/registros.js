// ============================================
// REGISTROS AGROVOICE
// ============================================


// ============================================
// CARGAR PRODUCTORES
// ============================================

async function cargarProductores() {

    const select = document.getElementById("productor");

    try {

        const respuesta = await fetch("/productores");

        const productores = await respuesta.json();

        select.innerHTML = `
            <option value="">
                Seleccionar productor
            </option>
        `;

        productores.forEach(productor => {

            const opcion = document.createElement("option");

            opcion.value = productor.id;

            opcion.textContent = productor.nombre;

            select.appendChild(opcion);

        });

    } catch (error) {

        console.error(
            "Error cargando productores:",
            error
        );

    }
}



// ============================================
// CARGAR PREDIOS
// ============================================

async function cargarPredios() {

    const select = document.getElementById("predio");

    try {

        const respuesta = await fetch("/predios");

        const predios = await respuesta.json();

        select.innerHTML = `
            <option value="">
                Seleccionar predio
            </option>
        `;

        predios.forEach(predio => {

            const opcion = document.createElement("option");

            opcion.value = predio.id;

            opcion.textContent = predio.nombre;

            select.appendChild(opcion);

        });

    } catch (error) {

        console.error(
            "Error cargando predios:",
            error
        );

    }
}



// ============================================
// CARGAR CUARTELES
// ============================================

async function cargarCuarteles() {

    const select = document.getElementById("cuartel");

    try {

        const respuesta = await fetch("/cuarteles");

        const cuarteles = await respuesta.json();

        select.innerHTML = `
            <option value="">
                Seleccionar cuartel
            </option>
        `;

        cuarteles.forEach(cuartel => {

            const opcion = document.createElement("option");

            opcion.value = cuartel.id;

            opcion.textContent =
                cuartel.nombre +
                " - " +
                cuartel.cultivo;

            select.appendChild(opcion);

        });

    } catch (error) {

        console.error(
            "Error cargando cuarteles:",
            error
        );

    }
}



// ============================================
// FECHA AUTOMÁTICA
// ============================================

function colocarFechaActual() {

    const fecha =
        document.getElementById("fecha");

    const hoy =
        new Date();

    const año =
        hoy.getFullYear();

    const mes =
        String(
            hoy.getMonth() + 1
        ).padStart(2, "0");

    const dia =
        String(
            hoy.getDate()
        ).padStart(2, "0");

    fecha.value =
        `${año}-${mes}-${dia}`;
}



// ============================================
// CARGAR REGISTROS
// ============================================

async function cargarRegistros() {

    const tabla =
        document.getElementById(
            "tablaRegistros"
        );

    try {

        const respuesta =
            await fetch("/registros");

        const registros =
            await respuesta.json();

        tabla.innerHTML = "";


        if (
            registros.length === 0
        ) {

            tabla.innerHTML = `
                <tr>
                    <td
                        colspan="9"
                        class="sin-datos"
                    >
                        Todavía no hay registros agrícolas.
                    </td>
                </tr>
            `;

            return;
        }


        registros.forEach(registro => {

            const fila =
                document.createElement("tr");


            fila.innerHTML = `

                <td>
                    ${registro.id}
                </td>

                <td>
                    ${registro.fecha}
                </td>

                <td>
                    ${registro.productor}
                </td>

                <td>
                    ${registro.predio}
                </td>

                <td>
                    ${registro.cuartel}
                </td>

                <td>
                    ${registro.cultivo}
                </td>

                <td>
                    ${registro.labor}
                </td>

                <td>
                    ${registro.transcripcion || ""}
                </td>

                <td>

                    <button
                        class="btn-eliminar"
                        onclick="eliminarRegistro(${registro.id})"
                    >
                        Eliminar
                    </button>

                </td>

            `;


            tabla.appendChild(fila);

        });

    } catch (error) {

        console.error(
            "Error cargando registros:",
            error
        );

        tabla.innerHTML = `
            <tr>
                <td
                    colspan="9"
                    class="sin-datos"
                >
                    No se pudieron cargar los registros.
                </td>
            </tr>
        `;

    }

}



// ============================================
// GUARDAR REGISTRO
// ============================================

async function guardarRegistro() {

    const fecha =
        document.getElementById(
            "fecha"
        ).value;

    const productorSelect =
        document.getElementById(
            "productor"
        );

    const predioSelect =
        document.getElementById(
            "predio"
        );

    const cuartelSelect =
        document.getElementById(
            "cuartel"
        );

    const productor =
        productorSelect
            .options[
                productorSelect.selectedIndex
            ]?.text || "";

    const predio =
        predioSelect
            .options[
                predioSelect.selectedIndex
            ]?.text || "";

    const cuartel =
        cuartelSelect
            .options[
                cuartelSelect.selectedIndex
            ]?.text || "";

    const cultivo =
        document.getElementById(
            "cultivo"
        ).value;

    const labor =
        document.getElementById(
            "labor"
        ).value;

    const transcripcion =
        document.getElementById(
            "transcripcion"
        ).value.trim();

    const mensaje =
        document.getElementById(
            "mensaje"
        );


    // ========================================
    // VALIDACIÓN
    // ========================================

    if (
        !fecha ||
        !productorSelect.value ||
        !predioSelect.value ||
        !cuartelSelect.value ||
        !cultivo ||
        !labor
    ) {

        mensaje.style.color =
            "#c62828";

        mensaje.textContent =
            "Completa todos los campos.";

        return;

    }


    try {

        const respuesta =
            await fetch(
                "/registros",
                {

                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({

                        fecha:
                            fecha,

                        productor:
                            productor,

                        predio:
                            predio,

                        cuartel:
                            cuartel,

                        cultivo:
                            cultivo,

                        labor:
                            labor,

                        transcripcion:
                            transcripcion

                    })

                }
            );


        const datos =
            await respuesta.json();


        if (!respuesta.ok) {

            mensaje.style.color =
                "#c62828";

            mensaje.textContent =
                datos.detail ||
                datos.mensaje ||
                "No se pudo guardar el registro.";

            return;

        }


        // ====================================
        // ÉXITO
        // ====================================

        mensaje.style.color =
            "#2e7d32";

        mensaje.textContent =
            "✓ Registro guardado correctamente.";


        document.getElementById(
            "productor"
        ).value = "";

        document.getElementById(
            "predio"
        ).value = "";

        document.getElementById(
            "cuartel"
        ).value = "";

        document.getElementById(
            "cultivo"
        ).value = "";

        document.getElementById(
            "labor"
        ).value = "";

        document.getElementById(
            "transcripcion"
        ).value = "";


        colocarFechaActual();

        cargarRegistros();


    } catch (error) {

        console.error(error);

        mensaje.style.color =
            "#c62828";

        mensaje.textContent =
            "No se pudo conectar con AgroVoice.";

    }

}



// ============================================
// ELIMINAR REGISTRO
// ============================================

async function eliminarRegistro(id) {

    const confirmar =
        confirm(
            "¿Quieres eliminar este registro?"
        );


    if (!confirmar) {

        return;

    }


    try {

        const respuesta =
            await fetch(
                `/registros/${id}`,
                {
                    method: "DELETE"
                }
            );


        if (!respuesta.ok) {

            alert(
                "No se pudo eliminar el registro."
            );

            return;

        }


        cargarRegistros();


    } catch (error) {

        console.error(error);

        alert(
            "No se pudo conectar con AgroVoice."
        );

    }

}



// ============================================
// INICIO
// ============================================

document.addEventListener(
    "DOMContentLoaded",
    () => {

        colocarFechaActual();

        cargarProductores();

        cargarPredios();

        cargarCuarteles();

        cargarRegistros();

    }
);