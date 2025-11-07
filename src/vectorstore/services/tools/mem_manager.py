from langchain_core.runnables import RunnableSequence, RunnableSerializable
from src.vectorstore.services.output_parsers import EntityExtractor
from src.vectorstore.helpers.vectorstore_helper import VSHelper
from src.vectorstore.utils.config_manager import ConfigManager
from langchain_ollama.chat_models import ChatOllama
from langchain_core.prompts import PromptTemplate
from src.vectorstore.utils.logger import AppLogger
from langchain_core.tools import BaseTool
from typing import List, Tuple, Union
from box import Box
import mlflow


class MemoryManager(BaseTool):
    name: str = "MemoryManager"
    description: str = "Tool for deciding whether existing memory (either long-term or entity) should be updated"

    class Config:
        extra = "allow"

    def __init__(self):
        super().__init__()
        self.sys_prompt: Union[None, PromptTemplate] = None
        self.llm: Union[None, ChatOllama] = None
        self.tool_chain: Union[None, RunnableSequence, RunnableSerializable] = None

        self.logger = AppLogger()
        self.vs_helper = VSHelper()
        self.config_loader = ConfigManager().cfg
        self._init_system_prompt()
        self._init_llm()

    def _init_system_prompt(self) -> None:
        try:
            self.sys_prompt = PromptTemplate(
                template=self.config_loader.system_prompts.memory_manager.sys_prompt,
                input_variables=[""]
            )
            self.logger.info("[MemoryManager](_init_system_prompt) Memory Manager Prompt Loaded")
        except Exception as initialization_error:
            self.logger.error(f"[MemoryManager](_init_system_prompt) Prompt Not Loaded:\n{initialization_error}")
            raise initialization_error

    def _init_llm(self) -> None:
        try:
            self.llm = ChatOllama(
                base_url=self.config_loader.ollama_configs.ollama.url,
                model=self.config_loader.ollama_configs.ollama.model_name,
                temperature=self.config_loader.ollama_configs.ollama.temp,
                num_predict=self.config_loader.ollama_configs.ollama.maxct,
                num_gpu=1
            )
            self.logger.info("[MemoryManager](_init_llm) Memory Manager LLM Loaded")
        except Exception as initialization_error:
            self.logger.error(f"[MemoryManager](_init_llm) Model Not Loaded :\n{initialization_error}")
            raise initialization_error
