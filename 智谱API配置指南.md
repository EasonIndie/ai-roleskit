# 智谱AI API配置指南

## 🔑 获取智谱API密钥

### 1. 注册账号
- 访问 [智谱AI开放平台](https://bigmodel.cn)
- 注册并登录账号

### 2. 创建API密钥
- 在控制台中创建应用
- 获取API Key

### 3. 选择合适的模型
- `glm-4`: 主要模型，功能全面
- `glm-4-flash`: 快速响应模型
- `glm-4-air`: 经济实惠模型
- `glm-4-long`: 长文本模型

## 🛠️ 配置方法

### 方法1: 使用配置脚本（推荐）
```bash
# 激活虚拟环境
.\ai-toolkit-env\Scripts\activate

# 运行配置向导
python setup_keys.py

# 选择选项 3 (ZhipuAI)
# 输入你的API密钥
```

### 方法2: 手动配置文件
编辑 `.env` 文件：
```env
# 设置智谱为默认提供商
AI_PROVIDER=zhipu

# 智谱API配置
ZHIPU_API_KEY=你的智谱API密钥
```

### 方法3: 环境变量
```bash
# Windows
set ZHIPU_API_KEY=你的智谱API密钥

# Linux/Mac
export ZHIPU_API_KEY=你的智谱API密钥
```

## 🧪 测试配置

运行测试脚本验证配置：
```bash
# 激活环境
.\ai-toolkit-env\Scripts\activate

# 运行智谱测试
python test_zhipu.py
```

## 📋 配置参数说明

### 基本配置
```yaml
zhipu:
  model: "glm-4"              # 模型选择
  api_key: "${ZHIPU_API_KEY}"  # API密钥
  base_url: "https://open.bigmodel.cn/api/paas/v4/"  # API地址
  max_tokens: 2000            # 最大token数
  temperature: 0.7             # 创造性参数 (0-1)
  timeout: 30                  # 超时时间(秒)
```

### 模型选择建议

| 模型 | 适用场景 | 特点 |
|------|----------|------|
| `glm-4` | 通用对话、复杂问题 | 功能全面，质量高 |
| `glm-4-flash` | 快速响应、实时交互 | 响应快，成本低 |
| `glm-4-air` | 长文本、文档处理 | 性价比高 |
| `glm-4-long` | 超长文本、代码分析 | 支持长上下文 |

### 参数调优

- `temperature`:
  - 0.0-0.3: 严谨、准确（适合技术问题）
  - 0.4-0.7: 平衡（日常使用）
  - 0.8-1.0: 创意、发散（适合创意工作）

- `max_tokens`:
  - 短回答: 100-500
  - 中等回答: 500-1000
  - 长回答: 1000-2000
  - 超长文本: 2000+

## 💡 使用技巧

### 1. 角色扮演优化
```python
# 在系统提示中明确角色定位
system_prompt = f"""
你是{character.name}，{character.description}。
专业领域：{character.info.position}
经验背景：{character.info.experience}
请以专业、深入的语调回答问题。
"""
```

### 2. 流式输出
```python
# 启用流式输出获得更好的交互体验
request = AIRequest(
    messages=[...],
    stream=True
)

async for chunk in provider.chat_completion_stream(request):
    print(chunk, end="", flush=True)
```

### 3. 错误处理
```python
try:
    response = await provider.chat_completion(request)
except Exception as e:
    print(f"智谱API调用失败: {e}")
    # 可以使用备用模型或重试机制
```

## 🔧 故障排除

### 常见问题

1. **API密钥无效**
   ```
   解决方案: 检查API密钥是否正确，是否已激活
   ```

2. **网络连接问题**
   ```bash
   # 测试网络连接
   ping open.bigmodel.cn
   ```

3. **模型参数错误**
   ```
   解决方案: 检查模型名称是否正确，是否支持该功能
   ```

4. **配额超限**
   ```
   解决方案: 检查账户余额，或切换到更经济的模型
   ```

### 调试方法

1. **启用详细日志**
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

2. **测试基本连接**
   ```bash
   python test_zhipu.py
   ```

3. **检查配置**
   ```python
   from ai_toolkit.utils.config import config
   print(config.get_zhipu_config())
   ```

## 📊 性能优化

### 1. 模型选择策略
- 简单问题使用 `glm-4-flash`
- 复杂问题使用 `glm-4`
- 长文档使用 `glm-4-long`

### 2. 请求优化
- 合理设置 `max_tokens`
- 使用适当的 `temperature`
- 启用流式输出改善用户体验

### 3. 错误重试
```python
import asyncio
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
async def call_with_retry(provider, request):
    return await provider.chat_completion(request)
```

## 🎯 最佳实践

1. **API密钥安全**
   - 不要在代码中硬编码API密钥
   - 使用环境变量或配置文件
   - 定期轮换API密钥

2. **成本控制**
   - 监控API使用量
   - 选择合适的模型
   - 设置合理的token限制

3. **性能监控**
   - 记录响应时间
   - 监控错误率
   - 优化请求频率

---

## 🚀 开始使用

配置完成后，你可以：

1. **创建智谱角色**
   ```bash
   python cli.py character create expert --name "智谱专家" --provider zhipu
   ```

2. **开始对话**
   ```bash
   python cli.py dialogue start <character_id> --provider zhipu
   ```

3. **创意探索**
   ```bash
   python cli.py explore start "你的想法" --provider zhipu
   ```

享受智谱大模型带来的AI角色体验！