FROM python:3.8-alpine

WORKDIR /app

RUN pip install sockets

RUN mkdir -p /app/data

#COPY ["../data/toyStoreData.json", "./data/"]
 
COPY ["catalog.py", "./"]

ENTRYPOINT [ "python", "catalog.py"]
