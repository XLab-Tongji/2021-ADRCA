## 根因分析服务

### 整体逻辑

```python
# ./docker/utils.py
# 入口： pcmci_and_walk 函数
```

1. 预处理 - `patch_constant_kpi`
2. PCMCI
3. 构建图 - 使用`networkx`
4. 画图 - 使用`matplotlib`
5. 计算概率转移矩阵 - `probablity_matrix`
6. 进行随机游走 - `random_walk`

### docker部署步骤：

`docker` 目录下为根因分析服务源代码与docker部署配置文件

```bash
# 构建docker镜像
cd ./docker
docker build -t root_cause_analysis .

# 启动docker容器
docker run -it --rm -p 80:8080 --name root_cause_analysis root_cause_analysis
```

### python接口

`client.py` 为docker部署后，调用被部署服务的`python`代码 (套娃？)

在自己的代码中 import 之后即可调用

```python
import pcmci_and_walk from client

res = pcmci_and_walk(...)
```