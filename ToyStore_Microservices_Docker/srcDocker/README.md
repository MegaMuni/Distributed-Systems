How to run part2:

We have everything needed to build the the images and containers inside the docker-compose.yml. We have provided a shell script that deletes the cache and builds all our containers using the compose file. Please run the script using the following command:

sh build.sh

Once all your containers are up, start testing the latencies using the client interfaces we provided. Note that whenever we try to run the client interfaces, we should always provide the host name as a parameter. Examples are given below:

Steps to run clients:

python3 client.py 

The above command does the following (No parameters passes -> Use Default parameters):

Starts 5 client threads, connects to host 0.0.0.0, probability (p) for query requests = 0.75

Passing parameters through command line:

python3 client.py 127.119.243.168 3 0.95

The above command creates three client threads which connects to 127.119.243.168 and makes buy requests with a probability of 0.95


We have an interfaces that runs either only buy or only query requests:

You can run them as follows:

Default values in these interfaces:

Host = 0.0.0.0
Number of clients: 5

python3 onlyBuyRequests

python3 onlyBuyRequests 127.119.243.168 3        -> Passing HostName = '127.119.243.168'; Num of Clients = 3

python3 onlyQueryRequests

python3 onlyQueryRequests 127.119.243.168 3      -> Passing HostName = '127.119.243.168'; Num of Clients = 3


Running aggregateLoadTest.py which gives us the graphs we need for part 3 of the lab:

The clear description of what happens inside this file is given in the design doc of part1.

Default values in this interface:

Host = 0.0.0.0
Probability (p) = 0.75

python3 aggregateLoadTest.py 

python3 aggregateLoadTest.py 127.119.243.168 0.95    -> Passing HostName = '127.119.243.168' ProbBuy requests: 0.95