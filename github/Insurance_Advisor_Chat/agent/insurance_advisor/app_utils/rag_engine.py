import os
import chromadb

# Path to data/policies relative to this file
# __file__ is insurance_advisor/insurance_advisor/app_utils/rag_engine.py
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
policies_dir = os.path.join(project_root, "data", "policies")
db_path = os.path.join(project_root, "data", "chroma_db")

# Initialize ChromaDB
# Persistent client saves data to disk
client = chromadb.PersistentClient(path=db_path)

# Create or get collection
collection = client.get_or_create_collection(name="insurance_policies")

def initialize_db():
    """Load policy documents into ChromaDB if collection is empty."""
    # We check count to avoid re-adding on every reload
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

# Initialize on import
initialize_db()

def search_policies(query: str) -> dict:
    """Search for relevant policy documents using ChromaDB."""
    try:
        results = collection.query(
            query_texts=[query],
            n_results=2 # Return top 2 results
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
