#!/bin/bash
# AI Character Toolkit 安装脚本

echo "🚀 安装 AI Character Toolkit"
echo "=============================="

# 检查Python版本
python_version=$(python3 --version 2>&1 | cut -d' ' -f2)
required_version="3.8"

echo "📋 检查系统要求..."
echo "   Python版本: $python_version (需要 >= $required_version)"

if python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
    echo "   ✅ Python版本满足要求"
else
    echo "   ❌ Python版本过低，请升级到Python 3.8或更高版本"
    exit 1
fi

# 创建虚拟环境（可选）
echo ""
echo "🔧 设置Python环境..."
read -p "是否创建虚拟环境？(y/n): " create_venv

if [ "$create_venv" = "y" ] || [ "$create_venv" = "Y" ]; then
    echo "   创建虚拟环境..."
    python3 -m venv ai_toolkit_env
    source ai_toolkit_env/bin/activate
    echo "   ✅ 虚拟环境已激活"
fi

# 安装依赖
echo ""
echo "📦 安装依赖包..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "   ✅ 依赖安装成功"
else
    echo "   ❌ 依赖安装失败"
    exit 1
fi

# 创建配置目录
echo ""
echo "📁 创建配置目录..."
config_dir="$HOME/.ai_toolkit"
mkdir -p "$config_dir"

# 复制配置文件
if [ ! -f "$config_dir/config.yaml" ]; then
    cp config/default.yaml "$config_dir/config.yaml"
    echo "   ✅ 配置文件已复制到: $config_dir/config.yaml"
else
    echo "   ⚠️  配置文件已存在，跳过复制"
fi

# 创建数据目录
data_dir="$config_dir/data"
mkdir -p "$data_dir"/{characters,dialogues,explorations,validations,backups}
echo "   ✅ 数据目录已创建: $data_dir"

# 设置权限
chmod +x cli.py
echo "   ✅ CLI脚本已设置执行权限"

# 运行测试
echo ""
echo "🧪 运行基础测试..."
python3 test_basic.py

if [ $? -eq 0 ]; then
    echo "   ✅ 基础测试通过"
else
    echo "   ⚠️  基础测试未完全通过，但安装可能仍然成功"
fi

# 显示使用说明
echo ""
echo "🎉 安装完成！"
echo "================"
echo ""
echo "📚 使用方法:"
echo "   1. 设置API密钥:"
echo "      export OPENAI_API_KEY='your-openai-api-key'"
echo "      # 或"
echo "      export CLAUDE_API_KEY='your-claude-api-key'"
echo ""
echo "   2. 运行CLI:"
echo "      python3 cli.py --help"
echo ""
echo "   3. 运行示例:"
echo "      python3 example.py"
echo ""
echo "   4. 开始创意探索:"
echo "      python3 cli.py explore start '你的想法' --interactive"
echo ""
echo "📖 更多信息:"
echo "   - 查看README.md了解详细文档"
echo "   - 查看config/default.yaml了解配置选项"
echo ""

if [ "$create_venv" = "y" ] || [ "$create_venv" = "Y" ]; then
    echo "💡 提示: 下次使用时请先激活虚拟环境:"
    echo "   source ai_toolkit_env/bin/activate"
    echo ""
fi