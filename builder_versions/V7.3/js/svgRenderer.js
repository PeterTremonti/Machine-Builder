function loadBoard(svgFile){

fetch(svgFile)
.then(r=>r.text())
.then(svg=>{
document.getElementById("svgCanvas").innerHTML=svg;
});

}
