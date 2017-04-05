#!/usr/bin/env python3

import requests
import random
import string

endpoint = 'http://127.0.0.1:5000/update' 

class user(object):

    def __init__(self,username):
        self.name = username;
        self.id = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10))
        self.vector = [.1,.2,.3,.5]
    
    def collect_data(self):
        None

    def update_server(self):
        global endpoint
        try:
            requests.post(endpoint,data={'user':self.id, 'vector': self.vector})
        except:
            print("Unable to update upstream server")

hackwa = user("hackwa")
print(hackwa.name,hackwa.id,hackwa.vector)
hackwa.update_server()
