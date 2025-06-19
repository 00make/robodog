#!/bin/bash

echo "========================================"
echo "   机器狗统一控制中心启动脚本"
echo "========================================"
echo ""

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "错误: 未找到Python，请先安装Python 3.7+"
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

# 显示Python版本
echo "检测到Python版本:"
$PYTHON_CMD --version

# 检查必要的库
echo ""
echo "检查必要的Python库..."

# 检查tkinter
$PYTHON_CMD -c "import tkinter" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "错误: tkinter库未安装"
    exit 1
fi

# 检查pygame
$PYTHON_CMD -c "import pygame" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "警告: pygame库未安装，手柄功能将不可用"
    echo "请运行: pip install pygame"
    echo ""
fi

# 检查pynput
$PYTHON_CMD -c "import pynput" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "警告: pynput库未安装，全局键盘监听将不可用"
    echo "请运行: pip install pynput"
    echo ""
fi

# 检查robodog
$PYTHON_CMD -c "import robodog" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "错误: robodog库未安装，无法控制机器狗"
    echo "请确保robodog库已正确安装"
    exit 1
fi

echo "✓ 所有必要的库检查完成"

# 启动程序
echo ""
echo "正在启动机器狗统一控制中心..."
echo "========================================"
echo ""

$PYTHON_CMD unified_control.py

echo ""
echo "程序已退出"
