import os
import chromadb
from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings

mcp = FastMCP(
    name="knowledge-rag-mcp",
    instructions="Search for coverage details in policy documents.",
    host="0.0.0.0",
    port=int(os.getenv("PORT", 8085)),
    transport_security=TransportSecuritySettings(enable_dns_rebinding_protection=False),
)

# Path to policies folder (copied into the directory)
policies_dir = os.path.join(os.path.dirname(__file__), "policies")
db_path = os.path.join(os.path.dirname(__file__), "chroma_db")

# Initialize ChromaDB
client = chromadb.PersistentClient(path=db_path)
collection = client.get_or_create_collection(name="insurance_policies")

def initialize_db():
    if collection.count() > 0:
        return
        
    if not os.path.exists(policies_dir):
        print(f"No policy documents found at {policies_dir}.")
        return
        
    documents = []
    metadatas = []
    ids = []
    
    for filename in os.listdir(policies_dir):
        if filename.endswith(".txt"):
            filepath = os.path.join(policies_dir, filename)
            with open(filepath, 'r') as f:
                content = f.read()
            
            documents.append(content)
            metadatas.append({"filename": filename})
            ids.append(filename)
            
    if documents:
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        print(f"Added {len(documents)} documents to ChromaDB.")

# Initialize on start
initialize_db()

@mcp.tool()
def search_policies(query: str) -> dict:
    """Search for relevant policy documents using ChromaDB.

    Args:
        query: The search query (e.g., "dental coverage").

    Returns:
        Dict with status and results.
    """
    try:
        results = collection.query(
            query_texts=[query],
            n_results=2
        )
        
        relevant_docs = []
        if results['documents']:
            for doc_list in results['documents']:
                for doc in doc_list:
                    relevant_docs.append(doc)
                    
        return {
            "status": "success", 
            "results": "\n\n".join(relevant_docs) if relevant_docs else "No relevant policies found."
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
