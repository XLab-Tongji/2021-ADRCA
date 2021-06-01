import tqdm
import pandas as pd
from multiprocessing import Pool
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# You can generate a Token from the "Tokens Tab" in the UI
token = "B8VrjXVlgsrdWrrJces6_uokTo75AxLTDMIeyROfaks2FIjTJpdqYlbrOUtcktG0zfYiv2T8AoJlJ23GrfwtKA=="
org = "Tongji"

client = InfluxDBClient(url="http://10.60.38.173:18086", token=token)

write_api = client.write_api(write_options=SYNCHRONOUS)


def push(file, i, system):
    metrics = pd.read_csv(file)
    batch_size = 5000
    size = len(metrics)
    for batch_start in tqdm.trange(0,
                                   size,
                                   batch_size,
                                   desc=f'Write {file[-10:]}',
                                   position=i):

        seq = [
            Point(row['kpi_name'])
            .tag('entity', row['cmdb_id'])
            .tag('system', system)
            .field('value', row['value'])
            .time(int(row['timestamp']), WritePrecision.S)
            for row in metrics.iloc[batch_start:batch_start+batch_size].iloc
        ]
        write_api.write("new_metrics", org, seq)


if __name__ == '__main__':
    p = Pool(8)
    for i, (system, file) in enumerate(
        [('system-a', 'data/system-a/0226/metric/metric_0226.csv'),
         ('system-a', 'data/system-a/0227/metric/metric_0227.csv'),
         ('system-a', 'data/system-a/0228/metric/metric_0228.csv'),
         ('system-a', 'data/system-a/0301/metric/metric_0301.csv'),
         ('system-b', 'data/system-b/0303/metric/metric_0303.csv'),
         ('system-b', 'data/system-b/0304/metric/metric_0304.csv')]):
        p.apply_async(push, args=(file, i, system))
    print('Waiting for all subprocesses done...')
    p.close()
    p.join()
    print('All subprocesses done.')
