<template>
  <div id="chart"></div>
</template>
<script>
import * as d3 from "d3";
import testdata from './data.json';

let width = window.innerWidth;
let height = window.innerHeight;
let color = d3
  .scaleLinear()
  .domain([0, 5])
  .range(["hsl(152,80%,80%)", "hsl(228,30%,40%)"])
  .interpolate(d3.interpolateHcl);
const pack = data =>
  d3
    .pack()
    .size([width, height])
    .padding(3)(
    d3
      .hierarchy(data)
      .sum(d => d.value)
      .sort((a, b) => b.value - a.value)
  );

export default {
  data() {
    return {
      svg:{},
      node:{},
      lable:{},
      data: {},
      root: {},
      focus: {},
      view: {}
    };
  },
  methods: {
    createSvg() {
      this.svg = d3
        .select("#chart")
        .append("svg")
        .attr("viewBox", `-${width / 2} -${height / 2} ${width} ${height}`)
        .style("display", "block")
        .style("margin", "0 -14px")
        .style("background", color(0))
        .style("cursor", "pointer")
        .on("click", () => this.zoom(this.root));
      
      this.node = this.svg
        .append("g")
        .selectAll("circle")
        .data(this.root.descendants().slice(1))
        .join("circle")
        .attr("fill", d => (d.children ? color(d.depth) : "white"))
        .attr("pointer-events", d => (!d.children ? "none" : null))
        .on("mouseover", function() {
          d3.select(this).attr("stroke", "#000");
        })
        .on("mouseout", function() {
          d3.select(this).attr("stroke", null);
        })
        .on("click", d => focus !== d && (this.zoom(d), d3.event.stopPropagation()));

      this.label = this.svg
        .append("g")
        .style("font", "18px Charlemagne Std")
        .attr("fill",'#000')
        .attr("pointer-events", "none")
        .attr("text-anchor", "middle")
        .selectAll("text")
        .data(this.root.descendants())
        .join("text")
        .style("fill-opacity", d => (d.parent === this.root ? 1 : 0))
        .style("display", d => (d.parent === this.root ? "inline" : "none"))
        .text(d => d.data.name);
    },
    getData() {
      this.data = testdata;
      this.root = pack(this.data);
      this.focus = this.root;
    },
    zoomTo(v) {
      const k = v[0]<v[1] ? width / v[2] : height / v[2];

      this.view = v;

      this.label.attr(
        "transform",
        d => d.x && d.y ? `translate(${(d.x - v[0]) * k},${(d.y - v[1]) * k})`:'translate( 0, 0 )'
      );
      this.node.attr(
        "transform",
        d => d.x && d.y ? `translate(${(d.x - v[0]) * k},${(d.y - v[1]) * k})`:'translate( 0, 0 )'
      );
      this.node.attr("r", d => d.r * k);
    },
    zoom(d) {
      const focus0 = focus;

      focus = d;

      const transition = this.svg
        .transition()
        .duration(d3.event.altKey ? 7500 : 750)
        .tween("zoom", d => {
          const i = d3.interpolateZoom(this.view, [focus.x, focus.y, focus.r * 2]);
          return t => this.zoomTo(i(t));
        });

      this.label
        .filter(function(d) {
          return d.parent === focus || this.style.display === "inline";
        })
        .transition(transition)
        .style("fill-opacity", d => (d.parent === focus ? 1 : 0))
        .on("start", function(d) {
          if (d.parent === focus) this.style.display = "inline";
        })
        .on("end", function(d) {
          if (d.parent !== focus) this.style.display = "none";
        });
    }
  },
  mounted() {
    this.getData();
    this.createSvg();
    this.zoomTo([this.root.x, this.root.y, this.root.r * 2]);
  }
};
</script>