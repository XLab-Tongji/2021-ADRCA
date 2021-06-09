
from flask import Flask, jsonify, request
import json
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.graphics.tsaplots import plot_pacf
from statsmodels.tsa.stattools import adfuller as ADF
from statsmodels.tsa.statespace.sarimax import SARIMAX 
import statsmodels.api as sm
import numpy as np
from statsmodels.tsa.arima_model import ARIMA
from pmdarima import auto_arima 
from pandas.io.json import json_normalize
import os
from pathlib import Path
from sklearn.preprocessing import MinMaxScaler
import csv
import pymysql


app = Flask(__name__)     #创建一个wsgi应用
def read_kpi_list():
    #input_files=r"C:\Users\syj\Documents\Jupyter\read_data/kpi_list.csv"
    input_files=r"/arima/data/kpi_list.csv"
    path = Path(input_files)
    csv_files = list(path.parents[0].glob(path.name))
    fieldnames = ["kpi_name", "algorithm"]
    print(csv_files)
    kpi_list=dict()
    for file in csv_files:  
        print(file.name)
        with open(file) as rf:
            reader = csv.DictReader(rf,fieldnames=fieldnames)
            for row in reader:
    #             print(row['algorithm'])
                kpi_list[row['kpi_name']]=row['algorithm']
                
    print(kpi_list)
    return kpi_list

def get_residual(ts,dta_pred,kpi_name): #计算arima得到的残差
    residual=ts.copy()
    residual['pred']=dta_pred
    residual['residual']=residual[kpi_name]-residual['pred']
    #print(test)
    #pred1.drop('date', axis = 1, inplace = True)
    residual.drop(kpi_name,axis=1,inplace=True)
    residual.drop('pred',axis=1,inplace=True)

    return residual
   
def three_sigma(ts,test_residual):
    n = 3
    data=ts.copy()
    data_y = data['residual']
    data_x = data.index
    ymean = np.mean(data_y)
    ystd = np.std(data_y)
    threshold1 = ymean - n * ystd
    threshold2 = ymean + n * ystd
    if (test_residual[0] < threshold1)|(test_residual[0] > threshold2):
                return False
    else:
                return True


def global_three_sigma_algorithm(kpi_name,ts):
    n=3
    origin_data=ts.copy()
    data=ts.copy().dropna()
    origin_data_y=origin_data[kpi_name]
    data_y = data[kpi_name]
    data_x = data.index
    ymean = np.mean(data_y)
    ystd = np.std(data_y)
    threshold1 = ymean - n * ystd
    threshold2 = ymean + n * ystd
    outlier = [] #将异常值保存
    outlier_x = []
    for i in range(len(data_y)-20, len(data_y)):
        if (origin_data_y[i] < threshold1)|(origin_data_y[i] > threshold2):
            outlier.append(origin_data_y[i])
            outlier_x.append(origin_data_y[i])
            return False
        else:
            continue
    return True


def global_arima_three_sigma_algorithm(kpi_name,ts,origin_data):
    n=3
    data=ts.copy()
    print(data)
    data_y = data['residual']
    data_x = data.index
    print(data_y)
    origin_data_y=origin_data[kpi_name]
    
    ymean = np.mean(data_y)
    ystd = np.std(data_y)
    threshold1 = ymean - n * ystd
    threshold2 = ymean + n * ystd
    outlier = [] #将异常值保存
    outlier_x = []
    print(origin_data_y)
    for i in range(len(origin_data_y)-20, len(origin_data_y)):
        if (origin_data_y[i] < threshold1)|(origin_data_y[i] > threshold2):
            outlier.append(origin_data_y[i])
            outlier_x.append(origin_data_y[i])
            return False
        else:
            continue
    return True
    # print('\n异常数据如下：\n')
    # print(outlier)
    # print(outlier_x)
    # fig4 = plt.figure(figsize=(24,16))
    # plt.plot(data_x, data_y)
    # plt.plot(outlier_x, outlier, 'ro')
    # for j in range(len(outlier)):
    #     plt.annotate(outlier[j], xy=(outlier_x[j], outlier[j]), xytext=(outlier_x[j],outlier[j]))


    # # plt.savefig('d:/picture//result/'+string+'.jpg')
    # plt.show()

def three_sigma_algorithm(kpi_name,kpi_value,ts):
    n=3
    data=ts.copy()
    data_y = data[kpi_name]
    data_x = data.index
    ymean = np.mean(data_y)
    ystd = np.std(data_y)
    threshold1 = ymean - n * ystd
    threshold2 = ymean + n * ystd
    if (kpi_value<threshold1)|(kpi_value>threshold2):
        return False
    else:
        return True

def autoarima(kpi_name,kpi_value,ts,isSeasonal): #arima算法
    print(ts)
    #ts.index=pd.to_datetime(ts.index)
    if (isSeasonal==0): #非季节性arima
        model = auto_arima(ts.dropna(), start_p=0, start_q=0, max_p=6, max_q=6, max_d=2,
                       seasonal=False, test='adf',
                       error_action='ignore',
                       information_criterion='aic',
                       njob=-1, trace=True, suppress_warnings=True)
        param=model.get_params(deep=True)
        order=param.get('order')
        arima = ARIMA(ts.dropna(), order).fit()
        
    else: #季节性arima
        model = auto_arima(ts.dropna(), start_p=0, start_q=0, max_p=6, max_q=6, max_d=2,
                       seasonal=True, test='adf',
                       error_action='ignore',
                       information_criterion='aic',
                       njob=-1, trace=True, suppress_warnings=True)
        param=model.get_params(deep=True)
        order=param.get('order')
        s_order=param.get('seasonal_order')
        arima= SARIMAX(ts.dropna(),order = order,seasonal_order =s_order).fit()

    dta_pred = arima.predict(typ = 'levels',dynamic=False)
    residual=get_residual(ts,dta_pred,kpi_name)
   
    residual=residual.dropna()
    print(residual)
    test_pred=arima.predict(len(ts),len(ts),typ = 'levels',dynamic=False)
    test_residual=kpi_value-test_pred.values
    #print(three_sigma(residual,test_residual))
    return three_sigma(residual,test_residual)  #判断输入值在不在3—sigma的范围内


def global_autoarima(kpi_name,ts,isSeasonal): #全局arima算法
    print(ts)
    origin_data=ts.copy()
    ts=ts.dropna()
    #ts.index=pd.to_datetime(ts.index)
    if (isSeasonal==0): #非季节性arima
        model = auto_arima(ts.dropna(), start_p=0, start_q=0, max_p=6, max_q=6, max_d=2,
                       seasonal=False, test='adf',
                       error_action='ignore',
                       information_criterion='aic',
                       njob=-1, trace=True, suppress_warnings=True)
        param=model.get_params(deep=True)
        order=param.get('order')
        arima = ARIMA(ts.dropna(), order).fit()
        
    else: #季节性arima
        model = auto_arima(ts.dropna(), start_p=0, start_q=0, max_p=6, max_q=6, max_d=2,
                       seasonal=True, test='adf',
                       error_action='ignore',
                       information_criterion='aic',
                       njob=-1, trace=True, suppress_warnings=True)
        param=model.get_params(deep=True)
        order=param.get('order')
        s_order=param.get('seasonal_order')
        arima= SARIMAX(ts.dropna(),order = order,seasonal_order =s_order).fit()

    dta_pred = arima.predict(typ = 'levels',dynamic=False)
    residual=get_residual(ts,dta_pred,kpi_name)
   
    residual=residual.dropna()
    print(residual)
    # test_pred=arima.predict(len(ts),len(ts),typ = 'levels',dynamic=False)
    # test_residual=kpi_value-test_pred.values
    #print(three_sigma(residual,test_residual))
    return global_arima_three_sigma_algorithm(kpi_name,residual,origin_data)
    #return three_sigma(residual,test_residual)  #判断输入值在不在3—sigma的范围内


def threshold(kpi_value,threshold_value1,threshold_value2):  #3—sigma算法
    if (kpi_value<threshold_value1)|(kpi_value>threshold_value2):
        return False
    else:
        return True
    

@app.route('/arima',methods=['GET'])
def get_arima():

    kpi_type=read_kpi_list()
    get_args = request.get_json()
    kpi_name=get_args.get('kpi_name')
    origin_data =get_args.get('data')
    kpi_value=get_args.get('kpi_value')
    print(type(kpi_value))
    kpi_value=float(kpi_value)
    #print(type(t1))
    algorithm=get_args.get('is_Seasonal')
   # print(get_args)
    data=pd.read_json(json.dumps(origin_data),encoding="utf-8", orient='records')
   # print(data)
   #预处理数据
    data['date'] = pd.to_datetime(data['timestamp'], unit='s')
    data = data.set_index(data.date)
    data.drop('date', axis = 1, inplace = True)
    data.drop('timestamp', axis = 1, inplace = True)
    data.index=pd.to_datetime(data.index)
    da=data[kpi_name]
    da=da.to_list()
    
    dta=np.array(da,dtype=np.float) 
    data[kpi_name]=dta
   # print(data)
    if kpi_type[kpi_name]=='arima': #使用arima算法
        res=autoarima(kpi_name,kpi_value,data,0)   #The return type must be a string, tuple  #jsonify(data)
    if kpi_type[kpi_name]=='stationary':  #使用3-sigma算法
        res=three_sigma_algorithm(kpi_name,kpi_value,data.dropna( ))
    if kpi_type[kpi_name]=='sarima': #使用sarima
        res=autoarima(kpi_name,kpi_value,data,1)
    if kpi_type[kpi_name]=='abnormal': #异常数据 不处理
        res=True
 #   return 'hello AIOps'  
    return jsonify(data={"res":res})
#     return jsonify(data={"res":res})


@app.route('/global_arima',methods=['GET'])
def global_arima():

    kpi_type=read_kpi_list()
    get_args = request.get_json()
    kpi_name=get_args.get('kpi_name')
    origin_data =get_args.get('data')
    #print(type(t1))
   # print(get_args)
    data=pd.read_json(json.dumps(origin_data),encoding="utf-8", orient='records')
   # print(data)
   #预处理数据
    data['date'] = pd.to_datetime(data['timestamp'], unit='s')
    data = data.set_index(data.date)
    data.drop('date', axis = 1, inplace = True)
    data.drop('timestamp', axis = 1, inplace = True)
    data.index=pd.to_datetime(data.index)
    da=data[kpi_name]
    da=da.to_list()
    
    dta=np.array(da,dtype=np.float) 
    data[kpi_name]=dta
   # print(data)
    if kpi_type[kpi_name]=='arima': #使用arima算法
        res=global_autoarima(kpi_name,data,0)   #The return type must be a string, tuple  #jsonify(data)
    if kpi_type[kpi_name]=='stationary':  #使用3-sigma算法
        res=global_three_sigma_algorithm(kpi_name,data)
    if kpi_type[kpi_name]=='sarima': #使用sarima
        res=global_autoarima(kpi_name,data,1)
    if kpi_type[kpi_name]=='abnormal': #异常数据 不处理
        res=True
 #   return 'hello AIOps'  
    return jsonify(data={"res":res})
#     return jsonify(data={"res":res})



@app.route('/test',methods=['GET'])
def get_test():
    #print(request.get_json())
    get_args=request.get_json()
    origin_data =get_args.get('data')
    kpi_value=get_args.get('kpi_value')
    
    is_Seasonal=get_args.get('is_Seasonal')
    #print(origin_data)
    c=pd.read_json(json.dumps(origin_data),encoding="utf-8", orient='records')
    print(c)
    return jsonify({'res':is_Seasonal})   


@app.route('/kpi_list',methods=['GET'])
def get_kpi_list():
    #print(request.get_json())
    
    return read_kpi_list()



@app.route('/login',methods=['POST'])
def login():
    get_args=request.get_json()
    username =get_args.get('username')
    password=get_args.get('password')
    db = pymysql.Connect(host='10.60.38.173',port=3307,user='root',passwd='arima',db='arima')
    cursor = db.cursor()
    sql = """ select USERNAME,PASSWORD from USER where USERNAME='%s' """ % (username)
    cursor.execute(sql)
    results = cursor.fetchone()
    if results:
        if (results[1]!=password):
            message="0"
        else:
            message="1"
    else:
        message="-1"
    db.close()
    return jsonify({'res':message})   

@app.route('/registry',methods=['POST'])
def registry():
    get_args=request.get_json()
    username =get_args.get('username')
    password=get_args.get('password')
    db = pymysql.Connect(host='10.60.38.173',port=3307,user='root',passwd='arima',db='arima')
    cursor = db.cursor()
    sql = """ select USERNAME from USER where USERNAME='%s' """ % (username)
    cursor.execute(sql)
    db.commit()
    
    results = cursor.fetchone()
    if results:
        message="0"
    else:
        sql_insert = """insert into USER values('%s','%s')"""%(username,password)
        try:
            cursor.execute(sql_insert)
            db.commit()
            message="1"
        except:
            db.rollback()
            message="-1"
         
    db.close()
    return jsonify({'res':message})   


@app.route('/')           #添加路由：根
def hello_world():
    return 'hello AIOps' #输出一个字符串

# @app.route('/a')           #添加路由：根
# def hello_world2():
#     return 'Hello' #输出一个字符串

# Flask应用程序实例的run方法启动WEB服务�?
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5001)  # 127.0.0.1 #指的是本地ip
    #app.run(host='0.0.0.0', port=12581, debug=True)
   #c=autoarima(45,data,0)
