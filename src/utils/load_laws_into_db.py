import json
import os
from time import sleep
from uuid import uuid4

import chromadb
import chromadb.api
import requests
from chromadb.utils.embedding_functions import \
    SentenceTransformerEmbeddingFunction
from requests import HTTPError


def trigger_dag(airflow_dag, creds):
    trigger_url = f'http://airflow-webserver:8080/api/v1/dags/{airflow_dag}/dagRuns'

    data = {
        'dag_run_id': str(uuid4())
    }

    headers = {
        'Content-type': 'application/json'
    }

    response = requests.post(
        trigger_url,
        headers=headers,
        data=json.dumps(data),
        auth=creds
    )

    return response.status_code

def check_dag_status(airflow_dag, creds):
    trigger_url = f'http://airflow-webserver:8080/api/v1/dags/{airflow_dag}/dagRuns'

    data = {
        'dag_run_id': str(uuid4())
    }

    headers = {
        'Content-type': 'application/json'
    }

    response = requests.get(
        trigger_url,
        data=data,
        auth=creds,
        headers=headers
    )

    dag_runs = json.loads(response.text)['dag_runs']

    newest_dag_run = sorted(
        dag_runs,
        key= lambda x: x['start_date'],
        reverse=True
    )[0]

    return newest_dag_run['state']



def get_newest_law_data(data_path):
    return sorted(
        os.listdir(
            os.path.join(
                data_path,
                'law_jsons'
            )
        ),
        key=lambda x: x,
        reverse=True
    )[0]


def load_laws_into_db(
        chroma_client: chromadb.api.ClientAPI,
        chroma_collection_name: str,
        embd_model: str,
        airflow_dag,
        data_volume_path: str,
        airflow_creds: tuple
    ):

    if not os.listdir(data_volume_path):
        status = trigger_dag(
            airflow_dag,
            airflow_creds
        )

        if status != 200:
            raise HTTPError(f'Error with trigger dag {airflow_dag}. \
                            status code: {status}')

        while check_dag_status(
            airflow_dag,
            airflow_creds
        ) != 'success':
            sleep(15)

    collection = chroma_client.get_collection(
        chroma_collection_name,
        embedding_function=SentenceTransformerEmbeddingFunction(embd_model)
    )


    newest_data_path = os.path.join(
        data_volume_path,
        'law_jsons',
        get_newest_law_data(data_volume_path)
    )

    with open(newest_data_path, encoding='cp1251') as f:
        for line in f:
            json_law = json.loads(line.strip())

            law_norm, law_text = list(json_law.items())[0]

            collection.add(
                documents=law_text,
                metadatas=[{'law_norm': law_norm}] * len(law_text),
                ids=[str(uuid4()) for _ in range(len(law_text))]
            )
