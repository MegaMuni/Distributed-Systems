from __future__ import print_function

import logging
from os import name
import threading
import grpc
import toy_store_pb2
import toy_store_pb2_grpc
import random
import time
import toystore_client

host = "elnux.cs.umass.edu:"
port = 12121

def run():
    
    client_no = input('Please provide number of clients: ')
     #taking input from user whether to invoke Query or Buy method 
    mthd_toinvoke = input('Do you want to Query or Buy an item: ')

    jbs = []
    
    with open(mthd_toinvoke+client_no+'.txt','w+') as f:
        f.write('')

    #passing the number of clients (1 to 5) and invoking toystore client from this master client file
    for i in range(int(client_no)):
        thread = threading.Thread(target=toystore_client.run, args=[host,mthd_toinvoke,client_no])
        jbs.append(thread)
    
    for i in jbs :
       i.start()

    for i in jbs :
        i.join()

if __name__ == '__main__':
    logging.basicConfig()
    
    run()
