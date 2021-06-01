from influxdb_client.rest import ApiException
import pandas as pd
from influxdb_client import InfluxDBClient

# You can generate a Token from the "Tokens Tab" in the UI
token = "B8VrjXVlgsrdWrrJces6_uokTo75AxLTDMIeyROfaks2FIjTJpdqYlbrOUtcktG0zfYiv2T8AoJlJ23GrfwtKA=="
org = "Tongji"
client = InfluxDBClient(url="http://10.60.38.173:18086", token=token)
query_api = client.query_api()


def query_all_kpi(system_name, start_time, end_time):
    '''
    系统全部黄金指标kpi获取

    **功能**：输入系统名、起始时间和终止时间，返回时间段内，按交易码和kpi_name划分的全部的kpi时间序列。

    **输入**：

    - a or b
    - start_time
    - end_time

    **返回**：

    - 一个DataFrame，其中：
    - data : 查询到的对应kpi时间序列
    - columns : a or b + '--' + kpi_name + '\--' + "tc$x$" (e.g. "a--mrt--tc1")
    - index : timestamp
    '''

    flux = f'''
    from(bucket: "kpi")
    |> range(start: {start_time}, stop: {end_time})
    |> filter(fn: (r) => r["system"] == "system-{system_name}")
    |> group(columns: ["_field","tc"])
    |> keep(columns: ["_field","tc","_time","_value"])
    '''
    print(flux)
    try:
        data = query_api.query_data_frame(flux, org)
    except ApiException as ex:
        raise ex
    data['_time'] = data['_time'].apply(lambda x: int(x.timestamp()))
    data.set_index('_time', inplace=True)

    res = pd.DataFrame(index=data.index)
    for kpi_name in data['_field'].unique():
        for tc in data['tc'].unique():
            new_measurement_name = f'{system_name}--{kpi_name}--tc{tc}'
            res[new_measurement_name] = data['_value'].loc[
                (data['_field'] == kpi_name) & (data['tc'] == tc)]
    return res


def query_kpi(system_name, kpi_name, start_time, end_time):
    '''
    指定系统指定黄金指标kpi获取

    **功能**：输入系统名、kpi_name、起始时间和终止时间，返回时间段内，按交易码划分的全部的kpi时间序列。

    **输入**：

    - a or b
    - kpi_name
    - start_time
    - end_time

    **返回**：

    - 一个DataFrame，其中：
    - data : 查询到的对应kpi时间序列
    - columns : a or b + '--' + kpi_name + '\--' + "tc$x$" (e.g. "a--mrt--tc1")
    - index : timestamp
    '''

    flux = f'''
    from(bucket: "kpi")
    |> range(start: {start_time}, stop: {end_time})
    |> filter(fn: (r) => r["system"] == "system-{system_name}")
    |> filter(fn: (r) => r["_field"] == "{kpi_name}")
    |> group(columns: ["tc"])
    |> keep(columns: ["_time","tc","_value"])
    '''
    print(flux)
    try:
        data = query_api.query_data_frame(flux, org)
    except ApiException as ex:
        raise ex
    if data.empty:
        return data
    data['_time'] = data['_time'].apply(lambda x: int(x.timestamp()))
    data.set_index('_time', inplace=True)

    res = pd.DataFrame(index=data.index)
    for tc in data['tc'].unique():
        new_measurement_name = f'{system_name}--{kpi_name}--tc{tc}'
        res[new_measurement_name] = data['_value'][data['tc'] == tc]
    return res


def query_all_metric(system_name, cmdb_id, start_time, end_time):
    '''
    指定系统指定cmdb_id全部运维指标metric获取

    **功能**：输入系统名、cmdb_id、起始时间和终止时间，返回时间段内，该cmdb_id对应的全部的kpi时间序列。

    **输入**：

    - a or b
    - cmdb_id
    - start_time
    - end_time

    **返回**：

    - 一个DataFrame，其中：
    - data : 查询到的对应kpi时间序列
    - columns : a or b + '\--' + cmdb_id + '\--' + kpi_name(e.g. "a--gjjweb001--system.cpu.guest")
    - index : timestamp
    '''

    flux = f'''
    from(bucket: "metrics")
    |> range(start: {start_time}, stop: {end_time})
    |> filter(fn: (r) => r["system"] == "system-{system_name}")
    |> filter(fn: (r) => r["entity"] == "{cmdb_id}")
    |> keep(columns: ["_time","_measurement","_value"])
    '''
    print(flux)
    try:
        data = query_api.query_data_frame(flux, org)
    except ApiException as ex:
        raise ex
    data['_time'] = data['_time'].apply(lambda x: int(x.timestamp()))
    data.set_index('_time', inplace=True)

    res = pd.DataFrame(index=data.index)
    for measurement in data['_measurement'].unique():
        new_measurement_name = f'{system_name}--{cmdb_id}--{measurement}'
        res[new_measurement_name] = data['_value'][data['_measurement'] == measurement]
    return res


def query_metric(system_name, cmdb_id, kpi_name, start_time, end_time):
    '''
    指定系统指定cmdb_id指定运维指标metric获取

    **功能**：输入系统名、cmdb_id、kpi_name、起始时间和终止时间，返回时间段内，该cmdb_id、kpi_name对应的kpi时间序列。

    **输入**：

    - a or b
    - cmdb_id
    - kpi_name
    - start_time
    - end_time

    **返回**：

    - 一个Series，查询到的对应kpi时间序列
    '''
    flux = f'''
    from(bucket: "metrics")
    |> range(start: {start_time}, stop: {end_time})
    |> filter(fn: (r) => r["system"] == "system-{system_name}")
    |> filter(fn: (r) => r["entity"] == "{cmdb_id}")
    |> filter(fn: (r) => r["_measurement"] == "{kpi_name}")
    '''
    print(flux)
    try:
        data = query_api.query_data_frame(flux, org)
    except ApiException as ex:
        raise ex
    if data.empty:
        return data
    data['_time'] = data['_time'].apply(lambda x: int(x.timestamp()))
    return data.set_index('_time')['_value']


def query_cmdbid_list(system_name):
    '''
    指定系统全部cmdb_id获取

    **功能**：输入系统名，返回该系统中全部cmdb_id。

    **输入**：

    - a or b

    **返回**：

    - 一个Series，查询到的cmdb_id列表
    '''
    flux = f'''
    from(bucket: "metrics")
    |> range(start: 0)
    |> filter(fn: (r) => r["system"] == "system-{system_name}")
    |> group()
    |> unique(column: "entity")
    |> keep(columns: ["entity"])
    '''
    print(flux)
    try:
        data = query_api.query_data_frame(flux, org)
    except ApiException as ex:
        raise ex
    return data['entity']


def query_metric_list(system_name, cmdb_id):
    '''
    指定系统指定cmdb_id全部运维指标metric_name获取

    **功能**：输入系统名、cmdb_id，返回该系统中全部metric_name。

    **输入**：

    - a or b
    - cmdb_id

    **返回**：

    - 一个Series，查询到的metric_name列表
    '''

    flux = f'''
    from(bucket: "metrics")
    |> range(start: 0)
    |> filter(fn: (r) => r["system"] == "system-{system_name}")
    |> filter(fn: (r) => r["entity"] == "{cmdb_id}")
    |> group()
    |> unique(column: "_measurement")
    |> keep(columns: ["_measurement"])
    '''

    try:
        data = query_api.query_data_frame(flux, org)
    except ApiException as ex:
        raise ex
    return data['_measurement']


def query_all_kpi2(system_name, start_time, end_time):
    '''
    系统全部黄金指标kpi获取

    **功能**：输入系统名、起始时间和终止时间，返回时间段内，按交易码和kpi_name划分的全部的kpi时间序列。

    **输入**：

    - fixed: 'business-kpi'
    - start_time
    - end_time

    **返回**：

    - 一个DataFrame，其中：
    - data : 查询到的对应kpi时间序列
    - columns : a or b + '--' + kpi_name + '\--' + "tc$x$" (e.g. "a--mrt--tc1")
    - index : timestamp
    '''
    system_name = 'business-kpi'

    flux = f'''
    from(bucket: "kpi")
    |> range(start: {start_time}, stop: {end_time})
    |> filter(fn: (r) => r["system"] == "{system_name}")
    |> group(columns: ["_field","cmdb_id"])
    |> keep(columns: ["_field","cmdb_id","_time","_value"])
    '''
    print(flux)
    try:
        data = query_api.query_data_frame(flux, org)
    except ApiException as ex:
        raise ex
    if isinstance(data, list):
        data = pd.concat(data)
    data['_time'] = data['_time'].apply(lambda x: int(x.timestamp()))
    data.set_index('_time', inplace=True)

    res = pd.DataFrame(index=data.index)
    for kpi_name in data['_field'].unique():
        for cmdb_id in data['cmdb_id'].unique():
            new_measurement_name = f'{system_name}--{kpi_name}--{cmdb_id}'
            res[new_measurement_name] = data['_value'].loc[
                (data['_field'] == kpi_name) & (data['cmdb_id'] == cmdb_id)]
    return res


def query_kpi2(system_name, kpi_name, start_time, end_time):
    '''
    指定系统指定黄金指标kpi获取

    **功能**：输入系统名、kpi_name、起始时间和终止时间，返回时间段内，按交易码划分的全部的kpi时间序列。

    **输入**：

    - fixed: 'business-kpi'
    - kpi_name
    - start_time
    - end_time

    **返回**：

    - 一个Series: 查询到的对应kpi时间序列
    - index : timestamp
    '''

    system_name = 'business-kpi'

    flux = f'''
    from(bucket: "kpi")
    |> range(start: {start_time}, stop: {end_time})
    |> filter(fn: (r) => r["system"] == "{system_name}")
    |> filter(fn: (r) => r["_field"] == "{kpi_name}")
    |> keep(columns: ["_time","cmdb_id","_value"])
    '''
    print(flux)
    try:
        data = query_api.query_data_frame(flux, org)
    except ApiException as ex:
        raise ex
    if data.empty:
        return data
    data['_time'] = data['_time'].apply(lambda x: int(x.timestamp()))
    data.set_index('_time', inplace=True)

    res = pd.DataFrame(index=data.index)
    for cmdb_id in data['cmdb_id'].unique():
        new_measurement_name = f'{system_name}--{kpi_name}--{cmdb_id}'
        res[new_measurement_name] = data['_value'][data['cmdb_id'] == cmdb_id]
    return res


def query_all_metric2(system_name, cmdb_id, start_time, end_time):
    '''
    指定系统指定cmdb_id全部运维指标metric获取

    **功能**：输入系统名、cmdb_id、起始时间和终止时间，返回时间段内，该cmdb_id对应的全部的kpi时间序列。

    **输入**：

    - a or b
    - cmdb_id
    - start_time
    - end_time

    **返回**：

    - 一个DataFrame，其中：
    - data : 查询到的对应kpi时间序列
    - columns : a or b + '\--' + cmdb_id + '\--' + kpi_name(e.g. "a--gjjweb001--system.cpu.guest")
    - index : timestamp
    '''
    system_name = 'platform-kpi'

    flux = f'''
    from(bucket: "metrics")
    |> range(start: {start_time}, stop: {end_time})
    |> filter(fn: (r) => r["system"] == "{system_name}")
    |> filter(fn: (r) => r["cmdb_id"] == "{cmdb_id}")
    |> keep(columns: ["_time","_measurement","_value"])
    '''
    print(flux)
    try:
        data = query_api.query_data_frame(flux, org)
    except ApiException as ex:
        raise ex
    if isinstance(data, list):
        data = pd.concat(data)
    data['_time'] = data['_time'].apply(lambda x: int(x.timestamp()))
    data = data[~data.duplicated(subset=['_measurement', '_time'], keep=False)]
    data.set_index('_time', inplace=True)

    res = pd.DataFrame(index=data.index)
    for measurement in data['_measurement'].unique():
        new_measurement_name = f'{system_name}--{cmdb_id}--{measurement}'
        res[new_measurement_name] = data[data['_measurement'] == measurement]['_value']
    return res


def query_metric2(system_name, cmdb_id, kpi_name, start_time, end_time):
    '''
    指定系统指定cmdb_id指定运维指标metric获取

    **功能**：输入系统名、cmdb_id、kpi_name、起始时间和终止时间，返回时间段内，该cmdb_id、kpi_name对应的kpi时间序列。

    **输入**：

    - a or b
    - cmdb_id
    - kpi_name
    - start_time
    - end_time

    **返回**：

    - 一个Series，查询到的对应kpi时间序列
    '''

    system_name = 'platform-kpi'

    flux = f'''
    from(bucket: "metrics")
    |> range(start: {start_time}, stop: {end_time})
    |> filter(fn: (r) => r["system"] == "{system_name}")
    |> filter(fn: (r) => r["cmdb_id"] == "{cmdb_id}")
    |> filter(fn: (r) => r["_measurement"] == "{kpi_name}")
    '''
    print(flux)
    try:
        data = query_api.query_data_frame(flux, org)
    except ApiException as ex:
        raise ex
    if data.empty:
        return data
    data['_time'] = data['_time'].apply(lambda x: int(x.timestamp()))
    return data.set_index('_time')['_value']


def query_metric_list2(system_name, cmdb_id):
    '''
    指定系统指定cmdb_id全部运维指标metric_name获取

    **功能**：输入系统名、cmdb_id，返回该系统中全部metric_name。

    **输入**：

    - a or b
    - cmdb_id

    **返回**：

    - 一个Series，查询到的metric_name列表
    '''
    system_name = 'platform-kpi'

    flux = f'''
    from(bucket: "metrics")
    |> range(start: 0)
    |> filter(fn: (r) => r["system"] == "{system_name}")
    |> filter(fn: (r) => r["cmdb_id"] == "{cmdb_id}")
    |> group()
    |> unique(column: "_measurement")
    |> keep(columns: ["_measurement"])
    '''

    try:
        data = query_api.query_data_frame(flux, org)
    except ApiException as ex:
        raise ex
    return data['_measurement']
