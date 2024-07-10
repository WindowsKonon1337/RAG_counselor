import chromadb
from chromadb.utils import embedding_functions
from fastapi import FastAPI


app = FastAPI()

@app.get('/question')
def question(q_str: str):
    pass


if __name__ == '__main__':
    client = chromadb.HttpClient(port=8000)

    collection_list = client.list_collections()

    if 'koap-rf' not in collection_list:
        client.create_collection('koap-rf')
        # parse data
        # insert into db
    
    koaprf_collection = client.get_collection('koap-rf')