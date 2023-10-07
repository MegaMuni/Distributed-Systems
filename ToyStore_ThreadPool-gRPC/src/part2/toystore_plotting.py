from __future__ import print_function
from http import client
import logging
from os import name
import grpc
import toy_store_pb2
import toy_store_pb2_grpc
import time
import statistics
import matplotlib.pyplot as plt
import os

list1 = []
list2 = []
client_toy= [1,2,3,4,5]

#finding which method user has invoked based on the generated filename
for x in os.listdir():
    if x.startswith("Query"):
        mthd1 = 'Query'
        list1.append(x)
    elif x.startswith("Buy"):
        mthd2 = 'Buy'
        list2.append(x)

def run():
    mean_latency=[]
    for filename in list1 :
        temp = []
        f = open(filename,'r')
        for row in f:
            temp.append(float(row))
        mean_latency.append(statistics.mean(temp))

    #plotting for querying an item
    plt.plot(client_toy,mean_latency)
    plt.xlabel('No.of clients')
    plt.ylabel('Response time/Latency in milliseconds')
    plt.title('Response time for Query')
    plt.show()
    print('here')

    mean_latency=[]
    for filename in list2:
        temp = []
        f = open(filename,'r')
        for row in f:
            temp.append(float(row))
        mean_latency.append(statistics.mean(temp))
    #plotting for buying an item
    plt.plot(client_toy,mean_latency)
    plt.xlabel('No.of clients')
    plt.ylabel('Response time/Latency in milliseconds')
    plt.title('Response time for Buy')
    plt.show()

if __name__ == '__main__':
    logging.basicConfig()
    run()
