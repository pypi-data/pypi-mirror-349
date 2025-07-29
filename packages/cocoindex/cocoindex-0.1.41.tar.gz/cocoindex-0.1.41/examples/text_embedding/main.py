import os
from dotenv import load_dotenv
from psycopg_pool import ConnectionPool

import cocoindex

@cocoindex.transform_flow()
def text_to_embedding(text: cocoindex.DataSlice[str]) -> cocoindex.DataSlice[list[float]]:
    """
    Embed the text using a SentenceTransformer model.
    This is a shared logic between indexing and querying, so extract it as a function.
    """
    return text.transform(
        cocoindex.functions.SentenceTransformerEmbed(
            model="sentence-transformers/all-MiniLM-L6-v2"))

@cocoindex.flow_def(name="TextEmbedding")
def text_embedding_flow(flow_builder: cocoindex.FlowBuilder, data_scope: cocoindex.DataScope):
    """
    Define an example flow that embeds text into a vector database.
    """
    data_scope["documents"] = flow_builder.add_source(
        cocoindex.sources.LocalFile(path="markdown_files", included_patterns=["*.md"]))

    doc_embeddings = data_scope.add_collector()

    with data_scope["documents"].row() as doc:
        doc["chunks"] = doc["content"].transform(
            cocoindex.functions.SplitRecursively(),
            language="markdown", chunk_size=2000, chunk_overlap=500)

        with doc["chunks"].row() as chunk:
            chunk["embedding"] = text_to_embedding(chunk["text"])
            doc_embeddings.collect(filename=doc["filename"], location=chunk["location"],
                                   text=chunk["text"], embedding=chunk["embedding"])

    doc_embeddings.export(
        "doc_embeddings",
        cocoindex.storages.Postgres(),
        primary_key_fields=["filename", "location"],
        vector_indexes=[
            cocoindex.VectorIndexDef(
                field_name="embedding",
                metric=cocoindex.VectorSimilarityMetric.COSINE_SIMILARITY)])

# Keep for now to allow CocoInsight to query.
# Will be removed later after we expose `search()` below as a query function (https://github.com/cocoindex-io/cocoindex/issues/502).
cocoindex.query.SimpleSemanticsQueryHandler(
    name="SemanticsSearch",
    flow=text_embedding_flow,
    target_name="doc_embeddings",
    query_transform_flow=text_to_embedding,
    default_similarity_metric=cocoindex.VectorSimilarityMetric.COSINE_SIMILARITY)

def search(pool: ConnectionPool, query: str, top_k: int = 5):
    table_name = cocoindex.utils.get_target_storage_default_name(text_embedding_flow, "doc_embeddings")
    query_vector = text_to_embedding.eval(query)
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(f"""
                SELECT filename, location, text, embedding <=> %s::vector AS distance
                FROM {table_name}
                ORDER BY distance
                LIMIT %s
            """, (query_vector, top_k))
            return [
                {"filename": row[0], "location": row[1], "text": row[2], "score": 1.0 - row[3]}
                for row in cur.fetchall()
            ]

@cocoindex.main_fn()
def _run():
    pool = ConnectionPool(os.getenv("COCOINDEX_DATABASE_URL"))
    # Run queries in a loop to demonstrate the query capabilities.
    while True:
        try:
            query = input("Enter search query (or Enter to quit): ")
            if query == '':
                break
            results = search(pool, query)
            print("\nSearch results:")
            for result in results:
                print(f"[{result['score']:.3f}] {result['filename']} location:{result['location']}")
                print(f"    {result['text']}")
                print("---")
            print()
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    load_dotenv(override=True)
    _run()
