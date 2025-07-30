#!/bin/bash

# 确保脚本在错误时退出
set -e

echo "开始安装 RC-IM-MCP-Demo..."

# 检查是否安装了 uv
if ! command -v uv &> /dev/null; then
    echo "正在安装 uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi

# 创建虚拟环境（如果需要）
if [ ! -d ".venv" ]; then
    echo "创建虚拟环境..."
    uv venv
fi

# 激活虚拟环境
source .venv/bin/activate

# 安装项目依赖
echo "安装依赖..."
uv pip install -r requirements.txt

# 安装项目包
echo "安装项目包..."
WHEEL_FILE=$(ls dist/*.whl | sort -V | tail -n1)
if [ -f "$WHEEL_FILE" ]; then
    echo "找到安装包: $WHEEL_FILE"
    uv pip install "$WHEEL_FILE"
else
    echo "错误: 在dist目录下没有找到.whl文件"
    exit 1
fi

echo "安装完成！"
echo "你现在可以使用以下命令运行服务器："
echo "uv run -m rc_im_server start --app-key YOUR_APP_KEY --token YOUR_TOKEN" 