export let canvas
export let ctx

export function init_canvas()
{

canvas = document.getElementById("builder_canvas")

resizeCanvas()

ctx = canvas.getContext("2d")

window.addEventListener("resize", resizeCanvas)

}

function resizeCanvas()
{

const rect = canvas.getBoundingClientRect()

canvas.width = rect.width
canvas.height = rect.height

}