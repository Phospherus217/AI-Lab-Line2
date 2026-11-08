# 文件读写要点（子目录样例）

这个文件放在 samples/sub/ 下，用来验证脚本的 **递归遍历** 是否生效。
如果 summary.json 里能出现本文件，说明 rglob 工作正常。

关键结论：文本文件读写一定要显式指定 encoding="utf-8"，
否则在 Windows 默认 GBK 环境下读中文会报 UnicodeDecodeError。

最后一行用来测试行数统计。
