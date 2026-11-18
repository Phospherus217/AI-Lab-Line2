# conda
## 一、上手说明
   1. 安装miniconda
   2. 配置conda清华源和pip清华源
   ![pnHxpUs.png](https://s41.ax1x.com/2026/11/18/pnHxpUs.png)
   [![pnHxMP1.png](https://s41.ax1x.com/2026/11/18/pnHxMP1.png)](https://imgchr.com/i/pnHxMP1)
   3. 创建指定python的独立环境
   * conda create -n py310=3.10
   4. 激活虚拟环境并验证
  * conda activate py310
  * python --version
  * conda env list
   ![pnHxPCq.png](https://s41.ax1x.com/2026/11/18/pnHxPCq.png)
   ![pnHxi80.png](https://s41.ax1x.com/2026/11/18/pnHxi80.png)
   5. 掌握依赖导出与复现
   * pip freeze > requirements.txt
   * cat requirements.txt
   * pip install -r requirements.txt
   ![pnHx8KO.png](https://s41.ax1x.com/2026/11/18/pnHx8KO.png)
   ![pnHxJqe.png](https://s41.ax1x.com/2026/11/18/pnHxJqe.png)

## 二、踩坑点
1. **requirements.txt 文件名拼写错误**
 
* **报错现象**
 
  执行命令提示： No such file or directory: requirement.txt 
* **问题原因**
 
   手动输入命令时少写字母 s，错误使用  requirement.txt ，正确文件名必须带复数后缀。
 
 
* **解决方法**
     使用正确命令：pip install -r requirements.txt

2. **PowerShell 禁止运行脚本，导致 conda activate 报错**
   * **报错现象**
    在 PowerShell 中输入 conda activate 环境名 时，提示红字错误：无法加载文件 ...\conda.ps1，因为在此系统上禁止运行脚本。
   * **问题原因**
     Windows 默认的安全策略限制了 PowerShell 脚本的执行。
    * **解决方法**：
    1. 以管理员身份打开 PowerShell。
    2. 输入命令：Set-ExecutionPolicy RemoteSigned。
    3. 输入 Y 确认，然后重启 VS Code 终端即可。   