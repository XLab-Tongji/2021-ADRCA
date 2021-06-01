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

        seq_avg_time = [
            Point('point')
            .tag('system', system)
            .tag('cmdb_id', row['serviceName'])
            .field('avg_time', row['avg_time'])
            .field('num', row['num'].item())
            .field('succee_num', row['succee_num'].item())
            .field('succee_rate', row['succee_rate'])
            .time(int(row['startTime']), WritePrecision.MS)
            for row in metrics.iloc[batch_start:batch_start+batch_size].iloc
        ]
        write_api.write("kpi", org, seq_avg_time)


if __name__ == '__main__':
    p = Pool(8)
    for i, (system, file) in enumerate([
        # ('platform-kpi', 'data/平台指标/db_oracle_11g.csv'),
        # ('platform-kpi', 'data/平台指标/dcos_container.csv'),
        # ('platform-kpi', 'data/平台指标/dcos_docker.csv'),
        # ('platform-kpi', 'data/平台指标/mw_redis.csv'),
        # ('platform-kpi', 'data/平台指标/os_linux.csv')
        ('business-kpi', 'data/业务指标/esb.csv')
    ]):
        p.apply_async(push, args=(file, i, system))
    print('Waiting for all subprocesses done...')
    p.close()
    p.join()
    print('All subprocesses done.')
