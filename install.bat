@echo off
echo ==========================================
echo    RoboDog SDK - UV 安装脚本
echo ==========================================
echo.

:: 检查 uv 是否安装，未安装则自动安装
uv --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ⚠️ 未找到 uv，正在自动下载并安装...
    echo.

    :: 使用 curl 进度条下载 uv 安装脚本，然后执行
    curl.exe -fSL --progress-bar https://astral.sh/uv/install.ps1 -o "%TEMP%\uv-install.ps1"
    if errorlevel 1 (
        echo ❌ 下载 uv 安装脚本失败，请检查网络连接
        pause
        exit /b 1
    )

    powershell -ExecutionPolicy ByPass -File "%TEMP%\uv-install.ps1"
    del /Q "%TEMP%\uv-install.ps1" 2>nul
    echo.

    :: 刷新环境变量以找到新安装的 uv
    for /f "delims=" %%i in ('powershell -Command "[Environment]::GetEnvironmentVariable('Path','User')"') do set "USER_PATH=%%i"
    set "PATH=%USER_PATH%;%PATH%"

    :: 再次检测 uv，如仍失败则尝试临时添加常见路径
    uv --version >nul 2>&1
    if errorlevel 1 (
        if exist "%USERPROFILE%\.cargo\bin\uv.exe" (
            set "PATH=%USERPROFILE%\.cargo\bin;%PATH%"
        ) else if exist "%USERPROFILE%\.local\bin\uv.exe" (
            set "PATH=%USERPROFILE%\.local\bin;%PATH%"
        )
    )

    uv --version >nul 2>&1
    if errorlevel 1 (
        echo ❌ uv 自动安装后仍无法找到
        echo.
        echo 请重新打开终端后重试
        pause
        exit /b 1
    )
    echo ✅ uv 安装成功
)

for /f "tokens=*" %%a in ('uv --version') do set UV_VER=%%a
echo ✅ uv 已安装: %UV_VER%

echo.
echo 📦 创建虚拟环境 (.venv)...
uv venv --clear

echo.
echo 📦 安装 RoboDog SDK [gui + dev]...
uv pip install -e ".[gui,dev]"

:: 将 uv 复制/链接到虚拟环境中，方便 activate 后直接使用
for /f "delims=" %%p in ('where uv') do set UV_PATH=%%p
if exist "%UV_PATH%" (
    if not exist ".venv\Scripts\uv.exe" (
        mklink ".venv\Scripts\uv.exe" "%UV_PATH%" >nul 2>&1
        if errorlevel 1 (
            copy /Y "%UV_PATH%" ".venv\Scripts\uv.exe" >nul
        )
        echo 🔗 已将 uv 添加到 .venv\Scripts（激活环境后可直接使用 uv）
    )
)

echo.
echo ==========================================
echo    ✅ 安装完成!
echo ==========================================
echo.
echo 使用方式:
echo   激活环境: .venv\Scripts\activate
echo   运行示例: python examples\demo_basic_movement.py
echo   运行 GUI:  python GUI\unified_control.py
echo   版本检查: python check_python_version.py
echo.
echo 使用 uv 直接运行（无需手动激活）:
echo   uv run python examples\demo_basic_movement.py
echo   uv run python GUI\unified_control.py
echo.

pause
