import pandas as pd
from client import pcmci_and_walk

df = pd.read_csv('test_df.csv', index_col=0)
print("%d Obs x %d Vars" % (df.shape))

problem_node = 'os_021'  # random.choice(df.columns)
print('Problem node:', problem_node)


result = pcmci_and_walk(df, problem_node,
                        p_threshold=0.05,
                        graphargs={'figsize': (30, 20), 'dpi': 90})

print(result)
