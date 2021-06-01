<template>
  <div id="hi"></div>
</template>

<script>
import Dygraph from "dygraphs";
import data from "../showData/data/data.json";
import global from '../showData/global'

export default {
  methods: {
    setData(data) {
      let sst = data.SST;
      let csv = "a,b\n";
      if (sst) {
        sst.map(i => {
          csv += global.timestampToTime(i[0]) + "," + i[1] + "\n";
        });
      }
      // console.log(csv);
      let width = document.documentElement.clientWidth;
      let height = document.documentElement.clientHeight;
      let g = new Dygraph(document.getElementById("hi"), csv, {
        valueRange: [-1, 1],
        drawAxesAtZero: true,
        height:height/2,
        width:width/2
      });
    }
  }
};
</script>

<style>
</style>