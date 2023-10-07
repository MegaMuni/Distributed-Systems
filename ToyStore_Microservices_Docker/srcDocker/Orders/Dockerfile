FROM python:3.8-alpine

RUN pip install sockets
WORKDIR /app

RUN mkdir -p /app/data

#COPY ["lab2-spring22-SUSMITA_MUNI/srcDocker/data/orderlog.csv", "./data/"]
 
COPY ["orders.py", "./"]


ENTRYPOINT [ "python", "orders.py"]
