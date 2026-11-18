# Docker
## 一、上手说明
1.1**环境**
* 环境：Centos7虚拟机，Finalshell(SSH远程连接)
* Docker版本：26.1.4
* 镜像：python：3.10-slim

1.2**步骤**
1. 安装与与启动Docker
* yum install -y yum-utils
* yum-config-manager --add-repo https://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
* yum install -y docker-ce docker-ce-cli containerd.io
* cat > /etc/docker/daemon.json <<EOF
{
  "registry-mirrors": ["https://docker.mirrors.ustc.edu.cn"]
}
EOF
* systemctl start docker
* systemctl enable docker
![pnbSehR.png](https://s41.ax1x.com/2026/11/18/pnbSehR.png)
2. 进入root
   * su -
3. 拉取镜像
   * docker pull python:3.10-slim
   * docker images
   ![](https://i.imgs.ovh/2026/11/18/e86363c841ea10e4dc5a26777d374d04.png)
4. 挂载目录方式运行容器
   * docker run -it --rm -v $(pwd):/app -w /app python:3.10-slim python -c "print('Hello AI-Lab Docker')"
   * ![](https://i.imgs.ovh/2026/11/18/3c3cd60de89cefcf49bbd0ea0cb16e9d.png)
  
5. 编写Dockerfile构建自定义镜像
   * vim hello
   * FROM python:3.10-slim
    WORKDIR /app
    COPY hello.py.                  
    CMD ["python", "hello"]       
   * ls
  ![](https://i.imgs.ovh/2026/11/18/4a0583366880c7e8fee8ba17c4a27d97.png)
6. 构建镜像
   * docker build -t my-python-app .
   ![](https://i.imgs.ovh/2026/11/18/a8c69d4a64427b55bb7c4c3931c3e6b0.png)
7. 运行容器
   * docker run --rm my-python-app
  ![](https://i.imgs.ovh/2026/11/18/35211cdd460cc9c98c6d4d1a7cb8f24f.png)


## 二、踩坑
1. 问题：docker pull 拉取镜像超时  context deadline exceeded 
 
- 现象：执行  docker pull python:3.10-slim ，长时间卡住，最后报超时。
- 原因：默认源是 docker.io 国外地址，国内网络访问很慢；一开始用的中科大镜像源不稳定。
- 解决：更换国内轩辕镜像加速器，修改  /etc/docker/daemon.json ，然后  daemon-reload  + 重启docker。
  ![](https://i.imgs.ovh/2026/11/18/d3102af270c5183fadf3063fec4d5081.png)
2. 问题：分不清镜像和容器，命令混用
- 现象：想用  docker run  后面写镜像ID，结果输成容器ID；或者用  docker rm  删除镜像（报错）
- 区分：docker images  → 查看镜像，删镜像： docker rmi 镜像ID 
     docker ps -a  → 查看容器，删容器： docker rm 容器ID 