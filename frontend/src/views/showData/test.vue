<template>
  <div class="algo">
    <el-card class="box">
    <div class="kpi">
      <KB />
    </div>
    </el-card>
    <el-card class="box">
    <div class="graph">
      <SG />
    </div>
    </el-card>
    <el-popover placement="right" width="400" trigger="hover">
      <Ima />
      <el-button slot="reference">hover查看聚类分析</el-button>
    </el-popover>
    <!-- <div class="img">
      <Ima />
    </div>-->
  </div>
</template>

<script>
import KB from "../showData/components/KB";
// import SG from "../showData/components/SG";
import SG from "../showData/components/new";
import Ima from "../showData/components/Image";

import d from "./data/data.json";

export default {
  components: {
    KB,
    SG,
    Ima
  },
  methods: {}
};
</script>

<style>
.algo {
  display: grid;
  
  grid-template-columns: 1.2fr 0.8fr;
  grid-template-rows: calc(100vh) auto;
  grid-column-gap: 20px;
  grid-row-gap: 15px;
}
.box{
 overflow-y:auto; 

}
.kpi {
  grid-column: 1/2;
  grid-row: 1/2;
  justify-self: stretch;
 align-items: stretch;
}
.graph {
  grid-column: 2/3;
  grid-row: 1/2;
   justify-self: stretch;
 align-items: stretch;
}
.img {
  grid-row: 2/3;
  justify-self: center;
  align-self: center;
}
.el-card, .el-message{
  border-radius: 0px

}
</style>