function draw_board(board,x,y)
{

let width = board.visual.size.width
let height = board.visual.size.height

ctx.fillStyle = "#dcdcdc"
ctx.fillRect(x,y,width,height)

ctx.strokeStyle = "black"
ctx.strokeRect(x,y,width,height)

ctx.fillStyle = "black"

/* ensure board title always centers */
ctx.textAlign = "left"

ctx.fillText(board.name,x+10,y+20)

draw_ports(board,x,y)

}

function draw_ports(board,x,y)
{

ctx.save()

board.visual.ports.forEach(port => {

let px = x + port.x
let py = y + port.y

ctx.beginPath()
ctx.arc(px,py,5,0,Math.PI*2)

ctx.fillStyle="blue"
ctx.fill()

ctx.fillStyle="black"

if(port.side === "right")
{
ctx.textAlign = "right"
ctx.fillText(port.label,px-8,py+4)
}
else
{
ctx.textAlign = "left"
ctx.fillText(port.label,px+8,py+4)
}

})

ctx.restore()

}