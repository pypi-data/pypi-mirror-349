#!/bin/bash

# 使用uv安装pip-tools（如果没有安装）
uv pip install pip-tools

# 使用uv pip-compile生成requirements.txt
uv pip compile pyproject.toml -o requirements.txt --generate-hashes 