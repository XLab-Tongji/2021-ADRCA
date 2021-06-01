import tqdm
import pandas as pd
from multiprocessing import Pool
from datetime import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# You can generate a Token from the "Tokens Tab" in the UI
token = "B8VrjXVlgsrdWrrJces6_uokTo75AxLTDMIeyROfaks2FIjTJpdqYlbrOUtcktG0zfYiv2T8AoJlJ23GrfwtKA=="
org = "Tongji"

client = InfluxDBClient(url="http://10.60.38.173:18086", token=token)

write_api = client.write_api(write_options=SYNCHRONOUS)


def push(file, i, system):
    data = pd.read_csv(file)
    batch_size = 5000
    size = len(data)
    for batch_start in tqdm.trange(0,
                                   size,
                                   batch_size,
                                   desc=f'Write {file[-10:]}',
                                   position=i):

        seq = [
            Point('point')\
            .tag('system',system)\
            .tag('tc', str(row['tc']))\
            .field('rr',int(row['rr']))\
            .field('sr',int(row['sr']))\
            .field('count',int(row['cnt']))\
            .field('mrt',int(row['mrt']))\
            .time(int(row['timestamp']), WritePrecision.S)
            for row in data.iloc[batch_start:batch_start+batch_size].iloc
        ]
        write_api.write("new_kpi", org, seq)


if __name__ == '__main__':
    p = Pool(8)
    for i, [system, file] in enumerate([
        #  ['system-a', 'data/system-a/0226/metric/kpi_0226.csv'],
        #  ['system-a', 'data/system-a/0227/metric/kpi_0227.csv'],
        #  ['system-a', 'data/system-a/0228/metric/kpi_0228.csv'],
        #  ['system-a', 'data/system-a/0301/metric/kpi_0301.csv'],
         ['system-b', 'data/system-b/0303/metric/kpi_0303.csv'],
         ['system-b', 'data/system-b/0304/metric/kpi_0304.csv']]):
        p.apply_async(push, args=(file, i, system))
    print('Waiting for all subprocesses done...')
    p.close()
    p.join()
    print('All subprocesses done.')
