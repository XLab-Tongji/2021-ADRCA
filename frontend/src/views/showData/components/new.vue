<template>
  <div>
    <el-form label-width="100px">
      <el-form-item label="选择异常时刻:">
        <el-select
          v-model="kpi"
          placeholder="选择想要查询的异常时刻"
          @change="change"
        >
          <el-option
            v-for="item in times"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          ></el-option>
        </el-select>
      </el-form-item>
    </el-form>

    <el-table :data="tableData1" style="width: 100%">
      <el-table-column
        prop="event"
        label="推荐根因"
        width="180"
      ></el-table-column>
      <el-table-column
        prop="relate"
        label="随机行走命中次数"
        width="180"
      ></el-table-column>
    </el-table>
  </div>
</template>

<script>
'7'
import global from '../global'
import axios from 'axios'

export default {
  data() {
    return {
      times: global.times,
      kpi: '',
      // tableData: [{ event: "", relate: "" }]
      tableData1: [],
    }
  },
  methods: {
    change() {
      // let formData = new FormData();
      // formData.append('kpi',this.kpi);
      // axios.post(global.url+"/getKpiCorrelation",formData).then(res=>{
      //     this.tableData = res.data.result;
      // })
      if (this.kpi == 1) {
        this.tableData1 = [
          {
            event: 'platform-kpi--os_021--Memory_used',
            relate: 120,
          },
          {
            event: 'platform-kpi--os_021--Processor_load_15_min',
            relate: 100,
          },
          {
            event: 'platform-kpi--os_021--Disk_wr_ios',
            relate: 88,
          },
          {
            event: 'platform-kpi--os_021--Memory_available_pct',
            relate: 75,
          },
          {
            event: 'platform-kpi--os_021--Memory_used_pc',
            relate: 52,
          },
          {
            event: 'platform-kpi--os_021--Processor_load_1_min',
            relate: 33,
          },
          {
            event: 'platform-kpi--os_021--Page_po',
            relate: 20,
          },
          {
            event: 'platform-kpi--os_021--Processor_load_5_min',
            relate: 20,
          },
          {
            event: 'platform-kpi--os_021--CPU_util_pct',
            relate: 10,
          },
          {
            event: 'platform-kpi--os_021--Recv_total',
            relate: 9,
          },
          {
            event: 'platform-kpi--os_021--Disk_wr_kbs',
            relate: 8,
          },
          {
            event: 'platform-kpi--os_021--Outgoing_network_traffico',
            relate: 7,
          },
          {
            event: 'platform-kpi--os_021--CPU_idle_pct',
            relate: 5,
          },
          {
            event: 'platform-kpi--os_021--Send_total',
            relate: 5,
          },
          {
            event: 'platform-kpi--os_021--CPU_system_time',
            relate: 1,
          },
        ]
      } else if (this.kpi == 2) {
        this.tableData1 = [
          {
            event: 'platform-kpi--docker_007--container_cpu_used',
            relate: 140,
          },
        ]
      } else if (this.kpi == 3) {
        this.tableData1 = [
          {
            event: 'platform-kpi--docker_002--container_cpu_used',
            relate: 48,
          },
        ]
      }else if (this.kpi == 4) {
        this.tableData1 = [
          {
            event: 'platform-kpi--docker_005--container_cpu_used',
            relate: 79,
          },
        ]
      }else if (this.kpi == 5) {
        this.tableData1 = [
          {
            event: 'platform-kpi--docker_004--container_cpu_used',
            relate: 81,
          },
        ]
      }else if (this.kpi == 6) {
        this.tableData1 = [
          {
            event: 'platform-kpi--docker_001--container_cpu_used',
            relate: 70,
          },
        ]
      }else if (this.kpi == 7) {
        this.tableData1 = [
          {
            event: 'platform-kpi--docker_002--container_cpu_used',
            relate: 77,
          },
        ]
      }
      // console.log("kpi:",this.kpi)
      // console.log ("tabledata",this.tableData1)
    },
  },
}
</script>

<style></style>
