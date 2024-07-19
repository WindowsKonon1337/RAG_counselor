from fastapi import FastAPI
from chromadb.utils.embedding_functions import \
    SentenceTransformerEmbeddingFunction
from torch.cuda import is_available

app = FastAPI()


def setup_rag_sys(**kwargs):
    client = kwargs['client']
    embd_model = kwargs['embd_model']

    collection_dict = dict()

    for i in range(5, 22):
        collection_dict[str(i)] = \
            client.get_collection(
                f'chapter_{i}_koap-rf',
                embedding_function = \
                    SentenceTransformerEmbeddingFunction(
                        embd_model,
                        device='cuda' if is_available() else 'cpu'
                    )
            )

    @app.get('/question')
    def question(q_str: str, chapter_num):
        result = collection_dict[str(chapter_num)].query(
            query_texts=q_str,
            n_results=5
        )

        return result
    return question


@app.get('/check_service')
def check_service():
    return {'status': 'running'}
