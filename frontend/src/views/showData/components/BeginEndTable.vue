<template>
  <el-table :data="options" stripe style="width: 100%">
    <el-table-column prop="time" label="异常时间" width="180"></el-table-column>
    <el-table-column
      prop="index"
      label="异常入口指标"
      width="180"
    ></el-table-column>
  </el-table>
</template>

<script>
import global from '../global'

export default {
  data() {
    return {
      options: [
        {
          time: '2020-04-11 01:41:00',
          index: 'os_021',
        },{
          time:"2020-04-11 02:15:00",
          index:"succee_rate"
        },{
          time:"2020-04-11 02:51:00",
          index:"docker_002"
        },{
          time:"2020-04-11 03:21:00",
          index:"num"
        },
        {
          time: '2020-04-11 03:56:00',
          index: 'num',
        },
        {
          time: '2020-04-11 04:41:00',
          index: 'docker_002',
        },
        {
          time: '2020-04-11 05:45:00',
          index: 'succee_num',
        },
      ],
    }
  },
  methods: {
    setData(param) {
      let data = param.Alarm
      this.options = []
      data.map((i) => {
        let tmp = {}
        tmp.begin = global.timestampToTime(i[0])
        tmp.end = global.timestampToTime(i[1])
        this.options.push(tmp)
      })
    },
  },
}
</script>

<style></style>
