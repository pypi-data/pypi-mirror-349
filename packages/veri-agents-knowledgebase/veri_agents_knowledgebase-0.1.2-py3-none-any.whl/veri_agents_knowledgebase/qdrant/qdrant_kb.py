import logging
from typing import AsyncGenerator, Iterator

import cachetools.func
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_qdrant import FastEmbedSparse, QdrantVectorStore, RetrievalMode
from qdrant_client import QdrantClient, models
from qdrant_client.models import Filter
from qdrant_client.models import Distance, VectorParams
from veri_agents_knowledgebase.knowledgebase import Knowledgebase, KnowledgeFilter, and_filters
from veri_agents_knowledgebase.qdrant.qdrant_doc_store import QdrantDocStore

log = logging.getLogger(__name__)


class QdrantKnowledgebase(Knowledgebase):
    def __init__(
        self,
        vectordb_url: str,
        embedding_model: Embeddings,
        filter: KnowledgeFilter | None = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.chunks_collection_name = f"chunks_{self.metadata.collection}"
        self.docs_collection_name = f"docs_{self.metadata.collection}"
        self.filter = filter

        self.embedding_model = embedding_model

        log.info(f"Connecting to Qdrant at {vectordb_url}")
        self.qdrant = QdrantClient(vectordb_url)
        self._init_collection()
        sparse_embeddings = FastEmbedSparse(model_name="Qdrant/bm25")
        self.vector_store = QdrantVectorStore(
            client=self.qdrant,
            collection_name=self.chunks_collection_name,
            # FIXME
            embedding=self.embedding_model,# pyright: ignore[reportArgumentType]
            retrieval_mode=RetrievalMode.HYBRID,
            vector_name="dense",
            sparse_embedding=sparse_embeddings,
            sparse_vector_name="sparse",
        )
        self.doc_store = QdrantDocStore(
            client=self.qdrant, collection_name=self.docs_collection_name
        )
        self.doc_store.create_schema()

    def _init_collection(self):
        if not self.qdrant.collection_exists(self.chunks_collection_name):
            self.qdrant.create_collection(
                self.chunks_collection_name,
                vectors_config={
                    "dense": VectorParams(
                        size=1024, distance=Distance.COSINE
                    )  # TODO get size from somewhere
                },
                sparse_vectors_config={
                    "sparse": models.SparseVectorParams(),
                },
            )

    @cachetools.func.ttl_cache(maxsize=1, ttl=360)
    def _load_tags(self):
        """Load tags from the documents in the knowledge base."""
        tags = self.metadata.tags
        for doc in self.doc_store.yield_documents():
            if doc.metadata and "tags" in doc.metadata:
                doc_tags = doc.metadata["tags"]
                if isinstance(doc_tags, str):
                    doc_tags = [doc_tags]
                for doc_tag in doc_tags:
                    if doc_tag not in tags:
                        tags[doc_tag] = ""
        return tags 

    @property
    def tags(self):
        """Get the tags for the workflow."""
        return self._load_tags()

    def retrieve(
        self,
        query: str,
        limit: int,
        filter: KnowledgeFilter | None = None,
        **kwargs,
    ) -> tuple[str | None, list[Document] | None]:
        # for now let's do naive retrieval
        qdrant_filter = self._create_qdrant_filter(and_filters(filter, self.filter))
        log.info(f"Qdrant Filter: {qdrant_filter}")
        return None, self.vector_store.similarity_search(query, k=limit, filter=qdrant_filter)

    def get_documents(
        self,
        filter: KnowledgeFilter | None = None,
    ) -> Iterator[Document]:
        qdrant_filter = self._create_qdrant_filter(and_filters(filter, self.filter))
        return self.doc_store.yield_documents(filter=qdrant_filter)

    async def aget_documents(
        self,
        filter: KnowledgeFilter | None = None,
    ) -> AsyncGenerator[Document, None]:
        """Get all documents from the knowledge base."""
        qdrant_filter = self._create_qdrant_filter(filter)
        for doc in self.doc_store.yield_documents(filter=qdrant_filter):
            yield doc

    def _create_qdrant_filter(
        self,
        filter: KnowledgeFilter | None = None,
    ):
        """Create a Qdrant filter from the knowledgebase filter.
        Args:
            filter (KnowledgeFilter): The knowledge filter to convert.
        Returns:
            Filter: The Qdrant filter.
        """
        if not filter:
            return None

        must = []
        # doc filter means all the documents in the list (so a should clause)
        if filter.docs:
            doc_filter = filter.docs
            if isinstance(filter.docs, str):
                doc_filter = [filter.docs]
            should = []
            for doc_id in doc_filter:
                should.append(
                    models.FieldCondition(
                        key="metadata.source", match=models.MatchValue(value=doc_id)
                    )
                )
            must.append(Filter(should=should))
        if filter.tags_any_of:
            tag_any_filter = filter.tags_any_of
            if isinstance(filter.tags_any_of, str):
                tag_any_filter = [filter.tags_any_of]
            should = []
            for tag in tag_any_filter:
                should.append(
                    models.FieldCondition(
                        key="metadata.tags",
                        match=models.MatchValue(value=tag),
                    )
                )
            must.append(Filter(should=should))
        if filter.tags_all_of:
            tag_all_filter = filter.tags_all_of
            if isinstance(filter.tags_all_of, str):
                tag_all_filter = [filter.tags_all_of]
            for tag in tag_all_filter:
                must.append(
                    models.FieldCondition(
                        key="metadata.tags",
                        match=models.MatchValue(value=tag),
                    )
                )
        return Filter(must=must) if must else None
