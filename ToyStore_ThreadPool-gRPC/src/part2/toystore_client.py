from __future__ import print_function

import logging
from os import name
import grpc
import toy_store_pb2
import toy_store_pb2_grpc
import random
import socket
import time
import statistics
import matplotlib.pyplot as plt


host = "elnux.cs.umass.edu:"
port = 12121

def run(host, method, client_no):
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    
    channel = grpc.insecure_channel(host+str(12121), options=(('grpc.enable_http_proxy', 0),))
    stub = toy_store_pb2_grpc.ToyStoreStub(channel)
    user_input = method 
    toy_items = ['Tux','Whale','Elephant','Bird','Random_Toy']
    latency = []
    numcl = client_no
    
    for i in range(100) :
        # assigning random toys to name field
        toyindex = random.choices(range(len(toy_items)), k=1)[0]
        name = toy_items[toyindex]
        #if user input is query, we are calculating the time and calling the Query method in Server        
        t = time.time()
        if(user_input == 'Query'):
            response = stub.Query(toy_store_pb2.ToyStoreSearchQuery(toy= name))
            if (response.stock == -1) : 
                print('Item does not exist')
            #if user input is Query and if the item and stock exists, price and stock of the item will be returned    
            else :
                print('Price ', response.price)
                print('Stock', response.stock)
        #else if user input is buy, we are calculating the time and calling the Query method in Server
        elif(user_input == 'Buy') :
            response = stub.BuyItem(toy_store_pb2.ToyStoreBuy(buy_toy= name))
            print('Buy response', response.value)
        #if user provides a value other than Query or Method as input method
        else :
            print('Please provide a valid response')
        new_t = time.time()
        delta_t = new_t - t
        latency.append(round(delta_t * 1000))
    #calculating mean latencies 
    lat=statistics.mean(latency)
    #writing lat values to a file
    with open(user_input+numcl+'.txt', 'a') as file:
        file.write(f"{lat}\n")
    

if __name__ == '__main__':
    logging.basicConfig()
    run()
