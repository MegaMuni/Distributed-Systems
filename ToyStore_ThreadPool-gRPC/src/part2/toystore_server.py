from concurrent import futures
import logging
import threading
import grpc
import numpy as np
import toy_store_pb2
import toy_store_pb2_grpc
import time

port = 12121

class ToyStore(toy_store_pb2_grpc.ToyStoreServicer):
    def __init__(self) -> None:
        super().__init__()
        self.lock = threading.Lock()

    # querying as per the toy name
    def Query(self,request,context) :
        self.lock.acquire()
        for row in toy :
            count = 0
            priceQ = -1.0
            stockQ =-1 
            for i in range(4):  
                if row[i][0] == request.toy:
                    priceQ = float(row[i][1])
                    stockQ = int(row[i][2])
                else :
                    count = count +1 
        # if count == 4 :
        #     return toy_store_pb2.ToyStoreSearchResponse(stock = stockQ)
        # else:
        self.lock.release()
        return toy_store_pb2.ToyStoreSearchResponse(price=priceQ,stock=stockQ)       
         
     #implementation of buyitem method   
    def BuyItem(self,request,context) :
        self.lock.acquire()
        stock = 0
        count = 0
        val = 0 
        for row in toy :
           for i in range(4) :
               # toy matched and 0 quantity               
                if row[i][0] == request.buy_toy and row[i][2] == '0' :
                    val=0
                    self.lock.release()  
                    return toy_store_pb2.ToyStoreBuyResponse(value=val)
                elif row[i][0] == request.buy_toy and row[i][2] != '0' :
                    stock = int(row[i][2]) - 1
                    row[i][2] = str(stock)
                    val = 1
                    self.lock.release()  
                    return toy_store_pb2.ToyStoreBuyResponse(value = val)
        
        val = -1
        self.lock.release()   
        return toy_store_pb2.ToyStoreBuyResponse(value= val)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    toy_store_pb2_grpc.add_ToyStoreServicer_to_server(ToyStore(), server)
    server.add_insecure_port('[::]:12121')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    toy = np.array([['Tux',5.99,2],['Whale',8.99,1],['Elephant',11.99,1],['Bird',11.99,1]]).tolist(),
    serve()
