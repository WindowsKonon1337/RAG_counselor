import chromadb
from fastapi import FastAPI


app = FastAPI()

def setup_rag_sys(**kwargs):
    collection = kwargs['collection']
    @app.get('/question')
    def question(q_str: str):
        result = collection.query(
            query_texts=q_str,
            n_results=1
        )

        return result
    return question
