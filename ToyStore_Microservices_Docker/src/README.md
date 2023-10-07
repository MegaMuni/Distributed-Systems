How to run the code:

Make sure you have python 3.8 installed

If at all you face any issue as 'module not found', please run:

pip3 install <module_name>

Start frontendservice.py, catalog.py, orders.py:

python3 frontendservice.py

python3 catalog.py

python3 orders.py


Steps to run clients:

python3 client.py 

The above command does the following (No parameters passes -> Use Default parameters):

Starts 5 client threads, connects to host 127.0.0.1, probability (p) for query requests = 0.75

Passing parameters through command line:

python3 client.py 0.0.0.0 3 0.95

The above command creates three client threads which connects to 0.0.0.0 and makes buy requests with a probability of 0.95


We have an interfaces that runs either only buy or only query requests:

You can run them as follows:

Default values in these interfaces:

Host = 127.0.0.1
Number of clients: 5

python3 onlyBuyRequests

python3 onlyBuyRequests 0.0.0.0 3        -> Passing HostName = '0.0.0.0'; Num of Clients = 3

python3 onlyQueryRequests

python3 onlyQueryRequests 0.0.0.0 3      -> Passing HostName = '0.0.0.0'; Num of Clients = 3


Running aggregateLoadTest.py which gives us the graphs we need for part 3 of the lab:

The clear description of what happens inside this file is given in the design doc of part1.

Default values in this interface:

Host = 127.0.0.1
Probability (p) = 0.75

python3 aggregateLoadTest.py 

python3 aggregateLoadTest.py 0.0.0.0 0.95    -> Passing HostName = '0.0.0.0' ProbBuy requests: 0.95