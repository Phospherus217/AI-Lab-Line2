# Markdown 学习工作区

## 怎么用

1. 打开 VSCode，菜单 **文件 → 打开文件夹**，选中 `桌面\MarkdownFile` 这个文件夹。
2. 打开 `Markdown入门教程.md`。
3. 按 `Ctrl + K` 松手，再按 `V` —— 右边出现预览，左边改字右边立刻变。
4. 装好 Paste Image 插件后，用 `Ctrl + Alt + V` 粘贴截图，图片会自动存进 `images/`。

## 目录结构

```
MarkdownFile/
├── .vscode/
│   ├── settings.json      # 已调好的编辑器 + 插件配置
│   └── extensions.json    # 打开文件夹时 VSCode 会提示装这几个插件
├── images/                # 粘贴的截图自动存这里
├── Markdown入门教程.md     # 语法教程（本身就是测试文件）
└── README.md              # 本文件
```

## 装插件（如果 extensions.json 没弹出提示）

在 VSCode 终端里粘贴运行：

```bash
code --install-extension yzhang.markdown-all-in-one
code --install-extension shd101wyy.markdown-preview-enhanced
code --install-extension mushan.vscode-paste-image
code --install-extension yzane.markdown-pdf
```

装完重启一下 VSCode。
