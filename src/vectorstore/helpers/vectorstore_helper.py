from langchain_community.docstore.in_memory import InMemoryDocstore
from source.backend.utils.config_loader import ConfigLoader
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from source.backend.utils.logger import AppLogger
from langchain_core.documents import Document
from vectorstore_helper import IndexFlatL2
from pathlib import Path
from typing import Union
from box import Box
import os.path


class FaissVS:

    def __init__(self):
        self.vectorstore: Union[FAISS, None] = None

        self.vectorstore_path = f"{Path(__file__).parent.parent}/faiss"
        self.config_loader = ConfigLoader()
        self.logger = AppLogger()
        self.secret_loader = Box(self.config_loader.load_config("secret_configs"))
        self.embedding_model = OllamaEmbeddings(
            model=self.secret_loader.ollama.embedding_model,
            base_url=self.secret_loader.ollama.url
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
            self.logger.info(f"[FaissVS](_init_vs) Vectorstore has been loaded sucessfully...")
            pass

    async def _update_tool_memory(
            self,
            tool_name: str,
            update_topic: str,
            content: str
    ) -> None:
        index_cod = Document(page_content=content)
        await self.vectorstore.aadd_documents()
