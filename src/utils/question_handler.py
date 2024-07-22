from fastapi import FastAPI
from chromadb.utils.embedding_functions import \
    SentenceTransformerEmbeddingFunction
from torch.cuda import is_available
import json
import requests
import sys

sys.path.insert(1, './prompt_templates')

from prompt_templates.get_classify_chapter_prompt import configure_classify_chapter_prompt
from prompt_templates.get_final_answer import configure_final_answer_prompt

app = FastAPI()


def setup_rag_sys(**kwargs):
    client = kwargs['client']
    embd_model = kwargs['embd_model']

    collection_dict = dict()

    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': f'Bearer {kwargs["TOKEN"]}'
    }

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
    def question(q_str: str):

        class_payload = json.dumps({
            "model": "GigaChat",
            "messages": [
                {
                "role": "system",
                "content": configure_classify_chapter_prompt(q_str)
                }
            ],
            "stream": False,
            "repetition_penalty": 1
        })

        class_response = requests.request(
            "POST",
            url,
            headers=headers,
            data=class_payload,
            verify=False
        )

        chapter_num = json.loads(
            class_response.text
        )['choices'][0]['message']['content']

        relevant_docs = collection_dict[chapter_num].query(
            query_texts=q_str,
            n_results=7
        )

        compiled_texts = []
        for label, doc in zip(
            relevant_docs['metadatas'][0],
            relevant_docs['documents'][0]
            ):
            compiled_texts.append(
                label['law_norm'] + '\n' + doc
            )

        full_text = '\n\n'.join(compiled_texts)

        class_payload = json.dumps({
            "model": "GigaChat",
            "messages": [
                {
                "role": "system",
                "content": configure_final_answer_prompt(full_text, q_str)
                }
            ],
            "stream": False,
            "repetition_penalty": 1
        })

        result = requests.request(
            "POST",
            url,
            headers=headers,
            data=class_payload,
            verify=False
        )

        return json.loads(result.text)\
            ['choices'][0]['message']['content']
    return question


@app.get('/check_service')
def check_service():
    return {'status': 'running'}
