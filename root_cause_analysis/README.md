docker部署步骤：

```shell
# 构建docker镜像
cd ./docker
docker build -t root_cause_analysis .

# 启动docker容器
docker run -it --rm -p 80:8080 --name root_cause_analysis root_cause_analysis

# 测试接口
cd ..
python test.py
```

client.py封装了调用服务的代码