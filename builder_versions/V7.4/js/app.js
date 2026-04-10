let deviceDB={};

fetch("data/devices.json")
.then(r=>r.json())
.then(data=>{

deviceDB=data;

populateDeviceSelect();

});

function populateDeviceSelect(){

const select=document.getElementById("deviceSelect");

Object.values(deviceDB).forEach(group=>{

group.forEach(device=>{

const opt=document.createElement("option");
opt.value=device.name;
opt.text=device.name;

select.appendChild(opt);

});

});

}

function addDevice(){

const name=document.getElementById("deviceSelect").value;

const device={name:name};

addMachineDevice(device);

log("Added device: "+name,"info");

}
