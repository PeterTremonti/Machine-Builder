function runDiagnostics(){

log("Running system diagnostics...","info");

let hasHotend=false;
let hasFan=false;
let hasThermistor=false;

machineDevices.forEach(d=>{

if(d.name==="Generic Hotend") hasHotend=true;
if(d.name==="Cooling Fan") hasFan=true;
if(d.name==="Thermistor") hasThermistor=true;

});

if(hasHotend && !hasFan)
log("WARNING: Hotend cooling fan missing","warn");

if(hasHotend && !hasThermistor)
log("ERROR: Hotend thermistor missing","error");

if(hasHotend && hasFan && hasThermistor)
log("INFO: Hotend system appears complete","info");

}
