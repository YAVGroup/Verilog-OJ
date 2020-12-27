# Verilog-OJ

[![Github Actions Test Status](https://github.com/lluckydog/Verilog-OJ/workflows/Test/badge.svg)](https://github.com/lluckydog/Verilog-OJ/actions)
[![Build Status](https://travis-ci.org/lluckydog/Verilog-OJ.svg?branch=master)](https://travis-ci.org/lluckydog/Verilog-OJ)
[![Coverage Status](https://coveralls.io/repos/github/lluckydog/Verilog-OJ/badge.svg?branch=master)](https://coveralls.io/github/lluckydog/Verilog-OJ?branch=master)

Verilog OJ 是面向数字电路学习和实践的在线评测平台。

## 开发环境部署指南

下文以 Ubuntu 20.04.1 LTS 为例进行说明。

需要的依赖：
- Python 3
  - ~~请注意，PyPI 上目前没有 Python 3.8 预编译的 Pandas 软件包，您可能需要安装 Cython, g++ 等再进行 pip install 操作，否则可能出现错误。~~ (Bumped Pandas to 1.1.4)
- NodeJS & NPM (需要选择支持 package-lock.json 功能的 NPM 版本，过旧的版本请不要使用)
- RabbitMQ 消息中间件
  - 此项用于后端向判题服务传递消息，是 Celery 的依赖
  - 请用 apt 安装并部署

> 目前判题脚本中 pyDigitalWaveTools 的版本还没有迁移，请参考 [Judger 中的说明](judger/test/README.md) 部署 libreliu 魔改的 pyDigitalWaveTools 版本。

大致过程：
```bash
# Update repo to latest
sudo apt update && sudo apt upgrade

# Install essential software
sudo apt install build-essential rabbitmq-server yosys nodejs npm python3-virtualenv 
sudo systemctl start rabbitmq-server

git clone https://github.com/lluckydog/Verilog-OJ
cd Verilog-OJ
virtualenv venv
. venv/bin/activate
pip install -r requirements.txt

cd frontend
# 建议先把 npm 源切换为淘宝源，此处略
npm install .

cd ../backend

# 设置一些必须的环境变量
# *Must READ*
# 如果不用 Docker 判题环境，就需要将 backend/settings/dev.py 中的 'use_docker' 修改正确
# 否则会报缺少一些 Docker 相关的环境变量

VERILOG_OJ_DEV=TRUE python manage.py migrate

# 此处创建您测试环境的超级用户的用户名和密码
VERILOG_OJ_DEV=TRUE python manage.py createsuperuser
```

这样就基本部署完成了。

### 运行前端

```bash
cd frontend
npm run serve
```

### 运行后端

```bash
cd backend
VERILOG_OJ_DEV=TRUE python manage.py runserver
```

### 运行判题服务器

```bash
cd backend
# Make sure your rabbitmq have started.
# If not, use systemctl start rabbitmq-server
# (use systemctl enable to start on system boot)
VERILOG_OJ_DEV=TRUE celery -A judge worker -l INFO
```

## 生产环境部署指南

> 针对 Git commit 00ee2a51，内容可能有落后之处。

1. 首先确保有 Docker（`sudo apt install docker.io`），然后换国内源，最后启动 daemon（`sudo systemctl start docker`）
2. 生产环境相关的值都统一维护在 `.env` 中了，按需编辑
3. 将 `judger-env` 镜像打包好
   > 可以进 `./deploy` 然后 `docker build -f Dockerfile.judger-env --build-arg USE_APT_MIRROR=yes --build-arg USE_PIP_MIRROR=yes`
4. `docker-compose up`
5. 第一次的时候，记得手动进 backend 容器，进行一下 `python manage.py migrate` 和 `python manage.py createsuperuser` 的操作，详情参考上面开发环境的指南

### 数据备份和回复

TBD

### 负载均衡

目前还没啥需求，一台机器而且用户量最高也不会超过几百的小打小闹就不上 swarm 或者 k8s 这种容器编排系统了。
