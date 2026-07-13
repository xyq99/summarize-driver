这份说明整理了你从**下载、安装、登录到成功运行 Cursor Agent** 的全过程，方便你日后查阅或分享给团队其他成员。

# Cursor Agent 部署与使用快速指南

**Cursor Agent** 是 AI 代码编辑器 Cursor 推出的**终端智能代理工具**。它允许开发者直接在 Linux 命令行中调用其顶级的 AI 能力（如 Composer 引擎），实现自动检索 SDK 代码、跨文件编写/修改驱动、自动执行编译及修复错误等深度开发任务。

## 一、 安装与环境配置

在 Linux 终端中执行安装脚本：

> <span class="mark">Bash</span>
>
> <span class="mark">curl https://cursor.com/install -fsS \| bash\
> </span>

### 安装成功提示：

- 自动检测系统环境（如 linux/x64）。

- 自动下载、解压并成功将可执行文件安装至 ~/.local/bin 目录。

- 自动创建好软链接（Symlink）。

### 🛠️ 关键后续配置：

为了能在任意路径下直接使用 agent 命令，需要将工具路径加入系统环境变量。在 **bash** 环境下依次执行以下两行命令：

> <span class="mark">Bash</span>
>
> <span class="mark">echo 'export PATH="\$HOME/.local/bin:\$PATH"' \>\> ~/.bashrc\
> source ~/.bashrc\
> </span>

## 二、 首次启动与账号登录

在终端输入 agent 启动工具：

> <span class="mark">Bash</span>
>
> <span class="mark">agent\
> </span>

1.  **触发登录：** 终端显示版本号并提示 Press any key to log in...，此时在终端内**按任意键**。

2.  **跳转授权：** 终端会生成一个专属的验证链接：\
    \[https://cursor.com/loginDeepControl?challenge=\](https://cursor.com/loginDeepControl?challenge=)...

3.  **完成登录：** 复制该链接至浏览器中打开，登录你的 Cursor 账号并点击授权。

4.  **终端同步：** 网页端授权后，终端会显示 Signing in...，验证通过后即可自动进入下一步。

## 三、 工作区安全信任（Workspace Trust）

进入目录后，Cursor Agent 会弹出安全提示：

⚠ Workspace Trust Required

- **原因：** 因为 Agent 拥有读取文件和在终端**自动执行脚本/编译命令**的高权限，因此需要确保当前目录是安全的。

- **操作：** 看到提示后，直接在键盘上按下字母 **a**（选择 *\[a\] Trust this workspace*），即可永久信任当前工作目录。

## 四、 正式进入 AI 交互界面

通过验证后，你会看到如下常驻交互界面：

> <span class="mark">Plaintext</span>
>
> <span class="mark">Cursor Agent\
> v2026.06.24-xxxxxxx\
> Tip: Use /config to customize Cursor settings and behavior.\
> \
> → Plan, search, build anything\
> \
> Composer 2.5 Fast\
> ~/nova · 98331_sdk_v3.03.108\
> </span>

### 💡 界面核心信息解读：

- **/config 命令：** 在输入框输入 /config 可以调整 AI 的行为偏好、更换大模型底座或调整网络。

- **AI 引擎（Composer 2.5 Fast）：** 当前默认启用 Cursor 顶级的全自动协同引擎，擅长感知多文件关联并直接帮你改写代码。

- **上下文感知（~/nova · 98331_sdk_v3.03.108）：** Agent 已自动锁定并加载了你当前的 **98331_sdk_v3.03.108** 项目上下文。接下来你对它说的每一句话，它都会基于该 SDK 的代码结构来理解。

## 🚀 进阶：如何给 Agent 派活？

现在你已经可以在 → 提示符后直接输入**中文指令**了。由于它已经完美融合了你的 SDK 环境，你可以直接尝试以下研发场景：

- **代码检索：** “帮我全局搜一下这个 SDK 里 GPIO 驱动的初始化函数在哪，并解释一下它的引脚配置逻辑。”

- **代码生成与修改：** “参考现有的 I2C 驱动，在当前目录下帮我搭建一个全新的 SPI 芯片驱动框架。”

- **编译与调优：** “直接帮我运行当前目录下的 Makefile 进行编译，如果报错了，请自动分析日志并帮我修改代码修复它。”
