def gen_toc(file_list):
    """生成总目录TOC，返回markdown格式文本"""
    toc_text = "#文档总目录\n\n"
    # 遍历每个md文件
    for f in file_list:
        # 添加一条文件链接
        toc_text += f"- [{f['path']}]({f['path']})\n"
        # 遍历文件内标题，按层级缩进
        for h in f["headings"]:
            indent = "  " * (h["level"] - 1)
            toc_text += f"{indent}- 标题 h{h['level']}\n"
    return toc_text

def save_report(toc_content, broken_links, heading_warn, out_path):
    """把所有检测结果拼成完整报告，写入文件"""
    report = toc_content + "\n# 检测异常报告\n\n"
    report += "## 损坏链接 / 失效图片\n\n"
    for item in broken_links:
        report += f"- 文件：`{item['file']}` | 资源：`{item['url']}` | 问题：{item['msg']}\n"
    report += "\n##标题层级警告\n\n"
    for item in heading_warn:
        report += f"- 文件：`{item['file']}` 存在跳级，当前 h{item['level']}\n"
    # 打开输出文件，写入报告文本，utf8防止中文乱码
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(report)

