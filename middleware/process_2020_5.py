#!/usr/bin/env python
# coding: utf-8

# In[1]:

import influx_api
import json
import requests
import pandas as pd
import csv
import sched
import time
import os
import re
from utils import *
# 参数设置

# 一些参数设置
system_name = "business-kpi"

# current_time = "1586534400150" #代表"现在"时间

''' 
"1586548560" ->                                               platform-kpi--docker_004--container_cpu_used       num
platform-kpi--docker_004--container_cpu_used                                      0.002001  0.001093
num                                                                               0.698686  0.557382
[('num', 999), ('platform-kpi--docker_004--container_cpu_used', 1)]
"1586551260" ->
[('docker_002', 941), ('platform-kpi--docker_002--container_cpu_used', 59)]
"1586555100" -> Wrong Answer
'''

current_time = "1586538660" 
window_length = 7200  # 一次取数据的窗口长度/s

myurl = "http://10.60.38.173:5002/arima"  # arima接口address
myurl_performance = "http://10.60.38.173:5002/global_arima"  # 性能指标使用的arima接口address

true = False
false = True


# 最终异常实体性能指标检测结果存储
final_abnormal_index = []


# 修改性能指标数据名字
def index_name_trans(name):
    new_name = str(re.search(r'[^-]+$', name).group(0))
    return new_name

# 将静态调用链数据存储为df格式


# 处理去年的数据 处理为dataframe
def show_files(path, all_files):
    # 首先遍历当前目录所有文件及文件夹
    file_list = os.listdir(path)
    # 准备循环判断每个元素是否是文件夹还是文件，是文件的话，把名称传入list，是文件夹的话，递归
    for file in file_list:
        # 利用os.path.join()方法取得路径全名，并存入cur_path变量，否则每次只能遍历一层目录
        cur_path = os.path.join(path, file)
        # 判断是否是文件夹
        if os.path.isdir(cur_path):
            show_files(cur_path, all_files)
        else:
            print(file)
            cur_path = os.path.join(path, file)
            print("cur", cur_path)
            all_files.append([file, cur_path])

    return all_files


# 传入空的list接收文件名
contents = show_files("trace2020/trace_csf/", [])

# 去年的数据
trace2020_df_list = [0]
for content in contents:
    tmp_lst = []
    file = content[1]
    with open(file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            tmp_lst.append(row)
    df = pd.DataFrame(tmp_lst[1:], columns=tmp_lst[0])
#     df.set_index(["timestamp"],inplace=True)
    trace2020_df_list.append([content[0], df])
# print(trace2020_df_list)


# 取数据


# 取黄金指标数据


# 取黄金指标数据以进行异常检测

# 取去年的
def golden_index_data_2020(system_name, current_time, window_length):

    # 处理查询起始时间以使用influx接口
    start_time = int(current_time) - int(window_length) - 1
    end_time = int(current_time) + 1

    # kpi_name list
    kpi_list = ["avg_time", "num", "succee_num", "succee_rate"]

    res_list = []

    # data 字典模板
    res_dict_template = {
        "kpi_name": "",
        "is_seasonal": 0,
        "kpi_value": 0
    }

    # 对于所有kpi都要取出数据
    for kpi_name in kpi_list:
        data = influx_api.query_kpi2("business-kpi", kpi_name, str(start_time), str(end_time))
#         print(data)
        res_dict_template["kpi_name"] = kpi_name

        time_series = data.index.values.tolist()
        index_name = data.index.name

        # 处理返回数据格式
        for i in data.columns.tolist():
            res_list.append(res_dict_template.copy())
            df = pd.DataFrame({index_name: time_series, i: data[i].values.tolist()})
            df.rename(columns={"_time": "timestamp"}, inplace=True)
            df.set_index(["timestamp"])
            # print(df)
            res_list[-1]["kpi_value"] = df[df.columns.tolist()[-1]].values.tolist()[-1]
            res_list[-1]["data"] = []

            # print(list(df))
            df.rename(columns={list(df)[1]: kpi_name}, inplace=True)

            res_list[-1]["data"].append(df)
            res_list[-1]["data"][0] = res_list[-1]["data"][0].to_json(orient="records")
            res_list[-1]["data"][0] = json.loads(res_list[-1]["data"][0])
            res_list[-1]["data"] = res_list[-1]["data"][0][0:-1]

    return res_list


# 取调用链数据


# 取调用链数据以进行异常检测

# 取去年的数据
def call_chain_data_2020(current_time, window_length):

    # 处理查询起始时间以使用influx接口
    start_time = int(current_time) - int(window_length) - 1
    end_time = int(current_time) + 1

    res_list = []

    # data 字典模板
    res_dict_template = {
        "kpi_name": "",
        "is_seasonal": 0,
        "kpi_value": 0
    }

    # 遍历每一个实体的timeseries筛选数据
    n = 0
    for content in trace2020_df_list:
        if n == 0:
            n += 1
            continue

        df = content[1]

        new_df = df[(df['startTime'] <= str(end_time)) & (df['startTime'] >= str(start_time))]
        if new_df.empty:
            continue
        new_df.rename(columns={"startTime": "timestamp"}, inplace=True)
        new_df.rename(columns={"elapsedTime": content[0][0:-4]}, inplace=True)

        res_list.append(res_dict_template.copy())

        print(new_df)

        res_list[-1]["kpi_name"] = content[0][0:-4]
        res_list[-1]["kpi_value"] = float(new_df.values.tolist()[-1][1])

        res_list[-1]["data"] = []

        res_list[-1]["data"].append(new_df)
        # print(df_list[-1]["data"][0])
        res_list[-1]["data"][0] = res_list[-1]["data"][0].to_json(orient="records")
        res_list[-1]["data"][0] = json.loads(res_list[-1]["data"][0])
        res_list[-1]["data"] = res_list[-1]["data"][0][0:-1]

        n += 1
    return res_list


# 获取异常实体对应的全部性能指标数据


# 获取到异常实体后，查询实体对应的全部性能指标
def find_span_performance_index(system_name, cmdb_id, current_time, window_length):

    # 处理查询起始时间以使用influx接口
    start_time = int(current_time) - int(window_length) - 1
    # 需要多取10分钟数据
    end_time = int(current_time) + 600 + 1
    df = influx_api.query_all_metric2(system_name, cmdb_id, start_time, end_time)
    print(df)

    time_series = df.index.values.tolist()
    index_name = df.index.name
    df_list = []
    res_dict_template = {
        "kpi_name": ""
    }
    for i in df.columns.tolist():
        # 处理数据，封装成列表形式以返回
        df_list.append(res_dict_template.copy())
        df_list[-1]["data"] = []
        df_list[-1]["kpi_name"] = index_name_trans(i)

        # 每一组以新的df形式放入列表中
        new_df = pd.DataFrame({index_name: time_series, index_name_trans(str(i)): df[i].values.tolist()})
        new_df.rename(columns={"_time": "timestamp"}, inplace=True)
        new_df.set_index(["timestamp"])

        df_list[-1]["data"].append(new_df)
        # print(df_list[-1]["data"][0])
        df_list[-1]["data"][0] = df_list[-1]["data"][0].to_json(orient="records")
        df_list[-1]["data"][0] = json.loads(df_list[-1]["data"][0])

        df_list[-1]["data"] = df_list[-1]["data"][0][0:-1]
        df_list[-1]["original_name"] = i
    return df_list


# 根据质心数据表寻找对应的时间序列数据

# 若调用链无异常，黄金指标数据异常，则利用质心数据寻找新的数据进行检测以寻找异常实体
def centroid_find_abnormal(current_time):
    # 处理查询起始时间以使用influx接口
    start_time = int(current_time) - int(window_length) - 1

    # 需要多取10分钟数据
    end_time = int(current_time) + 600 + 1

    # data 字典模板
    res_dict_template = {
        "kpi_name": "",
    }

    data_list = []

    with open("result2.csv", "r") as f:
        reader = csv.reader(f)
        # print(type(reader))
        n = 1
        for row in reader:
            if n == 1:
                n += 1
                continue

            data_list.append(res_dict_template.copy())

            data_list[-1]["data"] = []
            data_list[-1]["kpi_name"] = row[1]

            series = influx_api.query_metric2('business-kpi', row[0], row[1], start_time, end_time)
            # print("series",type(series),series)
            if not isinstance(series, pd.DataFrame):
                df = series.to_frame().reset_index()
            else:
                continue
            df.rename(columns={"_time": "timestamp", "_value": index_name_trans(str(row[0]))}, inplace=True)
            df.set_index(["timestamp"])
            # print(df)

            data_list[-1]["data"].append(df)
            data_list[-1]["kpi_name"] = index_name_trans(row[0])

            data_list[-1]["data"][0] = data_list[-1]["data"][0].to_json(orient="records")
            data_list[-1]["data"][0] = json.loads(data_list[-1]["data"][0])

            data_list[-1]["data"] = data_list[-1]["data"][0][0:-1]

        # 返回根据质心数据找到的时间序列数据
        return arima_test_centroid(data_list)


# arima检测


# 使用取得的黄金指标数据进行arima异常检测


# arima接口使用黄金指标数据进行检测
def arima_test_golden(data):
    for i in data:

        print("黄金指标数据调用arima接口")

        # 调用arima接口，指定数据格式
        result = requests.get(myurl, data=json.dumps(i), headers={'content-type': "application/json"})
        print(result.text)
        value_golden = []
        if result.text[0] == "<":
            continue
        response = eval(result.text)["data"]["res"]  # 检测的结果

        df1 = pd.DataFrame.from_dict(i["data"]).dropna()
        # print(df1)
        # 对于每一行，通过列名name访问对应的元素
        for row in df1.iterrows():
            print(row)
            value_golden.append(row[1][i["kpi_name"]])
        # 若response为TRUE则说明异常
        # 若response为FALSE则无异常

        # 黄金指标中只要出现结果为FALSE就说明有异常
        if response == false:
            return [i["kpi_name"], True], value_golden

    return ['', False], []


# 使用取得的调用链数据进行arima检测


# arima接口使用调用链数据进行检测
def arima_test_callchain(data):
    # 异常实体列表
    response_list = []
    for i in data:

        # 调用arima接口，指定数据格式
        print("调用链数据调用arima接口")
        result = requests.get(myurl, data=json.dumps(i), headers={'content-type': "application/json"})
        print(result.text)
        value_callchain = []
        if result.text[0] == "<":
            continue
        response = eval(result.text)["data"]["res"]  # 检测的结果
        # 若response为True则说明实体无异常
        # 若response为False则有异常

        df1 = pd.DataFrame.from_dict(i["data"]).dropna()
#             print(df1)
        # 对于每一行，通过列名name访问对应的元素
        for row in df1.iterrows():
            value_callchain.append(row[1][i["kpi_name"]])

        # 异常则将其加入异常实体列表
        if response == false:
            if i["kpi_name"] not in response_list:
                print(i["kpi_name"])
                response_list.append([i["kpi_name"], value_callchain])
#     print(response_list)
    return response_list


# 使用质心数据进行arima检测

# arima接口使用质心取出的数据进行检测
def arima_test_centroid(data):
    # 异常实体列表
    response_list = []
    for i in data:

        # 调用arima接口，指定数据格式
        print("质心数据调用arima接口")
        result = requests.get(myurl_performance, data=json.dumps(i), headers={'content-type': "application/json"})
        print(result.text)
        if result.text[0] == "<":
            continue
        response = eval(result.text)["data"]["res"]  # 检测的结果
        # 若response为True则说明实体无异常
        # 若response为False则有异常

        # 异常则将其加入异常实体列表
        if response == false:
            if i["kpi_name"] not in response_list:
                print(i["kpi_name"])
                response_list.append(i["kpi_name"])
    print(response_list)
    return response_list


# 使用性能指标数据进行arima检测


# arima接口调用性能指标数据进行检测
def arima_test_performance(data, current_time):

    abnormal_index_df = pd.DataFrame(columns=["timestamp", "index_name"])

    current_res_dict = {}

    for i in data:
        print('kpi_name:', i['kpi_name'])
        timestamp_list = []
        print("性能指标数据调用arima接口")

        result = requests.get(myurl_performance, data=json.dumps(i), headers={'content-type': "application/json"})

        if result.text[0] == "<":
            print(result.text)
            continue
        print(result.text)
        response = eval(result.text)["data"]["res"]  # 检测的结果
        # 若response为True则说明无异常
        # 若response为False则有异常
        if response == false:
            #             print(result.text)
            df1 = pd.DataFrame.from_dict(i["data"]).dropna()
#             print(df1)
            # 对于每一行，通过列名name访问对应的元素
            for row in df1.iterrows():
                timestamp_list.append(row[1][i["kpi_name"]])
#                 print(row[1])
                current_res_dict[i["original_name"]] = timestamp_list

#             print(current_res_df)

    return current_res_dict


# 调度器

# 设置调度器，定时调用以进行检测
interval = 1  # 调用的间隔时间 单位/s
# 在该函数执行完成后 才会再次进入重新执行

s = sched.scheduler(time.time, time.sleep)


def do_arima_test_2020(sc):
    global current_time
    # print(current_time)

    # 分别取同一时间段黄金指标数据和调用链数据进行检测

    # 取黄金指标数据
    data_golden = golden_index_data_2020(system_name, str(current_time), str(window_length))
#     print("golden_data 0",data_golden[0])
    # 取调用链指标数据
    data_callchain = call_chain_data_2020(str(current_time), str(window_length))
#     print("callchain_data 0",data_callchain[0])

    # 分别检测
    print("黄金指标数据检测")
    response, value_golden = arima_test_golden(data_golden)
    print("调用链数据检测")
    response_list = arima_test_callchain(data_callchain)

    # 根据检测结果分情况进行检测：

    # 1.若调用链数据出现异常，无论黄金指标是否异常，直接用找到的异常实体，寻找其对应的性能指标数据，再次进行arima检测
    if response_list:
        for item in response_list:
            cmdb_id = item[0]
            # 取异常指标性能指标数据
            data = find_span_performance_index(system_name, cmdb_id, current_time, window_length)

            cur_time_abnormal_dict = arima_test_performance(data, current_time)
            # 三个参数：异常指标时间序列，(调用链异常指标名+对应时间序列)，当前时间
            cur_time_abnormal_list = [cur_time_abnormal_dict, {cmdb_id: item[1]}, current_time]
            if cur_time_abnormal_dict:
                final_abnormal_index.append(cur_time_abnormal_list)

    # 2.若调用链数据检测无异常，但黄金指标出现异常，则进一步使用质心数据进行检测
    elif response[1] == True:
        response_list_centroid = centroid_find_abnormal(current_time)
        if response_list_centroid:
            for cmdb_id in response_list_centroid:
                data = find_span_performance_index(system_name, cmdb_id, current_time, window_length)
                cur_time_abnormal_dict = arima_test_performance(data, current_time)

                # 三个参数：异常指标时间序列，(黄金指标异常指标名+对应时间序列)，当前时间
                cur_time_abnormal_list = [cur_time_abnormal_dict, {response[0]:value_golden}, current_time]
                if cur_time_abnormal_dict:
                    final_abnormal_index.append(cur_time_abnormal_list)

    print(final_abnormal_index)
    final_dict = {}
    columns = []
    len_min = 9999
    for item in final_abnormal_index[0][:-1]:
        for key, value in item.items():
            final_dict[key] = value
            columns.append(key)
            if len(value) < len_min:
                len_min = len(value)

    final_df = pd.DataFrame(columns=columns)
    problem_node = columns[-1]
    for key, value in final_dict.items():
        if len(value) == len_min:
            # value_float_m = map(float, value)
            # value_float_lst = list(value_float_m)
            final_df[key] = value
        else:
            temp = []
            minus = len(value) // len_min
            residual = len(value) % len_min
            for i in range(1, len_min + 1):
                temp.append(float(value[i * minus + residual - 1]))
            final_df[key] = temp

    print("final_df", final_df)

    result = pcmci_and_walk(final_df, problem_node, use_granger=False)
    print(result)

    # print(eval(r.text)["data"]["res"])
    current_time = str(int(current_time) + 60)

    # 若需要持续调用该函数则取消注释即可
    #sc.enter(interval, 1, do_arima_test_2020, (sc,))


s.enter(1, 1, do_arima_test_2020, (s,))
# s.run()


if __name__ == "__main__":
    s.run()
