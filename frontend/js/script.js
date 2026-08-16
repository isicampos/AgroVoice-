fetch("/dashboard")


.then(res=>res.json())

.then(data=>{

document.getElementById("registros").innerHTML=data.total_registros;

document.getElementById("productores").innerHTML=data.total_productores;

document.getElementById("cultivos").innerHTML=data.total_cultivos;

});