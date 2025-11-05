# AI Character Toolkit (动态AI角色生成工具包)

一个基于Python的动态AI角色生成和验证工具包，实现《动态AI角色生成工具包.md》中的完整功能。

## 功能特性

### 🔍 创意探索 (Creative Exploration)
- 基于AI的深度想法探索
- 多维度问题生成和回答
- 利益相关者识别
- 知识领域分析
- 实施环境评估

### 🎭 角色生成 (Character Generation)
- 自动生成三种角色类型：用户、专家、组织
- 详细的角色背景和专业能力定义
- 角色验证和优化
- 角色模板管理

### 💬 对话管理 (Dialogue Management)
- 角色化对话系统
- 多轮对话支持
- 对话历史管理
- 流式响应支持

### 🔀 并发验证 (Concurrent Validation)
- 多角色并发对话验证
- 角色间观点对比分析
- 一致性评估
- 冲突识别

### 📊 整合分析 (Integration Analysis)
- 多维度观点整合
- 决策报告生成
- 风险评估矩阵
- 实施路线图

### 💾 数据存储 (Data Storage)
- 文件存储系统 (JSON/YAML)
- 数据备份和恢复
- 存储统计信息

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 环境配置

1. 复制配置文件：
```bash
cp config/default.yaml ~/.ai_toolkit/config.yaml
```

2. 设置AI提供商API密钥：
```bash
export OPENAI_API_KEY="your-openai-api-key"
# 或者
export CLAUDE_API_KEY="your-claude-api-key"
```

### 基本使用

#### 1. 创意探索
```bash
python cli.py explore start "我想开发一个AI辅助学习的移动应用" --interactive
```

#### 2. 生成角色
```bash
python cli.py character generate <exploration_id> --type user
python cli.py character generate <exploration_id>  # 生成所有角色
```

#### 3. 开始对话
```bash
python cli.py dialogue start <character_id> --title "产品功能讨论"
```

#### 4. 并发验证
```bash
python cli.py validate concurrent "这个产品的核心价值主张是什么？" --characters char1,char2,char3
```

#### 5. 生成分析报告
```bash
python cli.py analysis report <validation_id>
```

## 架构设计

```
ai-character-toolkit/
├── src/ai_toolkit/
│   ├── core/                   # 核心功能模块
│   │   ├── exploration.py      # 创意探索
│   │   ├── character.py        # 角色生成和管理
│   │   ├── dialogue.py         # 对话管理
│   │   ├── concurrent.py       # 并发验证
│   │   └── analysis.py         # 整合分析
│   ├── models/                 # 数据模型
│   │   └── schemas.py          # 数据结构定义
│   ├── ai/                     # AI提供商集成
│   │   ├── base.py             # AI提供商基类
│   │   ├── openai_provider.py  # OpenAI集成
│   │   └── claude_provider.py  # Claude集成
│   ├── templates/              # 提示词模板
│   │   └── prompts.py          # 模板管理
│   ├── storage/                # 数据存储
│   │   └── file_storage.py     # 文件存储实现
│   └── utils/                  # 工具模块
│       ├── config.py           # 配置管理
│       └── logger.py           # 日志工具
├── templates/                  # Jinja2模板文件
├── config/                     # 配置文件
├── cli.py                      # 命令行界面
└── requirements.txt            # 依赖列表
```

## 配置说明

主配置文件位于 `config/default.yaml`，包含：

- **AI提供商配置**：OpenAI/Claude API设置
- **存储配置**：数据存储格式和路径
- **日志配置**：日志级别和输出格式
- **对话配置**：对话历史和上下文设置
- **并发配置**：并发处理参数

## API参考

### 核心类

#### CharacterManager
```python
from ai_toolkit.core.character import CharacterManager

manager = CharacterManager(ai_provider)
character = await manager.create_character(exploration_summary, CharacterType.USER)
```

#### CreativeExplorer
```python
from ai_toolkit.core.exploration import CreativeExplorer

explorer = CreativeExplorer(ai_provider)
session = await explorer.start_exploration("初始想法")
result = await explorer.explore_idea(session.id, "用户输入")
```

#### DialogueManager
```python
from ai_toolkit.core.dialogue import DialogueManager

dialogue_manager = DialogueManager(ai_provider, character_manager)
dialogue = await dialogue_manager.create_dialogue(character_id)
response = await dialogue_manager.send_message(dialogue.id, "消息内容")
```

#### ConcurrentValidator
```python
from ai_toolkit.core.concurrent import ConcurrentValidator

validator = ConcurrentValidator(ai_provider, character_manager)
session = await validator.create_validation_session("问题", character_ids)
result = await validator.run_concurrent_validation(session.id, character_ids)
```

## 扩展开发

### 添加新的AI提供商

1. 继承 `BaseAIProvider`：
```python
from ai_toolkit.ai.base import BaseAIProvider

class CustomAIProvider(BaseAIProvider):
    @property
    def provider_name(self) -> str:
        return "custom"

    async def chat_completion(self, request: AIRequest) -> AIResponse:
        # 实现自定义AI调用
        pass
```

### 自定义角色模板

1. 在 `templates/` 目录创建新的模板文件
2. 在 `templates/prompts.py` 中注册模板
3. 使用 `template_manager.render_template()` 调用

### 扩展存储后端

1. 继承存储基类实现自定义存储
2. 支持数据库存储、云存储等

## 测试

```bash
# 运行所有测试
python -m pytest tests/

# 运行特定模块测试
python -m pytest tests/test_exploration.py

# 运行并发测试
python -m pytest tests/test_concurrent.py -v
```

## 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 更新日志

### v0.1.0 (2024-01-XX)
- 初始版本发布
- 实现核心功能模块
- 支持OpenAI和Claude AI
- 完整的CLI界面
- 文件存储系统

## 支持与反馈

- 📧 Email: contact@ai-agent.com
- 🐛 Issues: [GitHub Issues](https://github.com/ai-agent/ai-character-toolkit/issues)
- 📖 文档: [在线文档](https://ai-character-toolkit.readthedocs.io/)

## 致谢

感谢《动态AI角色生成工具包.md》文档提供的理论基础和设计指导。

---

*本工具包基于Python开发，支持异步并发处理，旨在为创意工作者和产品经理提供强大的AI辅助工具。*