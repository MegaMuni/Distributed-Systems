
 Add your source code to this directory. Part 1 should go to a directory called *part1* and Part 2 should go to a directory called *part2*
## How to run the code 

Part 1: Implementation with Socket Connection and Handwritten Thread Pool

javac Server.java #Compiles the Server class

java Server #Runs Server

javac Client.java #Compiles the Client class

java Client #Runs Client

javac ClientLoadTest.java #Compiles the ClientLoadTest class

Examples on how to run the load tests:

(Parameters are method name and num of clients you want to run. If no method name is given we evaluate on random requests. If num of clients parameter is not given we do the load test for one client, two clients, three clients, four clients, five clients each)

java ClientLoadTest query 2

java ClientLoadTest query 2

java ClientLoadTest

Now we write to json files when we run the class with only method type


java ClientLoadTest buy  -> This call writes to the jsonBuyMethodCalls.json

java ClientLoadTest query -> This call writes to the jsonQueryMethodCalls

java ClientLoadTest       -> This call writes to the jsonRandomMethodCalls.json 

python plotBuyReqGraph.py -> Plots the graph for buy request

python plotQueryReqGraph.py -> Plots the graph for Query request

Python plotRandomReqGraph.py -> Plots the graph for Random request


Part 2: Implementation with gRPC and Built in Thread Pool Execution Steps: 

1.Generate the data access classes using the protocol buffer compiler-protoc with below command in local :
    python3 -m grpc_tools.protoc --proto_path=. ./toy_store.proto --python_out=. --grpc_python_out=.

2.Files toy_store_pb2.py and toy_store_pb2_grpc.py will be generated.

3.Run toystore_server.py using below command in edlab:
    python3 toystore_server.py

4.Run master_toystore_client.py in local machine. 
    python3 master_toystore_client.py

5.Provide the number of clients(n) with which you want to invoke the server in a multithreaded fashion. 

6.Provide the method you want to invoke -Query/Buy 
 

Part 3: Execution steps for Evaluation and Performance Measurement for Toy Store implementation in gRPC :

1.Generate the data access classes using the protocol buffer compiler-protoc with below command in local:
  python3 -m grpc_tools.protoc --proto_path=. ./toy_store.proto --python_out=. --grpc_python_out=.

2.Files toy_store_pb2.py and toy_store_pb2_grpc.py will be generated. 

3.Run toystore_server.py using below command in edlab :
    python3 toystore_server.py

4.Run master_toystore_client.py in local machine. 
    python3 master_toystore_client.py

5.Provide the number of clients(n) with which you want to invoke the server in a multithreaded fashion. 

6.Provide the method you want to invoke -Query/Buy 

7.Run toystore_plotting.py 

8.Simple plot showing the number of clients on X-axis and response-time(in seconds)/latency on Y.axis.
