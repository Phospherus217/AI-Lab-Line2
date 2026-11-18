# 导入os：操作系统内置库，用来遍历文件夹、拼接文件路径
import os
# 导入MarkdownIt：第三方md解析器，专门拆解markdown语法元素
from markdown_it import MarkdownIt

# 定义函数 scan_md_files，接收参数 root_dir：要扫描的根文件夹路径
def scan_md_files(root_dir: str):
    """
    函数功能：遍历目录，找到所有.md文件，解析里面的链接、图片、标题
    返回值：列表，里面每一项是一个字典，保存单个md文件的全部提取信息
    """
    # 创建一个md解析实例，后面用它解析文本
    md = MarkdownIt()
    # 准备空列表，存放所有md文件解析后的信息
    file_info_list = []

    # os.walk：递归遍历文件夹
    # root：当前正在遍历的文件夹路径
    # dirs：当前文件夹里面的子文件夹列表
    # files：当前文件夹里面的文件列表
    for root, dirs, files in os.walk(root_dir):
        # 循环遍历当前文件夹下每一个文件名
        for fname in files:
            # 判断：文件名小写后，是不是以 .md 结尾，只处理markdown文件
            if fname.lower().endswith(".md"):
                # 拼接完整绝对路径：文件夹路径 + 文件名
                full_path = os.path.join(root, fname)
                # 打开文件，只读模式，编码utf-8（防止中文乱码）
                with open(full_path, "r", encoding="utf-8") as f:
                    # 读取整个文档文本
                    content = f.read()
                # 把md文本解析成token（语法单元，标题/图片/链接都是token）
                tokens = md.parse(content)
                # 定义3个空列表，分别存链接、图片、标题
                links = []
                imgs = []
                headings = []

                # 遍历所有语法token，筛选我们需要的元素
                for token in tokens:
                    # token.type == "image" → 匹配 ![]() 图片语法
                    if token.type == "image":
                        # 取出图片src地址，加到图片列表
                        imgs.append(token.attrs.get("src"))
                    # token.type == "link_open" → 匹配 [文字](url) 超链接
                    if token.type == "link_open":
                        # 取出链接href地址
                        links.append(token.attrs.get("href"))
                    # token.type == "heading_open" → 匹配标题 # h1 ## h2
                    if token.type == "heading_open":
                        # token.tag 是 "h1" "h2"这种字符串，取第二个字符转数字，得到标题层级
                        level = int(token.tag[1])
                        # 保存层级
                        headings.append({"level": level})

                # 把这个文件的全部信息打包成字典，放进总列表
                file_info_list.append({
                    "path": full_path,
                    "links": links,
                    "images": imgs,
                    "headings": headings
                })
    # 遍历全部结束，返回所有文件信息
    return file_info_list
