cargarProductores();
cargarPredios();

async function cargarProductores(){

    const r = await fetch("/productores");

    const datos = await r.json();

    let combo = document.getElementById("productor");

    combo.innerHTML="";

    datos.forEach(p=>{

        combo.innerHTML += `
        <option value="${p.id}">
            ${p.nombre}
        </option>`;

    });

}

async function cargarPredios(){

    const r = await fetch("/predios");

    const datos = await r.json();

    let tabla=document.getElementById("tabla");

    tabla.innerHTML=`

    <tr>

    <th>ID</th>

    <th>Predio</th>

    <th>Productor</th>

    <th>Superficie</th>

    <th>Región</th>

    <th>Comuna</th>

    </tr>

    `;

    datos.forEach(p=>{

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

}

async function guardarPredio(){

    await fetch("/predios",{

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({

            nombre:document.getElementById("nombre").value,

            productor_id:Number(document.getElementById("productor").value),

            superficie:Number(document.getElementById("superficie").value),

            region:document.getElementById("region").value,

            comuna:document.getElementById("comuna").value

        })

    });

    cargarPredios();

}