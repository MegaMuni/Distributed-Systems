import sys
from client import client
from onlyQueryRequests import onlyQueryRequests
from onlyBuyRequests import onlyBuyRequests

import matplotlib.pyplot as plt

if __name__ == '__main__':

    # Defining default values for buy probability and hostname of the frontend service
    probBuy = 0.75
    hostName = '127.0.0.1'

    # Read command line parameters and override the default values of
    # hostName and probability
    if len(sys.argv) > 1:
        hostName = sys.argv[1]
    if len(sys.argv) > 2:
        probBuy = float(sys.argv[2])

    # In the first loop we get latencies on only buy requests, varying the number of clients
    # In the second loop we get latencies on only query requests, varying the number of clients
    # In the third loop we get latencies when both type of requests are sent, varying the number of clients

    latency = {}
    print(
        '--------------------------Test only buy request types on various number on clients---------------------------------\n')

    for numClients in range(5):
        print("\n-----------------Number of clients = {num}--------------------".format(num=numClients + 1))
        testClient = onlyBuyRequests(numClients + 1, hostName)
        testClient.runClients()
        print('Latency for each client: ', testClient.requestLatencyArray)
        print('Average request latency when {num} client/s runs together: '.format(num=numClients + 1),
              testClient.averageLatency)
        latency[numClients + 1] = testClient.averageLatency
    print('\n\n')

    print('Latency map for only buy requests: {map}'.format(map=latency))

    # Plotting the graph of latency wrt number of clients
    plt.grid(True)
    plt.plot(*zip(*sorted(latency.items())))
    plt.plot(color='maroon', marker='o')
    plt.xlabel('Number of Clients')
    plt.ylabel('Average latency per request (only buy requests)) (ms)')
    plt.show()

    latency = {}
    print(
        '--------------------------Test only query requests on various number on clients---------------------------------\n')

    for numClients in range(5):
        print("\n-----------------Number of clients = {num}--------------------".format(num=numClients + 1))
        testClient = onlyQueryRequests(numClients + 1, hostName)
        testClient.runClients()
        print('Latency for each client: ', testClient.requestLatencyArray)
        print('Average request latency when {num} client/s runs together: '.format(num=numClients + 1),
              testClient.averageLatency)
        latency[numClients + 1] = testClient.averageLatency
    print('\n\n')

    print('Latency map for only query request types: {map}'.format(map = latency))

    # Plotting the graph of latency wrt number of clients
    plt.grid(True)
    plt.plot(*zip(*sorted(latency.items())))
    plt.plot(color='maroon', marker='o')
    plt.xlabel('Number of Clients')
    plt.ylabel('Average latency per request (only query requests)) (ms)')
    plt.show()

    latency = {}
    print(
        '--------------------------Test both request types on various number on clients---------------------------------\n')

    for numClients in range(5):
        print("\n-----------------Number of clients = {num}--------------------".format(num=numClients + 1))
        testClient = client(numClients + 1, probBuy, hostName)
        testClient.runClients()
        print('Latency for each client: ', testClient.requestLatencyArray)
        print('Average request latency when {num} client/s runs together: '.format(num=numClients + 1),
              testClient.averageLatency)
        latency[numClients + 1] = testClient.averageLatency
    print('\n\n')

    print('Latency map for both request types: {map}'.format(map=latency))

    # Plotting the graph of latency wrt number of clients
    plt.grid(True)
    plt.plot(*zip(*sorted(latency.items())))
    plt.plot(color='maroon', marker='o')
    plt.xlabel('Number of Clients')
    plt.ylabel('Average latency per request (both get and buy)) (ms)')
    plt.show()


