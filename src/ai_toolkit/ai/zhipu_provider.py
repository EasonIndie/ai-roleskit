"""
智谱AI Provider for AI Character Toolkit
支持智谱大模型的AI提供商实现
"""

import asyncio
import os
from typing import Dict, List, Optional, Any, AsyncGenerator
from datetime import datetime

from .base import BaseAIProvider, AIRequest, AIResponse, AIModel
from ..utils.logger import get_logger


class ZhipuProvider(BaseAIProvider):
    """智谱AI提供商实现"""

    def __init__(self, config: Dict[str, Any]):
        """
        初始化智谱AI提供商

        Args:
            config: 配置字典，包含api_key、model等
        """
        super().__init__(config)
        self.logger = get_logger(__name__)

        # 配置参数
        self.api_key = config.get('api_key') or os.getenv('ZHIPU_API_KEY')
        self.model = config.get('model', 'glm-4')
        self.base_url = config.get('base_url', 'https://open.bigmodel.cn/api/paas/v4/')
        self.max_tokens = config.get('max_tokens', 2000)
        self.temperature = config.get('temperature', 0.7)
        self.timeout = config.get('timeout', 30)

        if not self.api_key:
            raise ValueError("智谱API密钥未配置，请设置ZHIPU_API_KEY环境变量或在配置中指定api_key")

        # 延迟导入zai包，只在需要时导入
        try:
            import httpx
            from zai import ZhipuAiClient

            # 优化的httpx客户端配置
            # 保持使用同步客户端，因为ZhipuAI SDK可能要求同步客户端
            # 优化超时配置和连接池设置
            http_client = httpx.Client(
                timeout=httpx.Timeout(
                    timeout=self.timeout,  # 总超时
                    connect=15.0,          # 连接超时增加到15秒
                    read=45.0,             # 读取超时45秒
                    write=30.0             # 写入超时30秒
                ),
                limits=httpx.Limits(
                    max_keepalive_connections=20,  # 保持连接池
                    max_connections=100,           # 最大连接数
                    keepalive_expiry=30.0          # 保持连接过期时间
                ),
                follow_redirects=True,
                verify=True  # 启用SSL验证
            )

            self.client = ZhipuAiClient(
                api_key=self.api_key,
                http_client=http_client
            )
            self.logger.info("智谱AI客户端初始化成功")
        except ImportError as e:
            if "socksio" in str(e):
                raise ImportError(
                    "检测到SOCKS代理配置问题。请尝试:\n"
                    "1. 关闭系统代理\n"
                    "2. 或安装: pip install httpx[socks]\n"
                    "3. 或设置环境变量: set HTTP_PROXY= 和 set HTTPS_PROXY=\n"
                    f"详细错误: {e}"
                )
            else:
                raise ImportError(
                    "智谱SDK未安装，请运行: pip install zai-sdk\n"
                    f"详细错误: {e}"
                )
        except Exception as e:
            raise Exception(f"智谱AI客户端初始化失败: {e}")

    @property
    def provider_name(self) -> str:
        """获取提供商名称"""
        return "ZhipuAI"

    @property
    def default_model(self) -> str:
        """获取默认模型名称"""
        return self.model

    async def initialize(self) -> None:
        """初始化AI提供商"""
        try:
            # 优化初始化流程 - 延迟连接测试，避免阻塞初始化
            self.logger.info("智谱AI提供商初始化完成")
            self._connection_tested = False  # 标记连接测试未完成
        except Exception as e:
            self.logger.error(f"智谱AI提供商初始化失败: {e}")
            raise

    async def _test_connection(self):
        """测试API连接 - 延迟到首次使用时执行"""
        try:
            if self._connection_tested:
                return True  # 连接已测试过，跳过

            import time
            start_time = time.time()

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "test"}],
                max_tokens=1
            )

            duration = time.time() - start_time

            if response.choices:
                self.logger.info(f"智谱API连接测试成功，耗时 {duration:.2f} 秒")
                self._connection_tested = True
                return True
            else:
                raise Exception("智谱API连接测试失败：无响应")
        except Exception as e:
            self.logger.error(f"智谱API连接测试失败: {e}")
            self._connection_tested = False
            raise

    def _load_models(self) -> List[AIModel]:
        """加载可用的智谱模型"""
        return [
            AIModel(
                name="glm-4",
                provider="zhipu",
                max_tokens=8000,
                supports_streaming=True,
                supports_function_calling=True,
                cost_per_token=0.001
            ),
            AIModel(
                name="glm-4-flash",
                provider="zhipu",
                max_tokens=8000,
                supports_streaming=True,
                supports_function_calling=True,
                cost_per_token=0.0005
            ),
            AIModel(
                name="glm-4-air",
                provider="zhipu",
                max_tokens=8000,
                supports_streaming=True,
                supports_function_calling=True,
                cost_per_token=0.0001
            ),
            AIModel(
                name="glm-4-long",
                provider="zhipu",
                max_tokens=32768,
                supports_streaming=True,
                supports_function_calling=True,
                cost_per_token=0.005
            )
        ]

    def _convert_request_format(self, request: AIRequest) -> Dict[str, Any]:
        """
        转换请求格式到智谱API格式

        Args:
            request: 标准AI请求

        Returns:
            智谱API请求格式
        """
        # 转换消息格式
        messages = []
        for msg in request.messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            messages.append({"role": role, "content": content})

        # 构建请求参数
        zhipu_request = {
            "model": self.model,
            "messages": messages,
            "max_tokens": request.max_tokens or self.max_tokens,
            "temperature": request.temperature or self.temperature,
            "stream": request.stream
        }

        # 添加可选参数
        if request.top_p:
            zhipu_request["top_p"] = request.top_p
        if request.stop:
            zhipu_request["stop"] = request.stop

        return zhipu_request

    def _convert_response_format(self, response) -> AIResponse:
        """
        转换智谱API响应格式到标准格式

        Args:
            response: 智谱API响应

        Returns:
            标准AI响应
        """
        try:
            if hasattr(response, 'choices') and response.choices:
                choice = response.choices[0]
                content = choice.message.content if hasattr(choice, 'message') else ""
                finish_reason = getattr(choice, 'finish_reason', 'stop')
            else:
                content = str(response)
                finish_reason = 'stop'

            # 构建使用情况
            usage = {}
            if hasattr(response, 'usage') and response.usage:
                usage = {
                    "prompt_tokens": response.usage.prompt_tokens or 0,
                    "completion_tokens": response.usage.completion_tokens or 0,
                    "total_tokens": response.usage.total_tokens or 0
                }

            return AIResponse(
                content=content,
                role="assistant",
                finish_reason=finish_reason,
                usage=usage,
                metadata={
                    "model": getattr(response, 'model', self.model),
                    "provider": self.provider_name,
                    "timestamp": datetime.now().isoformat()
                }
            )
        except Exception as e:
            self.logger.error(f"转换响应格式失败: {e}")
            return AIResponse(
                content=f"响应解析错误: {str(response)}",
                role="assistant",
                finish_reason="error",
                metadata={"error": str(e)}
            )

    async def chat_completion(self, request: AIRequest) -> AIResponse:
        """
        执行聊天完成

        Args:
            request: AI请求

        Returns:
            AI响应
        """
        import time
        start_time = time.time()

        try:
            self.logger.debug(f"发送智谱API请求: {len(request.messages)} 条消息")

            # 转换请求格式
            zhipu_request = self._convert_request_format(request)

            # 添加请求时间戳用于诊断
            zhipu_request["request_id"] = f"req_{int(start_time)}"

            # 优化的API调用 - 使用更好的异常处理和超时控制
            try:
                # 使用run_in_executor但添加更好的异常处理
                loop = asyncio.get_event_loop()

                # 创建可包装的函数以便更好的错误处理
                def api_call():
                    return self.client.chat.completions.create(**zhipu_request)

                # 执行API调用，保持使用run_in_executor
                response = await loop.run_in_executor(None, api_call)

            except asyncio.TimeoutError:
                self.logger.error(f"智谱API调用超时: {time.time() - start_time:.2f}秒，尝试回退方案")
                # 尝试回退方案 - 直接HTTP调用
                return await self._fallback_direct_http(zhipu_request, start_time)
            except Exception as api_error:
                self.logger.error(f"智谱API调用异常: {api_error}，尝试回退方案")
                # 尝试回退方案 - 直接HTTP调用
                return await self._fallback_direct_http(zhipu_request, start_time)

            # 转换响应格式
            ai_response = self._convert_response_format(response)

            # 添加性能监控信息
            duration = time.time() - start_time
            self.logger.debug(f"智谱API响应: {len(ai_response.content)} 字符，耗时 {duration:.2f} 秒")

            # 添加性能元数据
            ai_response.metadata.update({
                "duration": duration,
                "request_id": zhipu_request.get("request_id"),
                "provider_version": "optimized_v1"
            })

            return ai_response

        except Exception as e:
            self.logger.error(f"智谱API调用失败: {e}")
            return AIResponse(
                content=f"智谱API调用失败: {str(e)}",
                role="assistant",
                finish_reason="error",
                metadata={
                    "error": str(e),
                    "duration": time.time() - start_time
                }
            )

    async def chat_completion_stream(self, request: AIRequest) -> AsyncGenerator[str, None]:
        """
        执行流式聊天完成

        Args:
            request: AI请求

        Yields:
            流式响应片段
        """
        try:
            self.logger.debug(f"发送智谱流式API请求: {len(request.messages)} 条消息")

            # 转换请求格式
            zhipu_request = self._convert_request_format(request)
            zhipu_request["stream"] = True

            # 调用智谱流式API
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.client.chat.completions.create(**zhipu_request)
            )

            # 处理流式响应
            for chunk in response:
                if hasattr(chunk, 'choices') and chunk.choices:
                    delta = chunk.choices[0].delta
                    if hasattr(delta, 'content') and delta.content:
                        yield delta.content

        except Exception as e:
            self.logger.error(f"智谱流式API调用失败: {e}")
            yield f"智谱流式API调用失败: {str(e)}"

    async def _fallback_direct_http(self, zhipu_request: dict, start_time: float) -> AIResponse:
        """
        回退方案：直接HTTP调用智谱API（类似demo脚本的方式）

        Args:
            zhipu_request: 智谱API请求参数
            start_time: 开始时间

        Returns:
            AI响应
        """
        try:
            import httpx
            import json
            import time

            self.logger.info("使用回退方案：直接HTTP调用")

            # 构建HTTP请求
            url = f"{self.base_url}chat/completions"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            # 过滤请求参数，只保留API支持的参数
            api_params = {
                "model": zhipu_request["model"],
                "messages": zhipu_request["messages"],
                "max_tokens": zhipu_request.get("max_tokens", self.max_tokens),
                "temperature": zhipu_request.get("temperature", self.temperature),
                "stream": False
            }

            # 添加可选参数
            if "top_p" in zhipu_request:
                api_params["top_p"] = zhipu_request["top_p"]
            if "stop" in zhipu_request:
                api_params["stop"] = zhipu_request["stop"]

            # 使用异步HTTP客户端
            async with httpx.AsyncClient(
                timeout=httpx.Timeout(timeout=45.0, connect=15.0),
                follow_redirects=True
            ) as client:
                response = await client.post(
                    url,
                    headers=headers,
                    json=api_params
                )

                if response.status_code == 200:
                    data = response.json()
                    if "choices" in data and data["choices"]:
                        content = data["choices"][0]["message"]["content"]
                        usage = data.get("usage", {})

                        self.logger.info(f"回退方案成功，耗时 {time.time() - start_time:.2f} 秒")

                        return AIResponse(
                            content=content,
                            role="assistant",
                            finish_reason="stop",
                            usage={
                                "prompt_tokens": usage.get("prompt_tokens", 0),
                                "completion_tokens": usage.get("completion_tokens", 0),
                                "total_tokens": usage.get("total_tokens", 0)
                            },
                            metadata={
                                "method": "fallback_http",
                                "duration": time.time() - start_time,
                                "request_id": zhipu_request.get("request_id"),
                                "status_code": response.status_code
                            }
                        )
                    else:
                        raise Exception("回退API响应格式错误")
                else:
                    raise Exception(f"回退API错误: {response.status_code} - {response.text}")

        except Exception as e:
            self.logger.error(f"回退方案也失败: {e}")
            return AIResponse(
                content=f"智谱API调用失败（包括回退方案）: {str(e)}",
                role="assistant",
                finish_reason="error",
                metadata={
                    "error": str(e),
                    "method": "fallback_failed",
                    "duration": time.time() - start_time,
                    "request_id": zhipu_request.get("request_id")
                }
            )