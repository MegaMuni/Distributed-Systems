import random
import unittest
import socket
import json

class Testcases(unittest.TestCase):

    #Placing an order for a certain product
    def testUpdate_PositiveCase(self):

        print('Test1')
        s_update = socket.socket()
        host ="0.0.0.0"
        port = 8000
        postJson = {'name': 'Whale', 'quantity': 1 }
        postRequest = 'POST /orders HTTP/1.1\r\n' + json.dumps(postJson) 
        s_update.connect((host, port))
        s_update.send(postRequest.encode('utf-8'))
        data = s_update.recv(1024).decode('utf-8')
        print('Testing for Placing an order for a certain product', data)
        s_update.close()
    
    #Placing an order for a certain product with a quantity higher than in the toy store
    def testUpdate_NegativeCase(self):
        print('Test2')
        s_update = socket.socket()
        host ="0.0.0.0"
        port = 8000
        postJson = {'name': 'Tux', 'quantity': 50000 }
        postRequest = 'POST /orders HTTP/1.1\r\n' + json.dumps(postJson) 
        s_update.connect((host, port))
        s_update.send(postRequest.encode('utf-8'))
        data = s_update.recv(1024).decode('utf-8')
        print('Testing for placing an order for a certain product with a quantity higher than in the toy store', data)
        s_update.close()

    # querying the details of an existing product
    def testQuery_ExistingProduct(self):
        print('Test3')
        s_get = socket.socket()
        host ="0.0.0.0"
        port = 8000
        existing_items = ['Tux', 'Whale', 'Elephant', 'Bird']
        randomItem = random.randint(0, 3)
        getRequest_existing = 'GET /products?product_name=' + existing_items[randomItem] + ' HTTP/1.1\r\n'
        s_get.connect((host, port))
        s_get.send(getRequest_existing.encode('utf-8'))
        resp_Existing = s_get.recv(1024).decode('utf-8')
        print('Testing for Querying the details of an existing product',resp_Existing)
        s_get.close()

    #Querying the details of non-existing product
    def testQuery_NonExistingProduct(self):
        print('Test4')
        s_get = socket.socket()
        host ="0.0.0.0"
        port = 8000
        # querying the details of non-existing product
        getRequest_Nonexisting ='GET /products?product_name=' + 'Ostrich' + ' HTTP/1.1\r\n'
        s_get.connect((host, port))
        s_get.send(getRequest_Nonexisting.encode('utf-8'))
        resp_Nonexisting = s_get.recv(1024).decode('utf-8')
        print('Testing for Querying the details of non-existing product',resp_Nonexisting)
        s_get.close()

    #testing invalid method call
    def test_InvalidMethod(self):
        print('Test5')
        s_get = socket.socket()
        host ="0.0.0.0"
        port = 8000
        # testing invalid method call
        existing_items = ['Tux', 'Whale', 'Elephant', 'Bird']
        randomItem = random.randint(0, 3)
        invalidMethod_Request = 'PUT /products?product_name=' + existing_items[randomItem] + ' HTTP/1.1\r\n' 
        s_get.connect((host, port))
        s_get.send(invalidMethod_Request.encode('utf-8'))
        resp_invalidMethod = s_get.recv(1024).decode('utf-8')
        print('Testing Invalid method response',resp_invalidMethod)
        s_get.close()

    #testing  invalid URL path
    def test_InvalidURLPath(self):
        print('Test6')
        s_get = socket.socket()
        host ="0.0.0.0"
        port = 8000
        # testing invalid method call
        existing_items = ['Tux', 'Whale', 'Elephant', 'Bird']
        randomItem = random.randint(0, 3)
        invalidURL_Request= 'GET /product?product_name=' + existing_items[randomItem] + ' HTTP/1.1\r\n' 
        s_get.connect((host, port))
        s_get.send(invalidURL_Request.encode('utf-8'))
        resp_invalidURL = s_get.recv(1024).decode('utf-8')
        print('Testing Invalid URL Path response',resp_invalidURL)
        s_get.close()

    #testing Invalid Resource for this Request type
    def test_InvalidResource(self):
        print('Test7')
        s_get = socket.socket()
        host ="0.0.0.0"
        port = 8000
        # testing Invalid Resource for this Request type
        existing_items = ['Tux', 'Whale', 'Elephant', 'Bird']
        randomItem = random.randint(0, 3)
        invalidResource_Request= 'GET /product1?product_name' + existing_items[randomItem] + ' HTTP/1.1\r\n' 
        s_get.connect((host, port))
        s_get.send(invalidResource_Request.encode('utf-8'))
        resp_invalidResource = s_get.recv(1024).decode('utf-8')
        print('Testing Invalid resource response',resp_invalidResource)
        s_get.close()

    #testing {product_name} parameter missing in POST method
    def testPOST_ParamMiss(self):
        
        print('Test8')
        s_update = socket.socket()
        host ="0.0.0.0"
        port = 8000
        postJson = {'name': 'Whale'}
        postRequest = 'POST /orders HTTP/1.1\r\n' + json.dumps(postJson) 
        s_update.connect((host, port))
        s_update.send(postRequest.encode('utf-8'))
        data = s_update.recv(1024).decode('utf-8')
        print('Testing for missing param in POST method', data)
        s_update.close()

    #testing parameter missing in GET method
    def testQuery_ParamMiss(self):
        print('Test9')
        s_get = socket.socket()
        host ="0.0.0.0"
        port = 8000
        existing_items = ['Tux', 'Whale', 'Elephant', 'Bird']
        randomItem = random.randint(0, 3)
        getRequest_existing = 'GET /products?' + ' HTTP/1.1\r\n'
        s_get.connect((host, port))
        s_get.send(getRequest_existing.encode('utf-8'))
        resp_Existing = s_get.recv(1024).decode('utf-8')
        print('Testing for missing param in GET method',resp_Existing)
        s_get.close()


    
if __name__ == '__main__':
    unittest.main()