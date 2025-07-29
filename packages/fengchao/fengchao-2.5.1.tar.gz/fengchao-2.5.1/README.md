该项目集成第三方大模型，本地开源大模型，知识库建设，指令设计，api消费统计，鉴权等功能。

支持的功能接口参见下表，部分接口需要进行鉴权使用，仅API需要单独鉴权（参考[【如何鉴权】](http://192.168.1.233:6053/fengchao/api)）。

支持通过SDK及API方式进行访问。推荐使用SDK方式进行访问，SDK已集成鉴权，解析等功能。

api_key及secret_key获取方式：[【安全中心】](http://192.168.1.233:6053/fengchao/get_secret)可以进行注册、查看api_key及secret_key，不同业务请注册属于自己的api_key及secret_key

### 环境配置

##### 线上环境

```shell
# 具体详见1panel配置文件
conda activate ijiwei-aigc
```

##### 测试环境

```shell
conda activate ijiwei_aigc
# 首次部署
supervisord -c /home/zhangpengfei/project/ijiwei-aigc/supervisor_test/conf/supervisor.conf
# 非首次部署,supervisor配置文件有更新时
supervisorctl -c /home/zhangpengfei/project/ijiwei-aigc/supervisor_test/conf/supervisor.conf update
```

### 支持功能
| 功能         | 是否鉴权 | 是否支持协程 |
|:-----------|:----:|:------:|
| 生成token    |  否   |   否    |
| 查看模型列表     |  否   |   否    |
| 查看prompt列表 |  否   |   否    |
| 查看知识库列表    |  否   |   否    |
| 对话服务：同步对话  |  是   |   是    |
| 对话服务：异步对话  |  是   |   是    |
| 对话服务：异步结果  |  是   |   是    |
| 对话服务：流式对话  |  是   |   是    |

### 支持的模型
```shell
curl --request GET --url 'http://192.168.1.233:6000/aigc/models/' | python -m json.tool --no-ensure-ascii
```
也可在[对话界面](http://192.168.1.233:6053/fengchao/chat)查看

### 支持的指令
```shell
curl --request GET --url 'http://192.168.1.233:6000/aigc/prompts/' | python -m json.tool --no-ensure-ascii
```
也可在[指令界面](http://192.168.1.233:6053/fengchao/prompts)查看

### 支持的知识库
```shell
curl --request GET --url 'http://192.168.1.233:6000/aigc/kgs/' | python -m json.tool --no-ensure-ascii
```
