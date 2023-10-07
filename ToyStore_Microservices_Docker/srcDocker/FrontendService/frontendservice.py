import os
import json
import socket
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse
# thread function

response = """\
HTTP/1.1 {status_code} {status_message}
Content-Type: application/json; charset=UTF-8
Content-Length: {content_length}

{payload}
"""

def threaded(c):
    while True:
        # Data received from client
        print('I am waiting to recieve')
        httpRequest = c.recv(1024)

        # If client stops sending messages, the break the loop and close the socket
        # This is a thread per session model
        if not httpRequest:
            print('Bye')
            break

        # Parsing the http request
        arr = httpRequest.decode().split('\r\n')
        print(arr)

        # Getting all the data we need from the http message
        request = arr[0]
        request_type = request.split(' ')[0]
        parsed = urlparse(request.split(' ')[1])
        request_path = parsed.path
        request_query = parsed.query
        request_body = arr[len(arr) - 1]

        # Getting the dictionary from the raw json the client passes with the post request
        request_body_json = json.loads(request_body.replace('\n', '')) if request_body != '' else {}

        # Getting the dictionary from the url parameters the client passes through the url
        request_query_json = {i.split('=')[0]: i.split('=')[1] if len(i.split('=')) == 2 else None for i in
                              request_query.split('&')} if request_query != '' else {}

        # Checking is the request is a 'GET' or a 'POST' request
        if request_type != 'GET' and request_type != 'POST':
            payload = json.dumps({"error": {"code": 404, "message": "Invalid Method Call"}})
            c.send(response.format(status_code=404,
                                   status_message="Invalid Method Call",
                                   content_length=len(payload),
                                   payload=payload)
                   .encode("utf-8"))
            continue

        # Checking if the resource name is '/products' or '/orders'
        if request_path != '/products' and request_path != '/orders':
            payload = json.dumps({"error": {"code": 404, "message": "Invalid URL Path"}})
            c.send(response.format(status_code=404,
                                   status_message="Invalid URL Path",
                                   content_length=len(payload),
                                   payload=payload)
                   .encode("utf-8"))
            continue

        # Checking if the resource name is '/products' when it is a 'GET' request
        # Checking if the resource name is '/orders' when it is a 'POST' request
        if (request_type == 'GET' and request_path != '/products') or (request_type == 'POST' and request_path != '/orders'):
            payload = {"error": {"code": 404, "message": "Invalid Resource for this Request type"}}
            c.send(response.format(status_code=404,
                                   status_message="Invalid Resource for this Request type",
                                   content_length=len(payload),
                                   payload=payload)
                   .encode("utf-8"))
            continue
        data = {}
        if request_type == 'GET':
            # Additional check to see the data type of the request_query_json
            if isinstance(request_query_json,str):
                request_query_json = json.loads(request_query_json)

            # Check if the url has product_name parameter when try to do a 'GET' request
            if request_query_json.get("product_name") is None:
                payload = json.dumps({"error": {"code": 404, "message": "{product_name} parameter missing"}})
                c.send(response.format(status_code=404,
                                       status_message="{product_name} parameter missing",
                                       content_length=len(payload),
                                       payload=payload)
                       .encode("utf-8"))
                continue
            else:

                # If everything is good then proceed to execute the request

                # Form a dictionary with the data we need to communicate with Catalog
                data["type"] = "get"
                data["name"] = request_query_json.get("product_name")

                # Start communication with Catalog
                catalog = socket.socket()
                port = 9001
                catalog.connect((catalog_host, port))
                catalog.send(json.dumps(data).encode('utf-8'))
                message = catalog.recv(1024)
                catalog.close()

                message = json.loads(message)

                # Process the information we received from the catalog and build payload we need to send to the client
                if message.get("code")==1:
                    payload = json.dumps({"data":{"name":message.get("name"),"price":message.get("price"),"quantity":message.get("quantity")}})
                else:
                    payload = json.dumps({"data": {"code": message.get("code"),
                                                   "message": message.get("message")}})

                # Format a HTTP message with the payload we built and send to client
                c.send(response.format(status_code=1,
                                       status_message="Get method success",
                                       content_length=len(payload),
                                       payload=payload)
                       .encode("utf-8"))

        if request_type == 'POST':

            # Additional check to see the data type of the request_query_json
            if isinstance(request_body_json,str):
                request_body_json = json.loads(request_body_json)

            # Check if the raw JSON sent by the client has both name and quantity attributes for the 'POST' request
            if request_body_json.get("name") is None or request_body_json.get("quantity") is None:
                payload = json.dumps({"error": {"code": 404, "message": "name or quantity parameter missing in raw json file"}})
                c.send(response.format(status_code=404,
                                       status_message="name or quantity parameter missing in raw json file",
                                       content_length=len(payload),
                                       payload=payload)
                        .encode("utf-8"))
                continue
            else:

                # If everything is good then proceed to execute the request

                # Form a dictionary with the data we need to communicate with Orders
                data["type"] = "post"
                data["name"] = request_body_json.get("name")
                data["quantity"] = request_body_json.get("quantity")

                # Form a connection with orders and send the request with above dictionary
                orders = socket.socket()
                port = 9000
                orders.connect((order_host, port))
                orders.send(json.dumps(data).encode('utf-8'))
                resp = orders.recv(1024)
                orders.close()

                message = json.loads(resp)

                # Analyze the response from the orders service and build the payload to the client
                if message.get("code") == 1:
                    payload = json.dumps({"data":{"order_number":message.get("order_number")}})
                else:
                    payload = json.dumps({"data": {"code": message.get("code"),
                                                   "message": message.get("message")}})

                # Format a HTTP message with the payload we built and send to client
                c.send(response.format(status_code=1,
                                       status_message="Post method success",
                                       content_length=len(payload),
                                       payload=payload)
                       .encode("utf-8"))

    # Close the socket after coming out of the while loop
    c.close()
    print('Connection Closed')
def main():

    # Defining host and port
    host = "0.0.0.0"
    port = 8000

    # Binding the socket to a port and starting the server
    s = socket.socket()
    s.bind((host, port))
    print("socket binded to port", port)
    # put the socket into listening mode
    s.listen(5)
    print("socket is listening")
    # Created a threadpool
    executor = ThreadPoolExecutor(max_workers=10)
    # a forever loop until client wants to exit
    while True:
        # establish connection with client
        c, addr = s.accept()
        print("Connected to :", addr[0], ":", addr[1])

        # Assign new thread to process the client's requests
        executor.submit(threaded, c)
if __name__ == "__main__":
    catalog_host = os.getenv("CATALOG_HOST", "srcdocker_catalog_1")
    order_host = os.getenv("ORDER_HOST", "srcdocker_orders_1")
    
    main()