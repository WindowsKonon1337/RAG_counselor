from datetime import datetime, timedelta
from time import gmtime, strftime

from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount


with DAG(
    'parse_data',
    schedule_interval='0 0 1 */3 *',
    start_date=datetime.strptime(strftime('%Y-%m-%d', gmtime()), '%Y-%m-%d'),
    default_args= {
        'owner': 'WindowsKonon1337',
        'retries': 3,
        "retry_delay": timedelta(hours=1),
    },
    dagrun_timeout= timedelta(minutes=10)
) as dag:
    get_links = DockerOperator(
        image="airflow-actual_links",
        command='--output_file /opt/airflow/data/links/{{ ds }}.json',
        network_mode="host",
        task_id="docker-airflow-get_koaprf-act-links",
        do_xcom_push=False,
        auto_remove=True,
        docker_url='unix://var/run/docker.sock',
        mounts=[
            Mount(source='rag_counselor_parse_data', target='/opt/airflow/data/', type='volume')
        ]
    )

    extract_law_data = DockerOperator(
        image='airflow-extract_data',
        command='--raw_law_links /opt/airflow/data/links/{{ ds }} --output_file /opt/airflow/data/law_jsons/{{ ds }}.json',
        network_mode="host",
        task_id="docker-airflow-extract_law_from-act-links",
        do_xcom_push=False,
        auto_remove=True,
        docker_url='unix://var/run/docker.sock',
        mounts=[
            Mount(source='rag_counselor_parse_data', target='/opt/airflow/data/', type='volume')
        ]
    )

    get_links >> extract_law_data
