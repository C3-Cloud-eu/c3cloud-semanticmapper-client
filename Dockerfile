from python:3.7

WORKDIR /app

COPY c3cloud_semanticmapper_client/ /app/c3cloud_semanticmapper_client/
COPY setup.py /app/

RUN python setup.py install




