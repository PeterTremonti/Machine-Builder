export class ConnectionEngine
{

constructor()
{
this.connections = []
this.pendingPort = null
}

begin(port)
{
this.pendingPort = port
}

tryComplete(port)
{

if(!this.pendingPort) return false

// prevent connecting same port
if(
this.pendingPort.deviceId === port.deviceId &&
this.pendingPort.portId === port.portId
)
{
this.pendingPort = null
return false
}

// TEMP: allow all connections
this.connections.push({

id: crypto.randomUUID(),

from: this.pendingPort,
to: port

})

this.pendingPort = null

return true

}

getConnections()
{
return this.connections
}

}