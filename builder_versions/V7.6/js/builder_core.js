document.addEventListener("DOMContentLoaded",function(){

let machineDevices=[];
let mode="basic";

const deviceSelect=document.getElementById("deviceSelect");

deviceDB.forEach(d=>{

let opt=document.createElement("option");
opt.value=d.name;
opt.text=d.name;

deviceSelect.appendChild(opt);

});

window.addDevice=function(){

let name=deviceSelect.value;

machineDevices.push(name);

updateList();

log("Added device: "+name,"info");

if(name==="BTT Octopus V1.1"){
drawOctopus();
}

}

function updateList(){

let list=document.getElementById("deviceList");

list.innerHTML="";

machineDevices.forEach(d=>{

let li=document.createElement("li");
li.innerText=d;
list.appendChild(li);

});

}

window.toggleMode=function(){

if(mode==="basic"){
mode="advanced";
log("Advanced mode enabled","info");
}else{
mode="basic";
log("Basic mode enabled","info");
}

}

window.runDiagnostics=function(){

let hasHotend=false;
let hasThermistor=false;
let hasFan=false;

machineDevices.forEach(d=>{

if(d==="Generic Hotend") hasHotend=true;
if(d==="Thermistor") hasThermistor=true;
if(d==="Cooling Fan") hasFan=true;

});

if(hasHotend && !hasThermistor)
log("ERROR: Hotend missing thermistor","error");

if(hasHotend && !hasFan)
log("WARNING: Hotend cooling fan missing","warn");

if(hasHotend && hasThermistor && hasFan)
log("Hotend system OK","info");

}

function log(msg,type){

let div=document.createElement("div");

div.className=type;
div.innerText=msg;

document.getElementById("console").appendChild(div);

}

});