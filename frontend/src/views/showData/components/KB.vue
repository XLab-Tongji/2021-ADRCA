<template>
  <div class="KB">
    <div class="select">
      <el-select v-model="value" placeholder="选择想要查询的KPI" @change="change">
        <el-option v-for="item in kpi" :key="item.value" :label="item.label" :value="item.value"></el-option>
      </el-select>
    </div>
    <div class="K">
      <K ref="k" />
    </div>
    <div class="B">
      <el-collapse>
        <el-collapse-item title="查看异常时刻表" name="1">
          <B ref="b" />
        </el-collapse-item>
      </el-collapse>
    </div>
  </div>
</template>

<script>
import K from "../components/KPIchange";
import B from "../components/BeginEndTable";
import axios from "axios";
import global from "../global";

export default {
  components: {
    K,
    B
  },
  data() {
    return {
      kpi: global.kpis,
      value: "",
      distance:""
    };
  },
  methods: {
    change() {
      let formData = new FormData();
      formData.append("kpi", this.value);
      axios.post(global.url + "/getClusterCSV", formData).then(res => {
        console.log(res.data)
        this.setK(res.data);
        this.setB(res.data);
      });
      axios.post(global.url + "/distance", formData).then(res => {
        this.distance = res.data.distance;
      });
    },
    setK(data) {
      this.$refs.k.setData(data);
    },
    setB(data) {
      this.$refs.b.setData(data);
    }
  }
};
</script>

<style>
.select {
  padding-top:10px;
  padding-bottom:10px;
}

.table{
overflow-y:auto; 
height:200px;
}
</style>
