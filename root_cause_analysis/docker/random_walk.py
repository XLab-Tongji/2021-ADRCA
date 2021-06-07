from typing import Iterable
import networkx as nx
import numpy as np
import pandas as pd
import random
from pandas.core.frame import DataFrame
import pingouin as pg
from statsmodels.tsa.stattools import grangercausalitytests


def remove(li, x):
    li = list(li)
    if not isinstance(x, Iterable):
        x = tuple(x)
    for i in x:
        try:
            li.remove(i)
        except:
            pass
    return li


def curve_similarity(G: nx.DiGraph(), n1, n2):
    '''
    计算两曲线相似度
    G 根因定位图,每个节点具有一个属性字典 字典中有一个属性 键为timelist值为一个列表 记录曲线
    n1 n2 节点名称
    返回相似度
    '''
    n1_data = G.nodes[n1]['timelist']
    n2_data = G.nodes[n2]['timelist']

    if len(n1_data) != len(n2_data):
        print("length not match")
        return 0

    n = len(n1_data)
    sum_x = sum(n1_data)
    sum_y = sum(n2_data)
    sum_x2 = sum([x * x for x in n1_data])
    sum_y2 = sum([y * y for y in n2_data])
    sum_xy = sum([n1_data[i] * n2_data[i] for i in range(n)])
    if ((n * sum_x2 - sum_x ** 2) * (n * sum_y2 - sum_y ** 2)) == 0:
        val = 0
    else:
        val = (n * sum_xy - sum_x * sum_y) / ((n * sum_x2 - sum_x ** 2) * (n * sum_y2 - sum_y ** 2)) ** 0.5

    return abs(val)


def extract_timeseries_from_graph(G):
    dict_tmp = {}
    for i in G.nodes():
        dict_tmp[i] = G.nodes[i]['timelist']
    return pd.DataFrame(dict_tmp)


def partial_corr_c(G: nx.DiGraph,
                   n1, n2,
                   df: pd.DataFrame,
                   corr_type='pearson'):
    if n1 == n2:
        return 1

    if len(df[n2].unique()) == 1 or len(df[n1].unique()) == 1:
        return 0

    node_1_preds = remove(G.pred[n1], n1)
    node_2_preds = remove(G.pred[n2], n2)

    confounder = list(set(node_1_preds) | set(node_2_preds) - set((n1, n2)))

    for item in confounder:
        if len(df[item].unique()) == 1:
            confounder.remove(item)

    return abs(pg.partial_corr(data=df, x=n1, y=n2, covar=confounder, method=corr_type)['r'].values[0])


def granger_p_value(df: DataFrame):
    res = grangercausalitytests(df, 6, verbose=False)
    # 10种时延取最小
    # 取均值
    min_p_value = min([sum(map(lambda pir:pir[1], v[0].values()))/4 for v in res.values()])
    return min_p_value


def probablity_matrix(G: nx.DiGraph, problem_node: str,
                      r, rev_p_matrix, use_p_corr=False, remove_kpi=False,
                      use_granger=True, corr_type='pearson'):
    '''
    计算概率矩阵
    problem_node 前端节点
    G 根因定位图

    return
    P n*n大小 标准化的概率矩阵 由相似性度量仅有P[i][i.succ]非0
    '''
    n = len(G.nodes)
    df = extract_timeseries_from_graph(G)
    P = pd.DataFrame(np.zeros((n, n), dtype=np.float64), index=G.nodes(), columns=G.nodes())

    for i in G.nodes():
        i_succs: list = remove(G.succ[i], i)
        for i_succ in i_succs:
            # 缓存 granger p值 < 0.05 就偏相关系数翻倍
            if use_p_corr:
                P[i][i_succ] = r * partial_corr_c(G, i_succ, problem_node, df, corr_type)
            else:
                P[i][i_succ] = r * curve_similarity(G, i_succ, problem_node)

            if use_granger and granger_p_value(df[[i_succ, problem_node]]) < 0.05:
                P[i][i_succ] *= 2

        i_preds: list = remove(G.pred[i], i)
        if remove_kpi:
            i_preds = remove(G.pred[i], problem_node)
        for i_pred in i_preds:
            if use_p_corr:
                P[i][i_pred] = partial_corr_c(G, i_pred, problem_node, df, corr_type)
            else:
                P[i][i_pred] = curve_similarity(G, i_pred, problem_node)

            if use_granger and granger_p_value(df[[i_pred, problem_node]]) < 0.05:
                P[i][i_pred] *= 2

        if use_p_corr:
            c_self = partial_corr_c(G, i, problem_node, df, corr_type)
        else:
            c_self = curve_similarity(G, i, problem_node)

        if use_granger and granger_p_value(df[[i_pred, problem_node]]) < 0.05:
            c_self *= 2

        if c_self > P[i].max():
            P[i][i] = c_self - P[i].max()

        row_sum = P[i].sum()
        if row_sum:
            for other in set(i_preds + i_succs + [i]):
                P[i][other] /= row_sum
    for i in range(n):
        for j in range(n):
            node_i = list(G.nodes)[i]
            node_j = list(G.nodes)[j]
            P[node_i][node_j] *= rev_p_matrix[i][j]

    return P


def random_pick(some_list: list, probabilities: list):
    '''
    somelist 项列表
    probablities 概率列表
    return
    返回所选的项
    '''
    x = random.uniform(0, 1)
    cumulative_probability = 0.0
    for item, item_probability in zip(some_list, probabilities):
        cumulative_probability += item_probability
        if x < cumulative_probability:
            break
    return item


def random_walk(G: nx.DiGraph, P: pd.DataFrame, problem_node, num_loop):
    '''
    G nx.DiGraph() 根因定位图
    P pd.DataFrame n*n大小 标准化的概率矩阵 由相似性度量仅有 P[i][i.succ]非0
    problem_node 前端节点
    r   参数rou
    beta 参数beta
    num_loop 循环次数
    n  节点数
    m  边数
    v_s 当前节点
    v_p 前一个节点
    M pd.DataFrame n*n大小 转移矩阵
    R 字典 以节点名为键 出现次数为值
    return
    返回一个排序后的列表
    '''
    cur_node = problem_node
    reach_times = dict.fromkeys(G.nodes(), 0)

    for i in range(num_loop):
        cur_node = random_pick(P.index.tolist(), P[cur_node].values)
        reach_times[cur_node] += 1

    order = sorted(reach_times.items(), key=lambda x: x[1], reverse=True)
    return order
