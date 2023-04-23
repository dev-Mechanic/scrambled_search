FROM python:3.9.16-slim

WORKDIR /opt/
COPY scramble_search.py .

ENTRYPOINT ["python","scramble_search.py","--dictionary=/opt/dictionary.txt","--input=/opt/input.txt"]