<template>
  <div class="KB">
    <div class="select">
      <span>选择想要查询的KPI </span>
      <el-select v-model="value" placeholder="KPI" @change="change()">
        <el-option
          v-for="item in kpi"
          :key="item.value"
          :label="item.label"
          :value="item.label"
        ></el-option>
      </el-select>
    </div>
    <div class="K">
      <K
        ref="k"
        :key_name="value"
        :time_data="time_data"
        :kpi_data="kpi_data"
      />
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
import K from '../components/KPIchange'
import B from '../components/BeginEndTable'
import axios from 'axios'
import global from '../global'

export default {
  components: {
    K,
    B,
  },
  data() {
    return {
      kpi: global.kpis,
      value: '',
      distance: '',
      time_data: [],
      kpi_data: [],
    }
  },
  methods: {
    async change() {
      this.time_data = []
      this.kpi_data = []
      var that = this
      const { InfluxDB } = require('@influxdata/influxdb-client')
      const token =
        'B8VrjXVlgsrdWrrJces6_uokTo75AxLTDMIeyROfaks2FIjTJpdqYlbrOUtcktG0zfYiv2T8AoJlJ23GrfwtKA=='
      const org = 'Tongji'
      const client = new InfluxDB({
        url: 'http://10.60.38.173:18086',
        token: token,
      })
      const queryApi = client.getQueryApi(org)
      var start_time = 1586534400
      var end_time = 1586620800
      var system_name = 'business-kpi'
      var kpi_name = this.value
      const query =
        'from(bucket: "kpi")' +
        '|> range(start: ' +
        start_time +
        ', stop: ' +
        end_time +
        ')' +
        '|> filter(fn: (r) => r["system"] == "' +
        system_name +
        '")' +
        '|> filter(fn: (r) => r["_field"] == "' +
        kpi_name +
        '")' +
        '|> keep(columns: ["_time","_value"])'
      console.log(query)


      queryApi.queryRows(query, {
        next(row, tableMeta) {
          const o = tableMeta.toObject(row)
          // console.log('o_value:', o._time)
          var utc_datetime = o._time
          var T_pos = utc_datetime.indexOf('T')
          var Z_pos = utc_datetime.indexOf('Z')
          var year_month_day = utc_datetime.substr(0, T_pos)
          var hour_minute_second = utc_datetime.substr(
            T_pos + 1,
            Z_pos - T_pos - 1
          )
          var new_datetime = year_month_day + ' ' + hour_minute_second
          // 处理成为时间戳
          var timestamp = new Date(Date.parse(new_datetime))
          timestamp = timestamp.getTime()
          timestamp = timestamp / 1000

          // 增加8个小时，北京时间比utc时间多八个时区
          var timestamp = timestamp + 8 * 60 * 60

          // 时间戳转为时间
          var beijing_datetime = new Date(parseInt(timestamp) * 1000)
            .toLocaleString()
            .replace(/年|月/g, '-')
            .replace(/日/g, ' ')
          that.time_data.push(beijing_datetime)
          that.kpi_data.push(o._value)
        },
        error(error) {
          console.error(error)
          console.log('\nFinished ERROR')
        },
        complete() {
          // return res
          console.log('\nFinished SUCCESS')
        },
      })
      // console.log('time_data:', this.time_data)
      // console.log('kpi_data:', this.kpi_data)
    },
    setK(data) {
      this.$refs.k.setData(data)
    },
    setB(data) {
      this.$refs.b.setData(data)
    },
  },
}
</script>

<style>
.select {
  padding-top: 10px;
  padding-bottom: 10px;
}

.table {
  overflow-y: auto;
  height: 200px;
}
</style>
