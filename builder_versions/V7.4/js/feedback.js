function log(msg,type){

const div=document.createElement("div");
div.className=type;
div.innerText=msg;

document.getElementById("console").appendChild(div);

}
