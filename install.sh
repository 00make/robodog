#!/bin/bash
set -e

echo "=========================================="
echo "   RoboDog SDK - UV 安装脚本"
echo "=========================================="

# 标记是否修改了 shell 配置文件
RC_FILES_MODIFIED=0

# 辅助函数：将目录添加到 shell 配置文件中
add_to_shell_rc() {
    local bin_dir="$1"
    local added=()
    
    # bash / sh
    for rc in "$HOME/.bashrc" "$HOME/.bash_profile" "$HOME/.profile"; do
        if [ -f "$rc" ]; then
            if ! grep -qF "$bin_dir" "$rc" 2>/dev/null; then
                echo "export PATH=\"$bin_dir:\$PATH\"" >> "$rc"
                added+=("$rc")
            fi
        fi
    done
    
    # zsh
    for rc in "$HOME/.zshrc" "$HOME/.zshenv"; do
        if [ -f "$rc" ]; then
            if ! grep -qF "$bin_dir" "$rc" 2>/dev/null; then
                echo "export PATH=\"$bin_dir:\$PATH\"" >> "$rc"
                added+=("$rc")
            fi
        fi
    done
    
    # fish
    local fish_config="$HOME/.config/fish/config.fish"
    if [ -f "$fish_config" ]; then
        if ! grep -qF "$bin_dir" "$fish_config" 2>/dev/null; then
            echo "fish_add_path $bin_dir" >> "$fish_config"
            added+=("$fish_config")
        fi
    fi
    
    # 如果没有任何已知的 rc 文件存在，根据当前 shell 创建
    if [ ${#added[@]} -eq 0 ]; then
        if [ -n "${ZSH_VERSION:-}" ]; then
            echo "export PATH=\"$bin_dir:\$PATH\"" >> "$HOME/.zshrc"
            added+=("$HOME/.zshrc")
        elif [ -n "${BASH_VERSION:-}" ]; then
            echo "export PATH=\"$bin_dir:\$PATH\"" >> "$HOME/.bashrc"
            added+=("$HOME/.bashrc")
        else
            echo "export PATH=\"$bin_dir:\$PATH\"" >> "$HOME/.profile"
            added+=("$HOME/.profile")
        fi
    fi
    
    if [ ${#added[@]} -gt 0 ]; then
        echo "📝 已将 $bin_dir 加入以下配置文件: ${added[*]}"
        echo "   提示：新配置将在下次打开终端时自动生效"
        RC_FILES_MODIFIED=1
    fi
}

# 检查 uv 是否安装，未安装则自动安装
if ! command -v uv &> /dev/null; then
    echo ""
    echo "⚠️ 未找到 uv，正在自动下载并安装..."
    echo ""

    # 使用 curl 进度条下载并执行 uv 安装脚本
    curl -fSL --progress-bar https://astral.sh/uv/install.sh | sh

    echo ""
    # 配置 shell 环境变量（写入 rc 文件）
    add_to_shell_rc "$HOME/.local/bin"
    
    # 加载 uv 到当前 shell 环境
    export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"

    if ! command -v uv &> /dev/null; then
        echo ""
        echo "❌ uv 自动安装后当前终端仍无法找到"
        echo ""
        echo "请执行以下命令刷新环境变量后重试："
        echo "  source ~/.bashrc"
        echo "  或 source ~/.zshrc"
        echo "  或重新打开终端"
        exit 1
    fi
    echo "✅ uv 安装成功"
fi

echo "✅ uv 已安装: $(uv --version)"

# 检查 Python 版本
PYTHON_VERSION=$(uv run python --version 2>/dev/null | awk '{print $2}' || echo "")
if [ -z "$PYTHON_VERSION" ]; then
    echo "⚠️ 警告: 未找到兼容的 Python 版本"
    echo "uv 将自动下载所需的 Python 版本..."
fi

# 创建虚拟环境
echo ""
echo "📦 创建虚拟环境 (.venv)..."
uv venv --clear

# 安装项目及依赖
echo ""
echo "📦 安装 RoboDog SDK [gui + dev]..."
uv pip install -e ".[gui,dev]"

# 将 uv 链接到虚拟环境中，方便 source activate 后直接使用
UV_PATH=$(command -v uv)
if [ -n "$UV_PATH" ] && [ ! -e ".venv/bin/uv" ]; then
    ln -sf "$UV_PATH" ".venv/bin/uv"
    echo "🔗 已将 uv 链接到 .venv/bin/uv（激活环境后可直接使用 uv）"
fi

echo ""
echo "=========================================="
echo "   ✅ 安装完成!"
echo "=========================================="
echo ""
echo "使用方式:"
echo "  激活环境: source .venv/bin/activate"
echo "  运行示例: python examples/demo_basic_movement.py"
echo "  运行 GUI:  python GUI/unified_control.py"
echo "  版本检查: python check_python_version.py"
echo ""
echo "使用 uv 直接运行（无需手动激活）:"
echo "  uv run python examples/demo_basic_movement.py"
echo "  uv run python GUI/unified_control.py"
echo ""

if [ "${RC_FILES_MODIFIED:-0}" -eq 1 ]; then
    echo "⚠️ 提示：由于修改了 shell 配置文件，"
    echo "   如果在新终端中找不到 uv，请执行："
    echo "     source ~/.zshrc     (zsh 用户)"
    echo "     source ~/.bashrc    (bash 用户)"
    echo ""
fi
