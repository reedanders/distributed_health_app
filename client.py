#!/usr/bin/env python3

import requests
import random
import string

endpoint = 'http://127.0.0.1:5000/update' 

class user(object):

    def __init__(self,username):
        self.name = username;
        self.id = 'A'
        #self.id = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10))
        self.vector = [.1,.2,.3,.5]
    
    def collect_data(self):
        None

    def update_server(self):
        global endpoint
        request_vector = ', '.join([str(y) for y in self.vector])
        try:
            resp = requests.post(endpoint,data={'user':self.id, 'vector': request_vector})
        except:
            print("Unable to update upstream server")
        print(resp.json())
        

hackwa = user("hackwa")
print(hackwa.name,hackwa.id,hackwa.vector)
hackwa.update_server()
