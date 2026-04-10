let machineDevices=[];

function addMachineDevice(device){
machineDevices.push(device);
updateDeviceList();
}

function updateDeviceList(){

const list=document.getElementById("deviceList");
list.innerHTML="";

machineDevices.forEach(d=>{
const li=document.createElement("li");
li.innerText=d.name;
list.appendChild(li);
});

}
