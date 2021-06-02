<template>
  <div>
    <el-form label-width="100px">
      <el-form-item label="选择异常时刻:">
        <el-select v-model="kpi" placeholder="选择想要查询的异常时刻" @change="change">
          <el-option v-for="item in times" :key="item.value" :label="item.label" :value="item.value"></el-option>
        </el-select>
      </el-form-item>
    </el-form>

    <el-table :data="tableData1" style="width: 100%">
      <el-table-column prop="event" label="推荐根因" width="180"></el-table-column>
      <el-table-column prop="relate" label="随机行走命中次数" width="180"></el-table-column>
    </el-table>
  </div>
</template>

<script>'7'
import global from "../global";
import axios from 'axios'

export default {
  data() {
    return {
      times: global.times,
      kpi: "",
      // tableData: [{ event: "", relate: "" }]
      tableData1:[]
    };
  },
  methods: {
    change() {
      // let formData = new FormData();
      // formData.append('kpi',this.kpi);
      // axios.post(global.url+"/getKpiCorrelation",formData).then(res=>{
      //     this.tableData = res.data.result;
      // })
      if (this.kpi == 1){
        this.tableData1 = [
          {
            event:"platform-kpi--os_021--CPU_util_pct",
            relate:11
          },
          {
            event:'platform-kpi--os_021--Incoming_network_traffic',
            relate:122
          }
        ]
      } else if (this.kpi == 2){
        this.tableData1 = [
          {
            event:'platform-kpi--docker_004--container_cpu_used',
            relate:1
          }
        ]
      } else if (this.kpi == 3){
        this.tableData1 = [
          {
            event:'platform-kpi--docker_002--container_cpu_used',
            relate:59
          }
        ]        
      }
      // console.log("kpi:",this.kpi)
      // console.log ("tabledata",this.tableData1)
    }
  }
};
</script>

<style>
</style>