# 导入需要的工具包
from pathlib import Path
import json
import sys

def count_one_file(file_path: Path):
    """统计单个md文件：行数、总字符数"""
    # ========== 知识点1：with open 打开文件 ==========
    # with 自动帮你关闭文件，不用手动写close()
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()  # 一次性读取全部内容

    # 算行数
    line_num = content.count("\n")
    # 如果最后一行没有换行，行数+1
    if content and not content.endswith("\n"):
        line_num += 1

    char_num = len(content)  # 总字符（包含换行、空格）
    return {
        "lines": line_num,
        "chars": char_num
    }


def scan_md(folder_path: str):
    """遍历文件夹，找到所有md文件"""
    root = Path(folder_path)
    result = {
        "files": {},
        "skipped": []
    }

    # ========== 知识点2：pathlib 路径处理 ==========
    # **/*.md 代表递归找所有子文件夹里面的md
    md_list = root.glob("**/*.md")

    for md_file in md_list:
        # 只处理文件，跳过名字叫xxx.md的文件夹
        if not md_file.is_file():
            continue

        try:
            # ========== 知识点3：try-except 异常捕获 ==========
            info = count_one_file(md_file)
            # 存相对路径，方便看
            rel_path = md_file.relative_to(root).as_posix()
            result["files"][rel_path] = info
        except Exception as e:
            # 出错的文件放进skipped，程序继续跑，不会直接崩溃
            result["skipped"].append({
                "filename": str(md_file),
                "reason": str(e)
            })
    return result


def main():
    # 命令行获取要扫描的文件夹，不传就默认当前文件夹
    if len(sys.argv) >= 2:
        target_folder = sys.argv[1]
    else:
        target_folder = "."

    data = scan_md(target_folder)

    # ========== 知识点4：json 写入文件 ==========
    with open("summary.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("完成！已经生成 summary.json")


if __name__ == "__main__":
    main()
