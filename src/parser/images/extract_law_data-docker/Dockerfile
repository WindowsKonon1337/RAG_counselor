FROM python:3.10

COPY . /

RUN python3 -m pip install --upgrade pip  && \
    pip install -r requirements.txt

ENTRYPOINT [ "python3", "extract_law_data.py"]