# AI Character Toolkit - 智能角色生成工具包

一个功能完整的AI角色生成和管理系统，支持动态角色创建、智能对话和创意探索。

## 🌟 核心特性

- **🎭 动态角色生成**: 支持专家、用户、组织三种角色类型
- **💬 智能对话系统**: 多角色并发对话和消息管理
- **🔍 创意探索引擎**: AI辅助的创意想法分析和拓展
- **📊 集成分析工具**: 冲突检测、机会识别、综合分析
- **💾 数据持久化**: 完整的角色和对话数据存储
- **🔧 灵活配置**: 支持OpenAI和Claude双AI提供商

## 🚀 快速开始

### 1. 环境设置
```bash
# 激活虚拟环境
.\ai-toolkit-env\Scripts\activate

# 验证安装
python test_setup.py
```

### 2. 配置API密钥
```bash
# 运行配置向导
python setup_keys.py

# 或手动编辑 .env 文件
```

### 3. 运行演示
```bash
# 基础功能演示
python demo.py

# 角色使用指南
python character_usage_guide.py

# 实用示例集合
python 实用示例集合.py
```

## 📚 文档导航

| 文档 | 描述 | 适用用户 |
|------|------|----------|
| [使用说明书.md](./使用说明书.md) | 完整详细的使用手册 | 所有用户 |
| [快速参考.md](./快速参考.md) | 常用命令和快速参考 | 熟练用户 |
| [实用示例集合.py](./实用示例集合.py) | 实际应用场景代码示例 | 开发者 |

## 🎭 角色类型

### 专家角色 (EXPERT)
- **用途**: 提供专业知识和深度见解
- **示例**: 科学家、顾问、行业专家
- **特点**: 专业、深入、权威

### 用户角色 (USER)
- **用途**: 代表用户视角和需求
- **示例**: 客户、用户、利益相关者
- **特点**: 实用、体验导向、需求驱动

### 组织角色 (ORGANIZATION)
- **用途**: 代表机构或群体观点
- **示例**: 公司、部门、团队
- **特点**: 客观、全面、战略思考

## 💻 CLI命令

### 角色管理
```bash
# 创建角色
python cli.py character create <type> --name <name>

# 查看角色
python cli.py character list
python cli.py character show <character_id>
```

### 对话管理
```bash
# 开始对话
python cli.py dialogue start <character_id>

# 发送消息
python cli.py dialogue message <character_id> "你的消息"
```

### 创意探索
```bash
# 开始探索
python cli.py explore start "你的想法" --interactive

# 查看历史
python cli.py explore list
```

## 🔧 编程接口

### 创建角色
```python
from ai_toolkit.models.schemas import Character, CharacterInfo, CharacterType

character = Character(
    name="专家姓名",
    type=CharacterType.EXPERT,
    description="专业描述",
    info=CharacterInfo(
        name="专家姓名",
        position="职位",
        experience="经验"
    )
)
```

### 对话交互
```python
from ai_toolkit.ai.base import AIRequest

request = AIRequest(
    messages=[
        {"role": "system", "content": f"你是{character.name}，{character.description}"},
        {"role": "user", "content": "你的问题"}
    ]
)

response = await ai_provider.chat_completion(request)
```

## 📁 项目结构

```
ai-agent/
├── src/ai_toolkit/           # 核心代码库
│   ├── models/              # 数据模型
│   ├── core/                # 核心功能模块
│   ├── ai/                  # AI提供商接口
│   ├── storage/             # 数据存储
│   ├── utils/               # 工具函数
│   └── templates/           # 提示词模板
├── config/                  # 配置文件
├── data/                    # 数据存储目录
├── ai-toolkit-env/         # Python虚拟环境
├── .env                     # 环境变量配置
├── 使用说明书.md             # 详细使用文档
├── 快速参考.md               # 快速命令参考
├── README_项目说明.md        # 项目说明（本文件）
├── demo.py                  # 基础演示
├── character_usage_guide.py  # 角色使用指南
├── 实用示例集合.py            # 实用示例代码
├── test_setup.py           # 基础测试
└── setup_keys.py           # API配置工具
```

## ⚡ 系统要求

- Python 3.8+
- OpenAI API Key 或 Claude API Key
- Windows/Linux/macOS

## 🛠️ 安装依赖

所有依赖已安装在虚拟环境中，包括：
- `openai>=1.0.0` - OpenAI API客户端
- `anthropic>=0.3.0` - Claude API客户端
- `aiohttp>=3.8.0` - 异步HTTP客户端
- `click>=8.1.0` - CLI框架
- `rich>=13.0.0` - 富文本终端输出
- `jinja2>=3.1.0` - 模板引擎
- 其他工具库

## 🎯 应用场景

1. **专业咨询**: 创建领域专家进行专业咨询
2. **用户研究**: 模拟不同用户群体进行需求分析
3. **团队协作**: 创建多个角色进行头脑风暴
4. **教育培训**: 创建教师角色进行知识传授
5. **创意探索**: 利用AI进行创意想法拓展
6. **决策支持**: 多角度分析复杂问题

## 🔍 故障排除

### 常见问题

1. **Unicode编码错误**
   - 避免Unicode字符使用
   - 使用ASCII输出

2. **API密钥配置错误**
   - 重新运行: `python setup_keys.py`
   - 检查 `.env` 文件

3. **模块导入错误**
   - 确保激活虚拟环境
   - 检查Python路径

### 获取帮助

- 查看详细文档: [使用说明书.md](./使用说明书.md)
- 运行基础测试: `python test_setup.py`
- 参考示例代码: [实用示例集合.py](./实用示例集合.py)

## 📈 版本信息

- **当前版本**: v1.0.0
- **最后更新**: 2025年11月6日
- **Python版本**: 3.8+
- **支持平台**: Windows, Linux, macOS

## 🤝 贡献指南

欢迎提交Issue和Pull Request来改进这个项目。

## 📄 许可证

本项目采用MIT许可证，详见LICENSE文件。

---

## 🎉 开始使用

1. **激活环境**: `.\ai-toolkit-env\Scripts\activate`
2. **配置API**: `python setup_keys.py`
3. **运行演示**: `python demo.py`
4. **创建角色**: `python cli.py character create expert --name "你的专家"`
5. **开始对话**: `python cli.py dialogue start <角色ID>`

开始你的AI角色探索之旅吧！ 🚀