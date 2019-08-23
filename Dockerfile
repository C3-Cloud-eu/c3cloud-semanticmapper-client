from python:3.7

WORKDIR /app

COPY c3_cloud_client/ /app/c3_cloud_client/
COPY setup.py /app/

RUN python setup.py install




