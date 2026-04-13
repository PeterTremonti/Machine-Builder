export function log(msg)
{

const consoleBox = document.getElementById("console")
if(!consoleBox) return

const line = document.createElement("div")
line.textContent = msg

// ✅ NEW: add to TOP instead of bottom
consoleBox.prepend(line)

}