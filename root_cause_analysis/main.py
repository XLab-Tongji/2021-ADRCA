from utils import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# entities = load_entities("C:/dev/lab/data/metric_0226_for_cluster/*.csv")

# # for entity_name, entity in filt_entities.items():
# entity_name = 'gjjcore4'
# entity = entities[entity_name]

# print('Entity name:', entity_name)

# filt_entity = {
#     kpi_name: kpi
#     for kpi_name, kpi in entity.items()
#     if len(kpi) == 288
# }

# if len(filt_entity.keys()) == 0:
#     print('No data')
# continue
# entity_name = 'os_021'
# entity = query_all_metric2('', entity_name, 0, 90000000000)
# filt_entities, removed = filter_constant_kpi({entity_name: entity}, threshold=0.003)
# filt_entity = filt_entities[entity_name]

# df = pd.concat(filt_entity.values(), axis=1, keys=filt_entity.keys())
df = pd.read_csv('C:/Users/FrezC/Documents/WeChat Files/wxid_pk8pcwfydsqv22/FileStorage/File/2021-06/final_df.csv', index_col=0)
print("%d Obs x %d Vars" % (df.shape))

problem_node = 'os_021'  # random.choice(df.columns)
print('Assumed problem node:', problem_node)
result = pcmci_and_walk(
    df, problem_node, use_granger=True,
    p_threshold=0.05,
    graphargs={'figsize': (30, 20), 'dpi': 90}
)
print(result)
# result = pcmci_and_walk(df, problem_node, use_granger=False)
# print(result)

print()
