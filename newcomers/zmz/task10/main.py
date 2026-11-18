# 导入argparse：python内置库，专门解析命令行参数（任务a要求）
import argparse
# 导入我们自己写的三个模块里的函数
from md_parser import scan_md_files
from checker import check_broken_links, check_heading_level
from reporter import gen_toc, save_report

def main():
    # 1. 创建参数解析器，写工具描述，敲-h时会展示这段文字
    parser = argparse.ArgumentParser(
        description="Markdown文档检查清洗CLI工具：扫描目录、检测死链坏图、校验标题层级、生成目录索引"
    )
    # 添加参数 --dir 简写 -d
    parser.add_argument(
        "--dir", "-d",
        type=str,          # 参数类型：字符串（文件路径）
        required=True,     # 必填参数，不写程序直接报错
        help="指定要扫描的目录，示例：./docs"
    )
    # 添加参数 --output 简写 -o
    parser.add_argument(
        "--output", "-o",
        type=str,
        default="./report.md", # 不给参数时，默认输出 report.md
        help="报告输出路径，默认 ./report.md"
    )
    # 添加参数 --timeout 简写 -t
    parser.add_argument(
        "--timeout", "-t",
        type=int,
        default=5,  # 默认5秒超时，弱网改成8/10
        help="外网链接访问超时时间（秒）"
    )
    # 添加开关 --skip-link
    parser.add_argument(
        "--skip-link",
        action="store_true", # 布尔开关：命令带上它=True，不带=False
        help="带上这个参数，跳过外网链接检测（离线本地文档加速）"
    )
    # 解析命令行输入的参数，结果存在args里面
    args = parser.parse_args()

    # ========== 模块调度流程 ==========
    # 第一步：调用parser，扫描目录，拿到所有md文件信息
    md_files_info = scan_md_files(args.dir)
    link_check_result = []
    # 如果没有开启skip-link，才执行链接检测
    if not args.skip_link:
        link_check_result = check_broken_links(md_files_info, timeout=args.timeout)
    # 第二步：标题层级检测
    heading_warn_result = check_heading_level(md_files_info)
    # 第三步：生成目录文本
    toc_str = gen_toc(md_files_info)
    # 第四步：把全部结果保存成报告文件
    save_report(toc_str, link_check_result, heading_warn_result, args.output)
    # 控制台打印完成提示
    print(f"检测完成！报告已输出至：{args.output}")

# 固定写法：当直接运行这个文件（python main.py）时，执行main()
# 如果别的py导入这个文件，不会自动运行main
if __name__ == "__main__":
    main()
