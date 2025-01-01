from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

from typing import Optional
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from typing import Any

class GenericLLMIndex:
    def __init__(
        self,
        llm_provider: str,
        model_name: str,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None
    ):
        self.llm = self._initialize_llm(llm_provider, model_name, api_key, base_url)
        self.embed_model = self._initialize_embeddings(llm_provider, model_name)

    def _initialize_llm(self, provider: str, model: str, api_key: Optional[str], base_url: Optional[str]) -> Any:
        if provider == "ollama":
            from llama_index.llms.ollama import Ollama
            return Ollama(model=model, base_url=base_url or "http://localhost:11434")
        ## we can extend

        raise ValueError(f"Unsupported provider: {provider}")

    def _initialize_embeddings(self, provider: str, model: str):
        if provider == "ollama":
            return HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")



    def create_index(self, data_path: str):
        documents = SimpleDirectoryReader(data_path).load_data()
        return VectorStoreIndex.from_documents(
            documents,
            llm=self.llm,
            embed_model=self.embed_model
        )
