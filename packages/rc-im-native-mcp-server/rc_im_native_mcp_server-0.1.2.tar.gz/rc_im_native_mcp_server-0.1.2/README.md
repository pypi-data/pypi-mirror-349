# Rongcloud Native MCP Server（Rust）

## 项目简介

本项目是一个基于 MCP 协议的 Python IM 服务端演示，集成了真实的 IM SDK（通过本地动态库），并通过 MCP 协议对外提供标准化的消息服务能力。项目支持消息收发、历史消息查询、连接管理等功能，适配 MCP Inspector、MCP Client 等工具。

## 安装

### 快速安装（推荐）

```shell
# 克隆项目
git clone https://github.com/rongcloud/rc-im-mcp-demo.git
cd rc-im-mcp-demo

# 运行安装脚本
./scripts/install.sh
```

### 手动安装

1. 安装 uv（如果没有）：

```shell
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. 创建并激活虚拟环境：

```shell
uv venv
source .venv/bin/activate
```

3. 安装依赖：

```shell
uv pip install -r requirements.txt
```

4. 安装项目：

```shell
uv pip install -e .
```

### 验证安装

安装完成后，你可以通过以下命令验证安装：

```shell
# 查看版本
uv run -m src.server.server version

# 运行服务器
uv run -m src.server.server --app-key YOUR_APP_KEY --token YOUR_TOKEN
```

### 使用 uv 运行

```shell
# 直接运行服务器
uv run src/server/server.py main --app-key YOUR_APP_KEY --token YOUR_TOKEN

# 或者通过安装后的命令运行
uv run -m rc_im_server main --app-key YOUR_APP_KEY --token YOUR_TOKEN
```

## 在 Cursor 中使用

在 Cursor 的 mcp.json 中添加以下配置：

```json
"rc_im_native_mcp": {
      "name": "rc-im-native-mcp-server",
      "type": "stdio",
      "command": "uvx",
      "args": [
        "rc-im-native-mcp-server"
      ],
      "env": {
        "APP_KEY": "key",
        "TOKEN": "token",
      }
    },
```

## 主要功能与工具（tools）说明

服务端（`src/server/mcp_im_server.py`）通过 MCP 协议暴露以下工具：

### 1. `init_and_connect`

- **功能**：初始化 IM 引擎并连接到 IM 服务器。
- **参数**：
  - `timeout_sec` (int, 默认30)：连接超时时间（秒）。
- **返回**：
  - `code` (int)：0 表示成功，非0为失败。
  - `message` (str)：结果说明。
  - `init_success` (bool)：初始化是否成功。
  - `connect_success` (bool)：连接是否成功。

### 2. `send_message`

- **功能**：发送 IM 消息给指定用户（支持单聊/群聊）。
- **参数**：
  - `receiver` (str)：消息接收者ID。
  - `content` (str)：消息内容。
  - `conversation_type` (int, 默认1)：会话类型，1=单聊，2=群聊。
- **返回**：
  - 失败：`code`、`message`。
  - 成功：`code`、`message_id`、`message`。

### 3. `get_history_messages`

- **功能**：获取与指定用户的历史消息。
- **参数**：
  - `user_id` (str)：用户ID。
  - `count` (int, 默认10)：获取的消息数量。
- **返回**：
  - 失败：`code`、`message`。
  - 成功：`code`、`messages`（消息数组）。

### 4. `disconnect`

- **功能**：断开与 IM 服务器的连接。
- **参数**：无
- **返回**：
  - `code` (int)：0 表示成功，非0为失败。
  - `message` (str)：结果说明。

## 环境变量配置

服务端依赖以下环境变量，请在启动前设置：

- `APP_KEY`：IM 应用的 AppKey。
- `TOKEN`：IM 用户连接 Token。
- `NAVI_HOST`：IM SDK 导航服务器地址。

**示例（Linux/macOS）：**

```shell
export APP_KEY=your_app_key
export TOKEN=your_token
export NAVI_HOST=your_navi_host
```

## 启动服务

1. 安装依赖：

   ```shell
   pip install -r requirements.txt
   # 或
   pip install .
   ```

2. 启动服务端：

   ```shell
   python src/server/mcp_im_server.py
   # 或指定端口/协议
   # APP_KEY=xxx TOKEN=xxx NAVI_HOST=xxx python src/server/mcp_im_server.py
   ```

3. 服务端默认以 MCP Streamable HTTP 协议对外提供服务，端口为 8000。

## 客户端调用

- 推荐使用 MCP Inspector、MCP Client 或自定义 Python 客户端调用 MCP 工具接口。
- 也可通过 HTTP POST 方式直接调用 MCP 工具接口。

## 典型用例

- **初始化并连接**：调用 `init_and_connect` 工具。
- **发送消息**：调用 `send_message` 工具。
- **获取历史消息**：调用 `get_history_messages` 工具。
- **断开连接**：调用 `disconnect` 工具。

## 注意事项

- 启动服务前请确保本地 IM SDK 动态库和依赖已正确配置。
- 环境变量必须设置正确，否则服务无法正常启动。
- 工具接口参数和返回值请严格按照上文说明传递和解析。
- 如需扩展更多工具，可在 `src/server/mcp_im_server.py` 中添加新的 `@app.tool()`。

---

如有问题请查阅源码或联系项目维护者。
