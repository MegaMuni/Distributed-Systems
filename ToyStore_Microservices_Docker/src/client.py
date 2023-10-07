import random
import socket
import json
import threading
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import wait
import time
import sys


class client:
    def __init__(self, numOfClients, p, hostName):
        self.numOfClients = numOfClients
        self.p = p
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
            randomItem = random.randint(0, 3)

            # Forming a get request with a random item
            getRequest = 'GET /products?product_name=' + items[randomItem] + ' HTTP/1.1\r\n'

            # Sending the request to the frontendservice
            start = time.time()
            frontendservice.send(getRequest.encode('utf-8'))
            r = frontendservice.recv(1024)
            end = time.time()

            # Computing the latency
            latency += (end - start)
            numberOfRequests += 1

            r = json.loads(r.decode('utf-8').split('\n')[4])
            print("Get Request Response: " + json.dumps(r))
            if r.get("data").get("quantity") > 0:

                # Get a random number between 0 and 1
                randomProb = random.uniform(0, 1)

                # Calling post request based on probability
                if randomProb >= (1 - self.p):

                    # Making sure that the user orders not more than 5 toys
                    buyQuantity = random.randint(1, r.get("data").get("quantity"))
                    if buyQuantity > 5:
                        buyQuantity = random.randint(1, 5)

                    # Building POST request
                    postJson = {'name': items[randomItem], 'quantity': buyQuantity}
                    postRequest = 'POST /orders HTTP/1.1\r\n' + json.dumps(postJson)

                    start = time.time()
                    frontendservice.send(postRequest.encode('utf-8'))
                    r = frontendservice.recv(1024)
                    end = time.time()

                    # Evaluating latency
                    latency += (end - start)
                    numberOfRequests += 1
                    r = json.loads(r.decode('utf-8').split('\n')[4])
                    print("Post Request Response: " + json.dumps(r))
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

        # Computing average of the average latencies encountered by each client
        self.averageLatency = 0
        for latency in self.requestLatencyArray:
            self.averageLatency += latency

        self.averageLatency /= self.numOfClients


if __name__ == '__main__':

    # Defining default values for hostname of the frontend service, number of clients and buy probability
    numClients = 5
    probBuy = 0.75
    hostName = '127.0.0.1'

    # Read command line parameters and override the default values of
    # hostName, number of clients and buy probability
    if len(sys.argv) > 1:
        hostName = sys.argv[1]
    if len(sys.argv) > 2:
        numClients = int(sys.argv[2])
    if len(sys.argv) > 3:
        probBuy = float(sys.argv[3])

    # Creating the client object
    client = client(numClients, probBuy, hostName)

    # Start the clients
    client.runClients()

    print('Average Latency per request for each client (ms): ', client.requestLatencyArray)
    print('Average latency per request (ms):', client.averageLatency)
