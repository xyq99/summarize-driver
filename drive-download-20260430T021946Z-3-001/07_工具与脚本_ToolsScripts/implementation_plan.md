# Word 转 Markdown 转换计划

本计划旨在将当前目录下的所有 `.docx` 文件批量转换为 `.md` 格式。

## 用户评审确认

> [!IMPORTANT]
> 我在当前的系统 `PATH` 路径中暂未检测到 `pandoc` 命令。如果您已经安装了 `pandoc`，请确认它是否已加入环境变量。
> 如果脚本执行失败，可能需要您提供 `pandoc.exe` 的完整路径。

## 待办任务

- [ ] 编写转换脚本 `convert_docx_to_md.ps1`
- [ ] 执行脚本进行转换
- [ ] 验证转换结果

## 提议的更改

### [NEW] [convert_docx_to_md.ps1](file:///e:/下载/drive-download-20260430T021946Z-3-001/convert_docx_to_md.ps1)

该脚本将遍历当前目录，识别 `.docx` 文件并调用 `pandoc`。

## 验证计划

### 自动化测试
- 运行脚本后检查是否存在同名的 `.md` 文件。

### 手动验证
- 随机打开一个转换后的 `.md` 文件，确认内容格式正确。
