FROM python:3.10

COPY . /

RUN python3 -m pip install --upgrade pip  && \
    pip install -r requirements.txt

# CMD ["bash"]

ENTRYPOINT [ "python3", "get_actual_links.py"]
