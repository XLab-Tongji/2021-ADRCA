import requests
import pandas as pd
from base64 import b64decode


def pcmci_and_walk(df: pd.DataFrame, problem_node: str, tau_max=5,
                   p_threshold=0.05,
                   graphargs={'figsize': (15, 10), 'dpi': 300},
                   **kwarg):
    res = requests.post('http://127.0.0.1/pcmci_and_walk', json={
        'dataframe': df.to_json(),
        'problem_node': problem_node,
        'tau_max': tau_max,
        'p_threshold': p_threshold,
        'graphargs': graphargs,
        **kwarg
    })
    result = res.json()

    res = requests.get('http://127.0.0.1/get_image')
    img_data = b64decode(res.content)
    with open('graph.png', 'wb') as img:
        img.write(img_data)

    return result
