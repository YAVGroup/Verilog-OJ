# Verilog OJ Architecture

设计架构如下：

```
                         VLab Reverse Proxy

                               ^
                               |
                    EXPOSE 80  |
                               |
                               |
                         +-----+----------+
                         |    nginx       |
                         +-----+----------+
                               |
                               |                   +----------------------+
                               |                   | Usercode in one-time |
+-----------------+      +-----+----------+        | container            |
|      MySQL      +------+    Django      |        |           no network |
+-----------------+      +-----+----------+        +---------+------------+
                               |                             |
                               |                             | connect via bind mount
                               |                             |
                         +-----+----------+          +-------+---------+
                         |   RabbitMQ     +----------+  Judger Worker  |
                         +----------------+          +-----------------+

```

其中每个实线框均为一个 Docker container。

## Nginx Container

采用 `nginx:stable-alpine` 镜像。

从 `docker container exec 77c sh -c "cat /etc/nginx/nginx.conf"` 容易得到，唯一的站点配置位于 `/etc/nginx/conf.d/default.conf`，则将自定义的站点文件放置于此即可。


### Helpful commands
- 手工构建：`cd frontend && docker build . -f Dockerfile.nginx --build-arg DELETE_NPM_LOCK=no --build-arg USE_NPM_MIRROR=yes -t front:v1`
- 启动：`docker run --rm -it --network=host front:v1`
