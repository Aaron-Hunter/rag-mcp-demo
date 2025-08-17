from typing import Any
import chromadb
import os
import httpx
from sentence_transformers import SentenceTransformer
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("rag")

@mcp.tool()
def rag(query: str) -> str:
    current_dir = os.getcwd()
    model = SentenceTransformer("prdev/mini-gte")
    client = chromadb.PersistentClient(path=f"{current_dir}/db")
    collection = client.get_or_create_collection("rag_docs")

    query_embedding = model.encode([query])[0]
    response = collection.query(query_embeddings=[query_embedding], n_results=5)
    results = response["documents"][0]
    context = "\n---\n".join(results)
    return context

if __name__ == "__main__":
    mcp.run(transport='stdio')