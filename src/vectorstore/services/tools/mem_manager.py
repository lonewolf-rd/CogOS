from src.vectorstore.utils.config_loader import ConfigLoader
from langchain_ollama.chat_models import ChatOllama
from src.vectorstore.utils.logger import AppLogger
from langchain_core.tools import BaseTool
from typing import List, Tuple
from box import Box


class MemoryManager(BaseTool):
