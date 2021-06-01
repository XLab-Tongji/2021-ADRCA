# %%
import influx_api

# %%
start_time = 1614268800
end_time = 1614960000
system_name = 'a'
cmdb_id = 'gjjcore2'
kpi_name = 'system.mem.free'

# %%
influx_api.query_metric(system_name, cmdb_id, kpi_name, start_time, end_time)

# %%
influx_api.query_metric_list(system_name, cmdb_id)

# %%
influx_api.query_cmdbid_list(system_name)

# %%
influx_api.query_all_metric(system_name, cmdb_id, start_time, end_time)

# %%
start_time = 1614268800
end_time = 1614960000
system_name = 'a'
kpi_name = 'sr'

# %%
influx_api.query_kpi(system_name, kpi_name, start_time, end_time)

# %%
influx_api.query_all_kpi(system_name, start_time, end_time)

# %%
influx_api.query_kpi2('business-kpi', 'avg_time', 0, 1614960000)

# %%
influx_api.query_all_kpi2('business-kpi', 0, 1614960000)

# %%
influx_api.query_metric2('business-kpi', 'os_021', 'CPU_util_pct', 0, 1614960000)


# %%
pass
influx_api.query_all_metric2('business-kpi', 'os_021', 0, 1614960000)

# %%
influx_api.query_metric_list2('business-kpi', 'container_001')
