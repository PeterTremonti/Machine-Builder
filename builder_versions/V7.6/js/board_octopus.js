function drawOctopus(){

let svg=`

<svg viewBox="0 0 600 300">

<rect x="50" y="50" width="500" height="200" fill="#333"/>

<text x="300" y="80" fill="white" text-anchor="middle">
BTT Octopus V1.1
</text>

<circle cx="120" cy="220" r="12" fill="#6cf" onclick="selectPort('STEP0')"/>
<circle cx="170" cy="220" r="12" fill="#6cf" onclick="selectPort('STEP1')"/>

<circle cx="420" cy="120" r="12" fill="#f66" onclick="selectPort('HE0')"/>
<circle cx="420" cy="160" r="12" fill="#ff9" onclick="selectPort('TH0')"/>

<circle cx="420" cy="200" r="12" fill="#6f6" onclick="selectPort('FAN0')"/>

<text x="120" y="250" fill="white">STEP0</text>
<text x="170" y="250" fill="white">STEP1</text>

<text x="450" y="120" fill="white">HE0</text>
<text x="450" y="160" fill="white">TH0</text>
<text x="450" y="200" fill="white">FAN0</text>

</svg>
`;

document.getElementById("svgCanvas").innerHTML=svg;

}