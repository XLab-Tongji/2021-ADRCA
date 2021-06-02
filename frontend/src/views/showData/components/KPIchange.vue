<template>
  <!-- <div> -->
  <!-- <dy ref="dy"/> -->
  <!-- <chart :options="options" :init-options="initOptions" autoresize /> -->
  <!-- </div> -->
  <!--为echarts准备一个具备大小的容器dom-->
  <div>
    <!-- {{typeof(kpi_data)}} -->
    <div id="main" style="width: 700px;height: 400px;"></div>
  </div>
</template>

<script>
import * as echarts from 'echarts'
import avg_time_data from '../data/data'
export default {
  props: ['key_name', 'time_data', 'kpi_data'],
  name: '',
  data() {
    return {
      charts: '',
      /*	opinion: ["1", "3", "3", "4", "5"],*/
      opinionData: ['3', '2', '4', '4', '5'],
    }
  },
  watch: {
    kpi_data: {
      // redraw(){
      //   console.log("happened")
      //   drawLine("main")
      handler(newName, oldName) {
        console.log('happened')
        this.$nextTick(function() {
          this.drawLine('main')
        })
      },
      deep: true,
      immediate: true,
    },
  },
  methods: {
    drawLine(id) {
      this.charts = echarts.init(document.getElementById(id))
      // console.log('motherasd')
      this.charts.setOption({
        tooltip: {
          trigger: 'axis',
        },
        legend: {
          data: ['近七日收益'],
        },
        grid: {
          left: '10%',
          right: '10%',
          bottom: '10%',
          containLabel: true,
        },

        toolbox: {
          feature: {
            saveAsImage: {},
          },
        },
        xAxis: {
          name:   'date' ,
          type: 'category',
          data: this.time_data,
        },
        yAxis: {
          name: this.key_name + ' value',
          type: 'value',
        },
        series: [
          {
            data: this.kpi_data,
            type: 'line',
            smooth: true,
          },
        ],
        title: {
          text: this.key_name + ' kpi数据',
        },
      })
    },
  },
  // 调用
  mounted() {
    // this.$nextTick(function() {
    //   this.drawLine('main')
    // })
  },
}
</script>
<style scoped>
* {
  margin: 0;
  padding: 0;
  list-style: none;
}
</style>
