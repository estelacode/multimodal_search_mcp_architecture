import asyncio
import chromadb
from chromadb.utils.embedding_functions import OpenCLIPEmbeddingFunction
from chromadb.utils.data_loaders import ImageLoader


# async def main():
 
#     client = await chromadb.AsyncHttpClient(host='localhost', port=8000)

#     collection = await client.get_collection(name="men_shoes")
#     count = await collection.count()
#     print(f"✅ Collection 'men_shoes' loaded. Embeddings: {count}")

# asyncio.run(main())


def main():
    embedding_function = OpenCLIPEmbeddingFunction()
    image_loader = ImageLoader()
   
          
    client = chromadb.HttpClient(host='localhost', port=8000)

    collection = client.get_collection(name="men_shoes", embedding_function=embedding_function, data_loader=image_loader)
    count = collection.count()
    print(f"✅ Collection 'men_shoes' loaded. Embeddings: {count}")
    
    result = collection.query(query_texts=['Military Boots'], include=['data', 'metadatas'], n_results=1)
    print("✅ Query Results:", result)
if __name__ == "__main__":
    main()

#chroma run --path C:/Users/emada/Desktop/ia_workspace/multimodal_search_mcp_architecture/chroma_db