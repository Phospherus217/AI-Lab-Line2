# 导入requests，用来访问外网链接
import requests
# 导入os，用来判断本地图片/本地链接文件是否存在
import os

# 函数：检测坏链接、损坏图片
# 参数：file_list 是上面parser返回的文件信息列表；timeout 超时秒数
def check_broken_links(file_list, timeout: int):
    """检测外网死链 + 本地不存在的图片/本地链接"""
    broken = []  # 空列表，存放异常链接信息
    # 遍历每一个md文件
    for file in file_list:
        fp = file["path"]  # 当前md文件完整路径
        # 遍历这个文件里所有超链接
        for url in file["links"]:
            # 判断：是http/https开头的外网链接
            if url.startswith("http"):
                try:
                    # HEAD请求：只请求响应头，不下载页面内容，速度更快
                    resp = requests.head(url, timeout=timeout)
                    # 状态码 >=400 代表访问失败（404找不到、403禁止访问等）
                    if resp.status_code >= 400:
                        broken.append({
                            "file": fp,
                            "url": url,
                            "msg": f"HTTP状态码:{resp.status_code}"
                        })
                # 捕获所有网络异常：超时、域名不存在、网络不通
                except requests.exceptions.RequestException as e:
                    broken.append({
                        "file": fp,
                        "url": url,
                        "msg": str(e)
                    })
            else:
                # 不是http → 本地相对路径（./xxx.png）
                # 获取当前md文件所在文件夹
                base_dir = os.path.dirname(fp)
                # 拼接本地资源的完整路径
                local_path = os.path.abspath(os.path.join(base_dir, url))
                # 判断这个本地文件是否不存在
                if not os.path.exists(local_path):
                    broken.append({
                        "file": fp,
                        "url": url,
                        "msg": "本地文件缺失（坏图/本地死链）"
                    })
        # 遍历当前文件里所有图片src，和链接逻辑一样，检测坏图片
        for img_url in file["images"]:
            if img_url.startswith("http"):
                try:
                    resp = requests.head(img_url, timeout=timeout)
                    if resp.status_code >= 400:
                        broken.append({"file": fp, "url": img_url, "msg": f"图片HTTP:{resp.status_code}"})
                except requests.exceptions.RequestException as e:
                    broken.append({"file": fp, "url": img_url, "msg": str(e)})
            else:
                base_dir = os.path.dirname(fp)
                local_path = os.path.abspath(os.path.join(base_dir, img_url))
                if not os.path.exists(local_path):
                    broken.append({"file": fp, "url": img_url, "msg": "本地图片缺失"})
    return broken

# 函数：检测标题跳级（禁止h1直接跳到h3这种不规范写法）
def check_heading_level(file_list):
    warn_list = []
    for f in file_list:
        last_level = 0  # 记录上一个标题层级，初始0
        for h in f["headings"]:
            lv = h["level"]
            # 判断：当前层级 比上一层+1还大 → 跳级
            if lv > last_level + 1:
                warn_list.append({
                    "file": f["path"],
                    "level": lv,
                    "msg": f"标题跳级！上一级标题是 h{last_level}"
                })
            # 更新上一层标题层级
            last_level = lv
    return warn_list
