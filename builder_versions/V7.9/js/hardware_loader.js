export async function loadHardwareDatabase()
{

const categories = [
"boards",
"motors",
"heaters",
"sensors"
]

const hardware = {}

for(const category of categories)
{

try
{
const response = await fetch(`../../hardware_database/${category}/index.json`)
const files = await response.json()

for(const file of files)
{
const res = await fetch(`../../hardware_database/${category}/${file}`)
const data = await res.json()

hardware[data.id] = data
}

}
catch(e)
{
console.warn(`No index.json for ${category}`)
}

}

return hardware

}