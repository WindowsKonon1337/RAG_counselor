import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from fastapi import FastAPI
from utils import load_laws_into_db


app = FastAPI()

@app.get('/question')
def question(q_str: str):
    pass


if __name__ == '__main__':
    client = chromadb.HttpClient(port=8000)

    collection_list = client.list_collections()

    if 'koap-rf' not in collection_list:
        client.create_collection(
            name='koap-rf',
            embedding_function=SentenceTransformerEmbeddingFunction('sentence-transformers/sentence-t5-large')
        )
        # trigger airflow DAG
    
    koaprf_collection = client.get_collection('koap-rf')