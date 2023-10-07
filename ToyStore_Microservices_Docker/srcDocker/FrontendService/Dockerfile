FROM python:3.8-alpine

RUN pip install sockets
WORKDIR /app

RUN mkdir -p /app/data

#COPY ["data/toyStoreData.json", "data/orderlog.csv", ".data/"]
 
COPY ["frontendservice.py","./"]


ENTRYPOINT [ "python", "frontendservice.py"]
