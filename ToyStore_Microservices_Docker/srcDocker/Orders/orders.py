import os
import csv
from concurrent.futures import ThreadPoolExecutor
import threading
import socket
import json

# This stores the last order_number from the csv file
globalOrderNumber = 0

def processRequest(c, lock) :
    global globalOrderNumber

    # Receiving the request from frontend service
    data = c.recv(1024)

    # Making a connection to the catalog and sending the request we got from the frontend
    catalog = socket.socket()
    catalog_host = os.getenv("CATALOG_HOST", "srcdocker_catalog_1")
    port = 9001
    catalog.connect((catalog_host, port))
    catalog.send(data)
    message = catalog.recv(1024)
    catalog.close()

    # Formatting the message from the catalog as a dictionary
    message = json.loads(message)

    # Getting data from the message sent by the frontend service
    dataFromFrontEnd = json.loads(data)
    name = dataFromFrontEnd.get("name")
    quantity = dataFromFrontEnd.get("quantity")

    # Building the response that needs to be sent to the frontend service
    resp = {}

    # Processing the response based on the reply we heard from catalog
    if message.get("code") == 1:
        resp["code"] = 1

        # Making sure that shared memory variables and files are read and modified
        # by one thread at a time
        lock.acquire()

        # Incrementing globalOrderNumber
        globalOrderNumber +=1

        # Adding data to the log
        with open('../data/orderlog.csv', 'a+', newline='') as orderlog:
            header_key = ['order_no', 'Product', 'quantity']
            value = csv.DictWriter(orderlog, fieldnames=header_key)
            value.writerow({'order_no': globalOrderNumber, 'Product': name,
                            'quantity': quantity})
        orderlog.close()

        resp["order_number"] = globalOrderNumber
        lock.release()
    else:

        # If the request failed, send the error code and message
        # to the frontend service
        resp["code"] = message.get("code")
        resp["message"] = message.get("message")

    # Sending the response to frontend service
    c.send(json.dumps(resp).encode('utf-8'))
    c.close()
    print('Request is processed')
def run():
    host = "0.0.0.0"
    port = 9000

    # Bind the socket to the host and port
    s = socket.socket()
    s.bind((host, port))
    print("socket catalog binded to port", port)

    # put the socket into listening mode
    s.listen(5)
    print("socket catalog is listening")

    # create a threadpool
    executor = ThreadPoolExecutor(max_workers=10)

    # Creating a lock object to pass it to the threads inorder to protect the critical region
    lock = threading.Lock()

    while True:

        # Accept requests from the frontend service
        c, addr = s.accept()
        print("Connected to :", addr[0], ":", addr[1])

        # Assign a thread to process the request
        executor.submit(processRequest, c, lock)
if __name__ == '__main__':

    # Reading the orders log and get last order number
    with open('../data/orderlog.csv', 'r') as f:
        for line in f:
            pass
        last_line = line
        print(last_line.split(',')[0])
    f.close()

    # Initializing globalOrderNumber with the latest order number
    if (last_line.split(',')[0]) == 'order_no':
        globalOrderNumber = 0
    else :
        globalOrderNumber = int(last_line.split(',')[0])
    run()