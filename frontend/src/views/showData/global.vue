<script>
import global from '../global'
const kpis = [
  {
    value: '1',
    label: 'avg_time',
  },
  {
    value: '2',
    label: 'num',
  },
  {
    value: '3',
    label: 'succee_num',
  },
  {
    value: '4',
    label: 'succee_rate',
  },
]
const times = [
  {
    value: '1',
    label: '2020-04-11 01:41:00',
  },{
    value: '2',
    label: '2020-04-11 02:15:00',
  },{
    value: '3',
    label: '2020-04-11 02:51:00',
  },{
    value: '4',
    label: '2020-04-11 03:21:00',
  },
  {
    value: '5',
    label: '2020-04-11 03:56:00',
  },
  {
    value: '6',
    label: '2020-04-11 04:41:00',
  },
  {
    value: '7',
    label: '2020-04-11 05:45:00',
  },
]
const url = global.base_url
const timestampToTime = (timestamp) => {
  var date = new Date(timestamp * 1000) //时间戳为10位需*1000，时间戳为13位的话不需乘1000
  var Y = date.getFullYear() + '-'
  var M =
    (date.getMonth() + 1 < 10
      ? '0' + (date.getMonth() + 1)
      : date.getMonth() + 1) + '-'
  var D = (date.getDate() < 10 ? '0' + date.getDate() : date.getDate()) + ' '
  var h = (date.getHours() < 10 ? '0' + date.getHours() : date.getHours()) + ':'
  var m =
    (date.getMinutes() < 10 ? '0' + date.getMinutes() : date.getMinutes()) + ':'
  var s = date.getSeconds() < 10 ? '0' + date.getSeconds() : date.getSeconds()
  return Y + M + D + h + m + s
}
export default {
  url,
  timestampToTime,
  kpis,
  times,
}
</script>
