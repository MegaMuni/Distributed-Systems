import random
import socket
import json
import threading
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import wait
import time
import sys


class onlyQueryRequests:

    def __init__(self, numOfClients, hostName):
        self.numOfClients = numOfClients
        self.requestLatencyArray = []
        self.averageLatency = 0
        self.hostName = hostName

    def threadingClient(self, lock):
        host = self.hostName
        port = 8000
        frontendservice = socket.socket()
        frontendservice.connect((host, port))
        iter = 0
        numberOfRequests = 0
        latency = 0

        # This loop runs for 100 iterations
        while True:
            items = ['Tux', 'Whale', 'Elephant', 'Bird']

            # Forming random GET request
            randomItem = random.randint(0, 3)
            getRequest = 'GET /products?product_name=' + items[randomItem] + ' HTTP/1.1\r\n'

            start = time.time()
            frontendservice.send(getRequest.encode('utf-8'))
            r = frontendservice.recv(1024)
            end = time.time()

            # Evaluating latency
            latency += (end - start)
            numberOfRequests += 1
            r = json.loads(r.decode('utf-8').split('\n')[4])
            print("GET Request Response: " + json.dumps(r))
            iter += 1
            if iter == 100:
                break

        avaerageLatency = latency / numberOfRequests

        # Locking since we have threads modifying shared resource space
        lock.acquire()
        self.requestLatencyArray.append(avaerageLatency * 1000)
        lock.release()
        frontendservice.close()

    def runClients(self):

        # Creating a lock object to pass it to the threads inorder to protect the critical region
        lock = threading.Lock()

        # Starting the threads
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(self.threadingClient, lock) for i in range(self.numOfClients)]

        # Waiting for all the threads to complete
        wait(futures)

        self.averageLatency = 0
        for latency in self.requestLatencyArray:
            self.averageLatency += latency

        # Computing average of the average latencies encountered by each client
        self.averageLatency /= self.numOfClients


if __name__ == '__main__':

    # Defining default values for number of clients and hostname of the frontend service
    numClients = 5
    hostName = '0.0.0.0'

    # Read command line parameters and override the default values of
    # hostName, number of clients
    if len(sys.argv) > 1:
        hostName = sys.argv[1]
    if len(sys.argv) > 2:
        numClients = int(sys.argv[2])

    onlyQueryRequests = onlyQueryRequests(numClients,hostName)
    onlyQueryRequests.runClients()

    print('Average Latency per request for each client (ms): ', onlyQueryRequests.requestLatencyArray)
    print('Average latency per request (ms):', onlyQueryRequests.averageLatency)
