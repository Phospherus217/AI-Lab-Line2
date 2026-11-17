# linux命令行
## 一、创建指定目录树
1. mkdir -p lab/logs lab/data lab/tmp
2. ls
3. cd lab
4. pwd
![pnHEmFS.png](https://s41.ax1x.com/2026/11/17/pnHEmFS.png)
* lab/
├── logs/
├── data/
└── tmp/
## 二、批量重命名文件
1. cd lab
2. touch logs/test{1..3}.txt
3. for i in {1..3};do mv "logs/test\${i}.txt" "logs/final${i}.txt";done
4. ls logs
  final1.txt  final2.txt  final3.txt
![pnHElyn.png](https://s41.ax1x.com/2026/11/17/pnHElyn.png)
lab/
├── logs/
│   ├── final1.txt
│   ├── final2.txt
│   └── final3.txt
├── data/
└── tmp/
## 三、过滤指定日志文件并输出为新文件
1. echo "1 22 333 4444">logs/my_test
2. cat logs/my_test
3. grep "3" logs/my_test
4. grep "3" logs/my_test>logs/new
5. cat logs/new

![pnHEEeP.png](https://s41.ax1x.com/2026/11/17/pnHEEeP.png)
lab/
├── logs/
│   ├── my_test
│   ├── new
│   ├── final1.txt
│   ├── final2.txt
│   └── final3.txt
├── data/
└── tmp/