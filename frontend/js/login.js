async function login(){

    const respuesta = await fetch("/login",{

        method:"POST",

        headers:{

            "Content-Type":"application/json"

        },

        body:JSON.stringify({

            correo:document.getElementById("correo").value,

            password:document.getElementById("password").value

        })

    });

    const datos = await respuesta.json();
    
if(datos.ok){

    window.location.href="/dashboard";

}

    else{

        document.getElementById("mensaje").innerHTML=datos.mensaje;

    }

}