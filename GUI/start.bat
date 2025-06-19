@echo off
echo ========================================
echo    机器狗统一控制中心启动脚本
echo ========================================
echo.

:: 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python，请先安装Python 3.7+
    pause
    exit /b 1
)

:: 显示Python版本
echo 检测到Python版本:
python --version

:: 检查必要的库
echo.
echo 检查必要的Python库...

python -c "import tkinter" 2>nul
if errorlevel 1 (
    echo 错误: tkinter库未安装
    pause
    exit /b 1
)

python -c "import pygame" 2>nul
if errorlevel 1 (
    echo 警告: pygame库未安装，手柄功能将不可用
    echo 请运行: pip install pygame
    echo.
)

python -c "import pynput" 2>nul
if errorlevel 1 (
    echo 警告: pynput库未安装，全局键盘监听将不可用
    echo 请运行: pip install pynput
    echo.
)

python -c "import robodog" 2>nul
if errorlevel 1 (
    echo 错误: robodog库未安装，无法控制机器狗
    echo 请确保robodog库已正确安装
    pause
    exit /b 1
)

echo ✓ 所有必要的库检查完成

:: 启动程序
echo.
echo 正在启动机器狗统一控制中心...
echo ========================================
echo.

python unified_control.py

echo.
echo 程序已退出
pause
