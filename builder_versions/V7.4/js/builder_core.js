document.addEventListener("DOMContentLoaded", function(){

let machineDevices=[];

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

updateDeviceList();

log("Added device: "+name,"info");

if(name==="BTT Octopus V1.1"){

loadOctopus();

}

}

function updateDeviceList(){

let list=document.getElementById("deviceList");

list.innerHTML="";

machineDevices.forEach(d=>{

let li=document.createElement("li");

li.innerText=d;

list.appendChild(li);

});

}

window.runDiagnostics=function(){

log("Running diagnostics...","info");

let hasHotend=false;
let hasFan=false;
let hasThermistor=false;

machineDevices.forEach(d=>{

if(d==="Generic Hotend") hasHotend=true;
if(d==="Cooling Fan") hasFan=true;
if(d==="Thermistor") hasThermistor=true;

});

if(hasHotend && !hasFan)
log("WARNING: Hotend cooling fan missing","warn");

if(hasHotend && !hasThermistor)
log("ERROR: Hotend thermistor missing","error");

if(hasHotend && hasFan && hasThermistor)
log("INFO: Hotend system appears complete","info");

}

function log(msg,type){

let div=document.createElement("div");

div.className=type;

div.innerText=msg;

document.getElementById("console").appendChild(div);

}

function loadOctopus(){

document.getElementById("svgCanvas").innerHTML=`

<svg viewBox="0 0 600 300">

<rect x="50" y="50" width="500" height="200" fill="#333"/>

<text x="300" y="120" fill="white" text-anchor="middle">
BTT Octopus V1.1
</text>

<circle cx="120" cy="220" r="10" fill="#6cf"/>
<circle cx="160" cy="220" r="10" fill="#6cf"/>
<circle cx="200" cy="220" r="10" fill="#6cf"/>

<text x="120" y="250" fill="white" font-size="12">M0</text>
<text x="160" y="250" fill="white" font-size="12">M1</text>
<text x="200" y="250" fill="white" font-size="12">M2</text>

</svg>

`;

log("Loaded board: Octopus V1.1","info");

}

});