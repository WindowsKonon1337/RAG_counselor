import sys
from time import sleep
from configparser import ConfigParser

import chromadb
import uvicorn
from chromadb.utils.embedding_functions import \
    SentenceTransformerEmbeddingFunction

sys.path.insert(1, './utils')
from utils.load_laws_into_db import load_laws_into_db
from utils.question_handler import app, setup_rag_sys


if __name__ == '__main__':
    config = ConfigParser()

    config.read('./rag_service.cfg')

    rag_config = config['RAG']


    client = chromadb.HttpClient(host='chroma')
    embd_model = rag_config['EmbdModel']
    if not client.list_collections():
        load_laws_into_db(
            client,
            embd_model,
            'parse_data',
            '/parsed_data',
            ('admin', 'admin')
        )

    setup_rag_sys(
            client=client,
            embd_model=embd_model,
            TOKEN=rag_config['LLM_TOKEN']
    )

    uvicorn.run(
        app,
        host='0.0.0.0',
        port=1337
    )
