### metrics相关接口

#### 指定系统全部黄金指标kpi获取

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

#### 指定系统指定黄金指标kpi获取

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

#### 指定系统指定cmdb_id全部运维指标metric获取

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

#### 指定系统指定cmdb_id指定运维指标metric获取

**功能**：输入系统名、cmdb_id、kpi_name、起始时间和终止时间，返回时间段内，该cmdb_id、kpi_name对应的kpi时间序列。

**输入**：

- a or b
- cmdb_id
- kpi_name
- start_time
- end_time

**返回**：

- 一个Series，查询到的对应kpi时间序列

#### 指定系统全部cmdb_id获取

**功能**：输入系统名，返回该系统中全部cmdb_id。

**输入**：

- a or b

**返回**：

- 一个Series，查询到的cmdb_id列表

#### 指定系统指定cmdb_id全部运维指标metric_name获取

**功能**：输入系统名、cmdb_id，返回该系统中全部metric_name。

**输入**：

- a or b
- cmdb_id

**返回**：

- 一个Series，查询到的metric_name列表