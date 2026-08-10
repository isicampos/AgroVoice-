/* ==========================================
   AGROVOICE - DASHBOARD
========================================== */


async function cargarDashboard() {

    try {

        const respuesta =
            await fetch("/dashboard_api");


        if (!respuesta.ok) {

            throw new Error(
                "No se pudo cargar el dashboard"
            );

        }


        const datos =
            await respuesta.json();


        /* ================================
           CONTADORES
        ================================= */

        document.getElementById(
            "total_productores"
        ).textContent =
            datos.total_productores ?? 0;


        document.getElementById(
            "total_predios"
        ).textContent =
            datos.total_predios ?? 0;


        document.getElementById(
            "total_cuarteles"
        ).textContent =
            datos.total_cuarteles ?? 0;


        document.getElementById(
            "total_registros"
        ).textContent =
            datos.total_registros ?? 0;


        /* ================================
           ÚLTIMOS REGISTROS
        ================================= */

        const tbody =
            document.querySelector(
                "#tabla_registros tbody"
            );


        tbody.innerHTML = "";


        const registros =
            datos.ultimos || [];


        if (registros.length === 0) {

            tbody.innerHTML = `

                <tr>

                    <td
                        colspan="4"
                        class="empty">

                        Todavía no hay registros agrícolas.

                    </td>

                </tr>

            `;

        } else {

            registros.forEach(registro => {

                const fila =
                    document.createElement("tr");


                /*
                    Estructura SQLite:

                    0 = id
                    1 = fecha
                    2 = productor
                    3 = predio
                    4 = cuartel
                    5 = cultivo
                    6 = labor
                    7 = transcripcion
                */


                fila.innerHTML = `

                    <td>
                        ${escaparHTML(
                            registro[1] || "-"
                        )}
                    </td>

                    <td>
                        ${escaparHTML(
                            registro[5] || "-"
                        )}
                    </td>

                    <td>
                        <span class="labor-badge">

                            ${escaparHTML(
                                registro[6] || "-"
                            )}

                        </span>
                    </td>

                    <td>
                        ${escaparHTML(
                            registro[3] || "-"
                        )}
                    </td>

                `;


                tbody.appendChild(fila);

            });

        }


        /* ================================
           CARGAR GRÁFICO
        ================================= */

        await cargarGraficoCultivos();


    } catch (error) {

        console.error(
            "Error cargando dashboard:",
            error
        );

    }

}


/* ==========================================
   GRÁFICO DE CULTIVOS
========================================== */


async function cargarGraficoCultivos() {

    const contenedor =
        document.getElementById(
            "grafico_cultivos"
        );


    try {

        const respuesta =
            await fetch("/registros");


        if (!respuesta.ok) {

            throw new Error(
                "No se pudieron obtener registros"
            );

        }


        const registros =
            await respuesta.json();


        if (!registros.length) {

            contenedor.innerHTML = `

                <div class="chart-empty">

                    Aún no existen registros
                    suficientes para mostrar
                    el gráfico.

                </div>

            `;

            return;

        }


        /* ================================
           CONTAR CULTIVOS
        ================================= */

        const cultivos = {};


        registros.forEach(registro => {

            const cultivo =
                registro.cultivo ||
                "Sin cultivo";


            if (!cultivos[cultivo]) {

                cultivos[cultivo] = 0;

            }


            cultivos[cultivo]++;

        });


        const datos =
            Object.entries(cultivos)
                .sort((a, b) => b[1] - a[1])
                .slice(0, 6);


        const maximo =
            Math.max(
                ...datos.map(item => item[1])
            );


        contenedor.innerHTML = "";


        datos.forEach(([cultivo, cantidad]) => {

            const porcentaje =
                maximo > 0
                    ? (cantidad / maximo) * 100
                    : 0;


            const elemento =
                document.createElement("div");


            elemento.className =
                "bar-item";


            elemento.innerHTML = `

                <div class="bar-label">

                    <span>
                        ${escaparHTML(cultivo)}
                    </span>

                    <strong>
                        ${cantidad}
                    </strong>

                </div>


                <div class="bar-track">

                    <div
                        class="bar-fill"
                        style="width:${porcentaje}%">

                    </div>

                </div>

            `;


            contenedor.appendChild(elemento);

        });


    } catch (error) {

        console.error(
            "Error cargando gráfico:",
            error
        );


        contenedor.innerHTML = `

            <div class="chart-empty">

                No se pudo cargar el gráfico.

            </div>

        `;

    }

}


/* ==========================================
   USUARIO
========================================== */


async function cargarUsuario() {

    try {

        const respuesta =
            await fetch("/usuario_actual");


        if (!respuesta.ok) {

            return;

        }


        const usuario =
            await respuesta.json();


        const nombre =
            usuario.usuario ||
            "Usuario";


        const rol =
            usuario.rol ||
            "Usuario";


        document.getElementById(
            "nombre_usuario"
        ).textContent = nombre;


        document.getElementById(
            "nombre_usuario_header"
        ).textContent = nombre;


        document.getElementById(
            "rol_usuario"
        ).textContent = rol;


        /* Inicial */

        const inicial =
            nombre
                .trim()
                .charAt(0)
                .toUpperCase();


        document.getElementById(
            "inicial_usuario"
        ).textContent =
            inicial || "U";


    } catch (error) {

        console.error(
            "Error cargando usuario:",
            error
        );

    }

}


/* ==========================================
   SEGURIDAD BÁSICA
========================================== */


function escaparHTML(texto) {

    return String(texto)

        .replace(/&/g, "&amp;")

        .replace(/</g, "&lt;")

        .replace(/>/g, "&gt;")

        .replace(/"/g, "&quot;")

        .replace(/'/g, "&#039;");

}


/* ==========================================
   INICIAR
========================================== */


window.addEventListener(
    "DOMContentLoaded",
    () => {

        cargarDashboard();

        cargarUsuario();

    }
);
