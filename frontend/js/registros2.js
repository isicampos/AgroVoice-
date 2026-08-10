cargarProductores();

async function cargarProductores(){

    const r = await fetch("/productores");

    const datos = await r.json();

    let combo = document.getElementById("productor");

    combo.innerHTML="";

    datos.forEach(p=>{

        combo.innerHTML+=`
        <option value="${p.id}">
            ${p.nombre}
        </option>`;

    });

}

async function guardarRegistro(){

    await fetch("/registros2",{

        method:"POST",

        headers:{

            "Content-Type":"application/json"

        },

        body:JSON.stringify({

            fecha:document.getElementById("fecha").value,

            productor_id:Number(document.getElementById("productor").value),

            predio_id:1,

            cuartel_id:1,

            cultivo:document.getElementById("cultivo").value,

            labor:document.getElementById("labor").value,

            descripcion:document.getElementById("descripcion").value

        })

    });

    alert("Registro guardado correctamente");

}