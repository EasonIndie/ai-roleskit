@echo off
REM AI Character Toolkit Windows 安装脚本

echo 🚀 安装 AI Character Toolkit
echo ==============================

REM 检查Python版本
echo 📋 检查系统要求...
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ 未找到Python，请先安装Python 3.8或更高版本
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set python_version=%%i
echo    Python版本: %python_version%

REM 检查Python版本是否满足要求
python -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Python版本过低，请升级到Python 3.8或更高版本
    pause
    exit /b 1
)
echo    ✅ Python版本满足要求

REM 创建虚拟环境（可选）
echo.
echo 🔧 设置Python环境...
set /p create_venv="是否创建虚拟环境？(y/n): "

if /i "%create_venv%"=="y" (
    echo    创建虚拟环境...
    python -m venv ai_toolkit_env
    call ai_toolkit_env\Scripts\activate.bat
    echo    ✅ 虚拟环境已激活
)

REM 安装依赖
echo.
echo 📦 安装依赖包...
pip install -r requirements.txt

if %ERRORLEVEL% EQU 0 (
    echo    ✅ 依赖安装成功
) else (
    echo    ❌ 依赖安装失败
    pause
    exit /b 1
)

REM 创建配置目录
echo.
echo 📁 创建配置目录...
set config_dir=%USERPROFILE%\.ai_toolkit
if not exist "%config_dir%" mkdir "%config_dir%"

REM 复制配置文件
if not exist "%config_dir%\config.yaml" (
    copy config\default.yaml "%config_dir%\config.yaml" >nul
    echo    ✅ 配置文件已复制到: %config_dir%\config.yaml
) else (
    echo    ⚠️  配置文件已存在，跳过复制
)

REM 创建数据目录
set data_dir=%config_dir%\data
if not exist "%data_dir%" mkdir "%data_dir%"
if not exist "%data_dir%\characters" mkdir "%data_dir%\characters"
if not exist "%data_dir%\dialogues" mkdir "%data_dir%\dialogues"
if not exist "%data_dir%\explorations" mkdir "%data_dir%\explorations"
if not exist "%data_dir%\validations" mkdir "%data_dir%\validations"
if not exist "%data_dir%\backups" mkdir "%data_dir%\backups"
echo    ✅ 数据目录已创建: %data_dir%

REM 运行测试
echo.
echo 🧪 运行基础测试...
python test_basic.py

if %ERRORLEVEL% EQU 0 (
    echo    ✅ 基础测试通过
) else (
    echo    ⚠️  基础测试未完全通过，但安装可能仍然成功
)

REM 显示使用说明
echo.
echo 🎉 安装完成！
echo ================
echo.
echo 📚 使用方法:
echo    1. 设置API密钥:
echo       set OPENAI_API_KEY=your-openai-api-key
echo       或
echo       set CLAUDE_API_KEY=your-claude-api-key
echo.
echo    2. 运行CLI:
echo       python cli.py --help
echo.
echo    3. 运行示例:
echo       python example.py
echo.
echo    4. 开始创意探索:
echo       python cli.py explore start "你的想法" --interactive
echo.
echo 📖 更多信息:
echo    - 查看README.md了解详细文档
echo    - 查看config\default.yaml了解配置选项
echo.

if /i "%create_venv%"=="y" (
    echo 💡 提示: 下次使用时请先激活虚拟环境:
    echo    ai_toolkit_env\Scripts\activate.bat
    echo.
)

echo 按任意键退出...
pause >nul