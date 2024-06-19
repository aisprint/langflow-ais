from typing import List

import weaviate
from langchain_community.vectorstores import Weaviate

from langflow.base.vectorstores.model import LCVectorStoreComponent
from langflow.helpers.data import docs_to_data
from langflow.io import BoolInput, HandleInput, IntInput, StrInput, SecretStrInput, DataInput
from langflow.schema import Data


class WeaviateVectorStoreComponent(LCVectorStoreComponent):
    display_name = "Weaviate"
    description = "Weaviate Vector Store with search capabilities"
    documentation = "https://python.langchain.com/docs/modules/data_connection/vectorstores/integrations/weaviate"
    icon = "Weaviate"

    inputs = [
        StrInput(name="url", display_name="Weaviate URL", value="http://localhost:8080", required=True),
        SecretStrInput(name="api_key", display_name="API Key", required=False),
        StrInput(name="index_name", display_name="Index Name", required=True),
        StrInput(name="text_key", display_name="Text Key", value="text", advanced=True),
        HandleInput(name="embedding", display_name="Embedding", input_types=["Embeddings"]),
        DataInput(
            name="vector_store_inputs",
            display_name="Vector Store Inputs",
            is_list=True,
        ),
        BoolInput(
            name="add_to_vector_store",
            display_name="Add to Vector Store",
            info="If true, the Vector Store Inputs will be added to the Vector Store.",
        ),
        StrInput(name="search_input", display_name="Search Input"),
        IntInput(
            name="number_of_results",
            display_name="Number of Results",
            info="Number of results to return.",
            value=4,
            advanced=True,
        ),
        BoolInput(name="search_by_text", display_name="Search By Text", advanced=True),
    ]

    def build_vector_store(self) -> Weaviate:
        return self._build_weaviate()

    def _build_weaviate(self) -> Weaviate:
        if self.api_key:
            auth_config = weaviate.AuthApiKey(api_key=self.api_key)
            client = weaviate.Client(url=self.url, auth_client_secret=auth_config)
        else:
            client = weaviate.Client(url=self.url)

        if self.add_to_vector_store:
            documents = []
            for _input in self.vector_store_inputs or []:
                if isinstance(_input, Data):
                    documents.append(_input.to_lc_document())
                else:
                    documents.append(_input)

            if documents and self.embedding:
                return Weaviate.from_documents(
                    client=client,
                    index_name=self.index_name,
                    documents=documents,
                    embedding=self.embedding,
                    by_text=self.search_by_text,
                )

        return Weaviate(
            client=client,
            index_name=self.index_name,
            text_key=self.text_key,
            embedding=self.embedding,
            by_text=self.search_by_text,
        )

    def search_documents(self) -> List[Data]:
        vector_store = self._build_weaviate()

        if self.search_input and isinstance(self.search_input, str) and self.search_input.strip():
            docs = vector_store.similarity_search(
                query=self.search_input,
                k=self.number_of_results,
            )

            data = docs_to_data(docs)
            self.status = data
            return data
        else:
            return []
