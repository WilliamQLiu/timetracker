var data_exp = [10, 20, 30, 40, 50, 60];

//var w=960, h=500, svg=d3.select("#chart").append("svg").attr("width", w).attr("height",h);
//var text = svg.append("text").text("hello world").attr("y", 50);
var x = d3.scale.linear()
        .domain([0, d3.max(data_exp)])
        .range([0, 420]);

d3.select(".chart")
        .selectAll("div")
        .data(data_exp)
        .enter().append("div")
        .style("width", function(d)
    { return x(d) + "px";
     })
    .text(function(d) { return d; });
