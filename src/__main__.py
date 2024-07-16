import sys
from time import sleep
from argparse import ArgumentParser

import chromadb
import uvicorn
from chromadb.utils.embedding_functions import \
    SentenceTransformerEmbeddingFunction

sys.path.insert(1, './utils')
from utils.load_laws_into_db import load_laws_into_db
from utils.question_handler import app, setup_rag_sys


if __name__ == '__main__':

    client = chromadb.HttpClient(host='chroma')
    embd_model = 'sentence-transformers/sentence-t5-large'

    print('CONNECTED')

    name_collection_list = list(
        map(
            lambda x: x.name,
            client.list_collections()
        )
    )

    if 'koap-rf' not in name_collection_list:
        client.create_collection(
            name='koap-rf',
            embedding_function=SentenceTransformerEmbeddingFunction(embd_model)
        )

        load_laws_into_db(
            client,
            'koap-rf',
            embd_model,
            'parse_data',
            '/parsed_data',
            ('admin', 'admin')
        )
    
    # koaprf_collection = client.get_collection(
    #     'koap-rf',
    #     embedding_function=SentenceTransformerEmbeddingFunction(embd_model)
    # )

    # setup_rag_sys(
    #     {
    #         'collection': koaprf_collection
    #     }
    # )

    # uvicorn.run(
    #     app,
    #     host='0.0.0.0',
    #     port=1337
    # )
