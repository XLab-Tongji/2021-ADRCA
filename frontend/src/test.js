const {InfluxDB} = require('@influxdata/influxdb-client')

// You can generate a Token from the "Tokens Tab" in the UI
const token = 'B8VrjXVlgsrdWrrJces6_uokTo75AxLTDMIeyROfaks2FIjTJpdqYlbrOUtcktG0zfYiv2T8AoJlJ23GrfwtKA=='
const org = 'Tongji'
const bucket = 'AIOps'

const client = new InfluxDB({url: 'http://10.60.38.173:18086', token: token})

const queryApi = client.getQueryApi(org)

start_time = 1586536860
end_time = 1586540460
system_name = 'business-kpi'
kpi_name = "os_021"

const query = 'from(bucket: "metrics")' +
'|> range(start: ' + start_time +', stop: ' + end_time + ')' + 
'|> filter(fn: (r) => r["system"] == "' + system_name + '")' +
'|> filter(fn: (r) => r["_measurement"] == "' + kpi_name + '")' + 
'|> keep(columns: ["_time","cmdb_id","_value"])'

queryApi.queryRows(query, {
  next(row, tableMeta) {
    const o = tableMeta.toObject(row)
    // console.log(
    //   \`\${o._time} \${o._measurement} in \'\${o.location}\' (\${o.example}): \${o._field}=\${o._value}\`
    // ) 
    console.log(o)
  },
  error(error) {
    console.error(error)
    console.log('\\nFinished ERROR')
  },
  complete() {
    console.log('\\nFinished SUCCESS')
  },
})