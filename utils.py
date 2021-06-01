import csv
import os
from matplotlib.figure import Figure
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import networkx as nx
from sklearn.preprocessing import MinMaxScaler

import tigramite.data_processing as pp
from tigramite.independence_tests import ParCorr
from tigramite.pcmci import PCMCI

from random_walk import *


def pcmci_and_walk(dataframe: pd.DataFrame, problem_node: str, tau_max=5, *args, **kwarg):
    '''PCMCI & Random Walk'''
    n = len(dataframe.columns)
    column_names = dataframe.columns

    # PCMCI
    ppdf = pp.DataFrame(dataframe.values, var_names=dataframe.columns)
    pcmci = PCMCI(ppdf, cond_ind_test=ParCorr())
    pcmci_result = pcmci.run_pcmci(tau_max=tau_max, pc_alpha=None)

    # 构建图
    G = nx.DiGraph()

    _P = pcmci_result['p_matrix']
    _V = pcmci_result['val_matrix']
    np.nan_to_num(_P, copy=False, nan=1)
    rev_p_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            # pcmci的最大(1-p)值
            rev_p_matrix[i][j] = 1 - min([_P[i][j][tau] for tau in range(tau_max+1)])
            # 在P值小于0.05的边中，只保留val值最大的边
            edge = (0, 0, 0)
            for tau in range(tau_max + 1):
                if _P[i][j][tau] < 0.5:
                    val = _V[i][j][tau]
                    if val > edge[2]:
                        edge = (i, j, val)
            # 插入到图中
            G.add_edge(column_names[edge[0]], column_names[edge[1]], weight=edge[2])

    # 将每个指标的时间序列存到该节点的'timelist'数据域中
    for node_name in G.nodes:
        G.nodes[node_name]['timelist'] = dataframe[node_name]

    # 画图
    pos = nx.spring_layout(G)
    edge_labels = {(u, v): str(d['weight'])[:5] for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    nx.draw_networkx(G, pos, arrows=True, **{
        'node_color': 'red',
        'node_size': 400,
        'width': 2,
        'arrowstyle': '->',
        'arrowsize': 12,
    })
    plt.savefig('graph.png')

    # 计算概率转移矩阵
    P = probablity_matrix(G, problem_node, 0.5, rev_p_matrix=rev_p_matrix, *args, **kwarg)

    walk_result = random_walk(G, P, problem_node, 1000)
    return walk_result


def load_entities(input_files="data/metric_0226_for_cluster/*.csv"):
    '''加载数据集'''
    path = Path(input_files)
    csv_files = list(path.parents[0].glob(path.name))
    return {file.name[:-4]: read_ragged_csv(file, encoding="utf-8") for file in csv_files}


def read_ragged_csv(filename, **param_dict):
    '''逐行读取csv'''
    index = []
    data = []
    with open(filename, **param_dict) as f:
        f = csv.reader(f)
        for line in f:
            index.append(line[0])
            data.append(pd.Series(list(map(float, line[1:]))))
    return pd.Series(data, index)


def filter_constant_kpi(entities: dict, threshold=0.002):
    '''过滤近零方差的指标'''
    std = MinMaxScaler()
    res = {}
    removed = {}

    for entity_name, entity in entities.items():
        res1 = {}
        removed1 = []

        for kpi_name, kpi in entity.items():
            kpi_df = pd.DataFrame(kpi)
            kpi_df_scaled = std.fit_transform(kpi_df).reshape(-1)
            kpi_scaled = pd.Series(kpi_df_scaled)
            if kpi_scaled.var() < threshold:
                removed1.append(kpi_name)
                continue
            res1[kpi_name] = kpi

        if res1:
            res[entity_name] = res1
        removed[entity_name] = removed1
    return res, removed


def escape(arr, val):
    """把所有nan换成val"""
    newarr = arr
    newarr[np.isnan(arr)] = val
    return newarr


def pad(X, val=-1):
    '''将长度不一的X填充val到一致长度'''
    length = max(map(len, X))
    return np.array([
        np.pad(x, (0, length - len(x)), "constant",
               constant_values=val).tolist() for x in X
    ])


def truncate(arr, val):
    """把向量值为val的地方裁掉"""
    if np.isnan(val):
        return arr[~np.isnan(arr)]
    return arr[arr != val]


def normalization(data):
    """归一化"""
    _range = np.max(data) - np.min(data)
    if _range == 0:
        return data - np.min(data)
    return (data - np.min(data)) / _range


def standardization(data):
    """标准化"""
    mu = np.mean(data, axis=0)
    sigma = np.std(data, axis=0)
    return (data - mu) / sigma


def visualize_labels(entities: dict, output_dir: Path, norm=False):
    """画所有实体所有指标的图"""
    for name, entity in entities.items():
        output_dir1 = output_dir / name

        if not output_dir1.exists():
            output_dir1.mkdir()

        for label in entity.keys():
            fig, ax = plt.subplots(figsize=(18, 3))
            visualize_label(ax, entity[label], norm, label=label)
            ax.set_title(f"{name}-{label}")
            print(output_dir1 / f"{label}.png")
            fig.savefig(output_dir1 / f"{label}.png", dpi=300)
            plt.close(fig)


def visualize_label(ax, X, norm=False, **kwarg):
    """画一个指标的图"""
    if norm:
        X = normalization(X)
    ax.plot(X, **kwarg)


def visualize_cluster(entities: dict, label_dir: Path, output_dir: Path):
    """读取聚类，画图"""
    all_ids = {}
    for file in label_dir.glob("*"):
        all_ids[file.name] = np.fromfile(file, dtype=np.int64)  # 一维int64型数组

    for name, entity in entities.items():
        print("Entity name:", name)

        kpi_names = entity.keys()
        ids = all_ids[name]

        output_dir1 = output_dir / name
        os.makedirs(output_dir1, exist_ok=True)

        c_ids = set(ids)
        n_cluster = len(c_ids) - (-1 in c_ids)

        for c_id in c_ids:
            c_labels = [kpi_name for kpi_name, iid in zip(kpi_names, ids) if iid == c_id]
            c_size = len(c_labels)
            print(f"Cluster #{c_id}:", c_size)

            fig, ax = plt.subplots(figsize=(18, 3))
            for label in c_labels:
                visualize_label(ax, entity[label], label=label)
            # Add a title to the axes.
            ax.set_title(f"{name}-#{c_id}")
            ax.legend()
            # plt.show(fig)
            fig.savefig(output_dir1 / f"{c_id}.png",
                        dpi=300,
                        bbox_inches="tight",
                        pad_inches=0)
            plt.close(fig)
