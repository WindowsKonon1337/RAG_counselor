FROM python:3.10

WORKDIR /app

COPY ./requirements.txt *.py utils prompt_templates /app/

RUN pip install -r requirements.txt

CMD [ "python3", "./__main__.py" ]