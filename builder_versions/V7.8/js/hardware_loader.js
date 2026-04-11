async function load_hardware(path)
{
    try
    {
        let response = await fetch(path)

        if(!response.ok)
        {
            throw new Error("HTTP error " + response.status)
        }

        let data = await response.json()

        return data
    }
    catch(error)
    {
        console.error("Hardware load failed:", error)
    }
}