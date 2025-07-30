# Rongcloud Native MCP Server（Rust）

基于 MCP 协议的融云 IM 服务（包装 Rust SDK）

## 安装

### 方法一：使用 pip 安装（推荐）

```bash
# 使用 pip 安装
pip install rc-im-native-mcp-server

# 或使用 uv 安装
uv pip install rc-im-native-mcp-server
```

### 方法二：从源码安装

1. 克隆项目：

```bash
git clone https://github.com/rongcloud/rc-im-mcp-demo.git
cd rc-im-mcp-demo
```

2. 安装 uv（如果没有）：

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

3. 创建并激活虚拟环境：

```bash
uv venv
source .venv/bin/activate
```

4. 安装项目：

```bash
uv pip install -e .
```

## 使用方法

### 1. 环境变量配置

在使用前，需要设置以下环境变量：

```bash
# 设置融云 AppKey
export APP_KEY="your_app_key"

# 设置融云 Token
export TOKEN="your_token"

# 设置融云导航服务器地址（可选）
export NAVI_HOST="your_navi_host"
```

### 2. 启动服务器

```bash
# 方法一：直接运行（推荐）
rc-im-native-mcp-server

# 方法二：使用 Python 模块运行
python -m src.server.server

# 方法三：使用 uv 运行
uv run -m src.server.server
```

### 3. macOS 用户特别说明

由于 macOS 的安全机制，首次运行时可能会遇到安全警告。请按照以下步骤解决：

1. 当看到安全警告时，点击"取消"按钮
2. 打开系统偏好设置（System Preferences）
3. 点击"安全性与隐私"（Security & Privacy）
4. 在"通用"（General）标签页中，你会看到一条关于 `librust_universal_imsdk.dylib` 的警告
5. 点击"仍要打开"（Open Anyway）按钮
6. 在弹出的确认对话框中点击"打开"（Open）
7. 现在你可以重新运行服务器了

#### 为什么会出现这个警告？

这个警告是 macOS 的安全机制（Gatekeeper）触发的，用于保护用户免受潜在的安全威胁。我们的动态库（`librust_universal_imsdk.dylib`）是安全的，但由于没有 Apple 开发者证书签名，所以会触发这个警告。

#### 安全说明

- 我们的动态库是开源的，代码经过安全审计
- 动态库仅用于本地 IM 服务，不会收集或上传任何用户数据
- 所有通信都使用加密通道，确保数据安全

## 主要功能与工具（tools）说明

服务端通过 MCP 协议暴露以下工具：

### 1. `init_and_connect`

- **功能**：初始化 IM 引擎并连接到 IM 服务器
- **参数**：
  - `timeout_sec` (int, 默认30)：连接超时时间（秒）
- **返回**：
  - `code` (int)：0 表示成功，非0为失败
  - `message` (str)：结果说明
  - `init_success` (bool)：初始化是否成功
  - `connect_success` (bool)：连接是否成功

### 2. `send_message`

- **功能**：发送 IM 消息给指定用户（支持单聊/群聊）
- **参数**：
  - `receiver` (str)：消息接收者ID
  - `content` (str)：消息内容
  - `conversation_type` (int, 默认1)：会话类型，1=单聊，2=群聊
- **返回**：
  - 失败：`code`、`message`
  - 成功：`code`、`message_id`、`message`

### 3. `get_history_messages`

- **功能**：获取与指定用户的历史消息
- **参数**：
  - `user_id` (str)：用户ID
  - `count` (int, 默认10)：获取的消息数量
- **返回**：
  - 失败：`code`、`message`
  - 成功：`code`、`messages`（消息数组）

### 4. `disconnect`

- **功能**：断开与 IM 服务器的连接
- **参数**：无
- **返回**：
  - `code` (int)：0 表示成功，非0为失败
  - `message` (str)：结果说明

## 在 Cursor 中使用

在 Cursor 的 mcp.json 中添加以下配置：

```json
{
  "rc_im_native_mcp": {
    "name": "rc-im-native-mcp-server",
    "type": "stdio",
    "command": "uvx",
    "args": [
      "rc-im-native-mcp-server"
    ],
    "env": {
      "APP_KEY": "your_app_key",
      "TOKEN": "your_token"
    }
  }
}
```

## 常见问题

### Q: 为什么需要设置环境变量？

A: 环境变量用于配置融云 IM 服务的基本参数，包括 AppKey 和 Token，这些是连接融云服务的必要信息。

### Q: 如何获取 AppKey 和 Token？

A: 请登录融云开发者控制台，在应用管理页面可以找到 AppKey。Token 需要根据你的用户系统生成，具体方法请参考融云文档。

### Q: 服务器启动后如何验证是否正常运行？

A: 服务器启动后，你可以使用融云提供的测试工具或 SDK 进行连接测试。如果看到连接成功的日志，说明服务器运行正常。

### Q: 如何查看服务器版本？

A: 运行以下命令：

```bash
rc-im-native-mcp-server version
```

## 典型用例

1. **初始化并连接**：
   - 调用 `init_and_connect` 工具
   - 等待连接成功响应

2. **发送消息**：
   - 调用 `send_message` 工具
   - 指定接收者和消息内容

3. **获取历史消息**：
   - 调用 `get_history_messages` 工具
   - 指定用户ID和消息数量

4. **断开连接**：
   - 调用 `disconnect` 工具
   - 确认断开成功

## 注意事项

- 启动服务前请确保本地 IM SDK 动态库和依赖已正确配置
- 环境变量必须设置正确，否则服务无法正常启动
- 工具接口参数和返回值请严格按照说明传递和解析
- 建议使用 MCP Inspector 或 MCP Client 进行测试

## 技术支持

如果遇到问题，请：

1. 检查环境变量是否正确设置
2. 查看日志输出，了解具体错误信息
3. 访问 [融云开发者社区](https://developer.rongcloud.cn) 获取帮助

## 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。
