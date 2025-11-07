from langchain_community.docstore.in_memory import InMemoryDocstore
from src.vectorstore.utils.config_manager import ConfigManager
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from src.vectorstore.utils.logger import AppLogger
from langchain_core.documents import Document
from faiss import IndexFlatL2
from pathlib import Path
from typing import Union
import os.path


class VSHelper:

    def __init__(self):
        self.vectorstore: Union[FAISS, None] = None
        self.vectorstore_path: str = f"{Path(__file__).parent.parent}/faiss"

        self.logger = AppLogger()
        self.configs = ConfigManager().cfg
        self.embedding_model = OllamaEmbeddings(
            model=self.configs.ollama_configs.ollama.model_name,
            base_url=self.configs.ollama_configs.ollama.base_url
        )
        self._init_vs()

    def _init_vs(self):
        if not os.path.exists(self.vectorstore_path):
            embedding_dimension = len(self.embedding_model.embed_query("dummy"))
            self.logger.info(f"[FaissVS](_init_vs) Vectorstore is being initialized...")
            self.vectorstore = FAISS(
                embedding_function=self.embedding_model,
                index=IndexFlatL2(embedding_dimension),
                docstore=InMemoryDocstore(),
                index_to_docstore_id={},
                normalize_L2=False
            )
            self.logger.info(f"[FaissVS](_init_vs) Vectorstore has been created successfully...")
        else:
            self.logger.info(f"[FaissVS](_init_vs) Vectorstore already exists...")
            self.vectorstore = FAISS.load_local(
                folder_path=self.vectorstore_path,
                embeddings=self.embedding_model,
                allow_dangerous_deserialization=True
            )
            self.logger.info(f"[FaissVS](_init_vs) Vectorstore has been loaded successfully...")
            pass
