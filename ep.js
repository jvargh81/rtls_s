async function main(){
/* Predefining the SVG params.*/
var w=1000;
var h=1000;
var padding=60;  
var yValue=440;

/* Creating the SVG canvas. */  
var svg = d3.select("body")
.append("svg")
.attr("width",w)
.attr("height",h)

/* Static text append. */
svg.append("text")
.attr("x",300)
.attr("y",15)
.text("Visualize RSSI for each tagmac associated endpoints (not In Motion)")
.attr("font-size",22)
.attr("text-anchor","middle")

svg.append("text")
.attr("x",275)
.attr("y",40)
.text("Select the Tag Mac")
.attr("font-size",15)
.attr("fill","red")
.attr("text-anchor","middle")

var image = svg.append("svg:image")
    .attr("xlink:href", "0x5f8d55.svg")
    .attr("width", 750)
    .attr("height", 750)
    .attr("x",0)
    .attr("y",100)

d3.selectAll("option")
     /*Click Functionality */
     .on("click", function(){ 
        image
        .attr("xlink:href",this.value)
        console.log(this.value);
        })  
}

main();
