# task01  （Windows PowerShell｜Trae + Aider + 智谱 GLM）

```
# Task01 AI编程环境与CLI Agent协同配置
> 组件选型：Trae IDE + Aider + 智谱GLM-4-Flash
操作系统：Windows11

## 1. 工具清单
- AI IDE：Trae
- CLI Agent：Aider v0.86.2
- API服务：智谱AI GLM
  - BaseURL：https://open.bigmodel.cn/api/paas/v4
  - 模型：openai/glm-4-flash（免费额度）

## 2. 配置流程
1. 注册智谱开放平台，获取sk密钥
2. 安装Trae，手机号登录
3. pip安装aider-chat
```powershell
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
pip install aider-chat
```

![image-20261025142443552](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20261025142443552.png)

![4b3e4e24d05710ba82c33ec8e9fe86b9](take01.assets/4b3e4e24d05710ba82c33ec8e9fe86b9.jpg)

```
# 设置智谱接口（仅当前终端生效，关闭窗口失效）
$env:OPENAI_API_BASE="https://open.bigmodel.cn/api/paas/v4/"
$env:OPENAI_API_KEY="替换成你的智谱sk密钥"

# 校验密钥是否加载成功（会打印密钥，截图务必打码！）
echo $env:OPENAI_API_KEY

# 进入项目文件夹，修改为你自己路径
cd E:\ai-lab take01

# 启动Aider（必须带 openai/ 前缀！！）
aider --model openai/glm-4-flash --no-show-model-warnings
```

![image-20261025222845524](take01.assets/image-20261025222845524.png)![image-20261025220029728](take01.assets/image-20261025220029728.png

![image-20261025220042934](take01.assets/image-20261025220042934.png)

![image-20261025220058210](take01.assets/image-20261025220058210.png)

![image-20261025221107231](take01.assets/image-20261025221107231.png)

## Aider 常用交互指令

```
# 新建/修改文件
帮我写快速排序，保存为sort.py，增加计时功能

# 修改已有文件
给sort.py增加详细注释，耗时保留6位小数

# 查看当前加载了哪些文件
/files

# 退出Aider
/exit

# 查看帮助
/help
```

## PowerShell 设置临时环境变量

```
$env:OPENAI_API_BASE="https://open.bigmodel.cn/api/paas/v4/"
$env:OPENAI_API_KEY="你的sk密钥"
```

## cd 进入项目目录，启动 Aider

```
aider --model openai/glm-4-flash --no-show-model-warnings
```

## 协同验证：Aider 修改 sort.py，Trae 自动感知外部文件变更

# 踩坑记录

1. 坑：模型直接写 glm-4-flash，报 LLM Provider NOT provided
   解决：模型名必须加前缀 openai/glm-4-flash
2. 坑：ConnectionResetError (10054，远程主机强迫关闭连接)
   解决：这个是启动探测报错，只要进入 > 提示符、能正常对话就不影响；关闭防火墙 / 安全软件拦截
3. 坑：setx 全局变量设置后 Aider 读不到 key
   解决：全局模式必须关闭所有终端窗口重新打开；使用会话临时变量，不用重启终端
4. 坑：密钥复制带有多余空格换行
   解决：复制密钥前后不要带空白字符，截图密钥必须打码，禁止完整上传 sk
