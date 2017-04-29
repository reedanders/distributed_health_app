#!/usr/bin/env python3

import requests
import random
import string
import sys

endpoint = 'http://127.0.0.1:5000'

class user(object):

    def __init__(self,username,pwd):
        global endpoint
        self.name = username;
        self.id = 'A'
        self.password=pwd
        #self.id = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10))
        self.vector = [.1,.2,.3,.5]
        self.attrs = {
        'Age' : None,
        'Gender' : None,
        'HeartRateAvg' : None,
        'ExerciseHrs' : None,
        'SleepHrs': None,
        'SaltLv' : None,
        'WaterIntake': None,
        'DiseaseType' : None,
        'DiseaseDuration': None,
        'OtherData' : None
        }
        self.kvstore={}

    def register(self):
        try:
            requests.post(endpoint+'/register',data={'user':self.id, 'password': self.password})
        except:
            print("Register Failed")

    def login(self):
        try:
            requests.post(endpoint+'/register',data={'user':self.id, 'password': self.password})
        except:
            print("Login Failed")

    
    def collect_data(self):
        """
        Set Random Values For Now
        """
        self.attrs['Age'] = 25
        # 0 = Male 1 = Female
        self.attrs['Gender'] = 1
        self.attrs['HeartRateAvg'] = 75
        self.attrs['ExerciseHrs'] = 2
        self.attrs['SleepHrs'] = 7
        self.attrs['SaltLv'] = 20
        # Liters
        self.attrs['WaterIntake'] = 3
        # Need a disease type to number matching
        self.attrs['DiseaseType'] = 420
        # Months
        self.attrs['DiseaseDuration'] = 24
        self.attrs['OtherData'] = None

    def update_server(self):
        global endpoint
        request_vector = ', '.join([str(y) for y in self.vector])
        try:
            resp = requests.post(endpoint+'/update',data={'user':self.id, 'vector': request_vector})
            self.kvstore = {}
            for k in resp.json():
                self.kvstore[k] = None
        except:
            print("Unable to update upstream server")

    def get_ip_list(self):
        global endpoint
        requestd = {'user' : self.id, 'userids':['A','B']}
        try:
            resp = requests.post(endpoint+'/getips',data=requestd)
            self.compat_ip_list = resp
            for k in resp.json.keys():
                self.kvstore[k] = resp.json()[k]
#        print(resp.json())
        except:
            print("Unable to update upstream server")

def showmenu():
    print("""
    1. Register
    2. Login
    3. List Compatible Users
    4. Chat with a User
    5. Show my profile
    6. Quit Application
""")

def run():
    uname = input("Enter Username: ")
    upass = input("Enter Password for "+uname+": ")
    uobject = user(uname,upass)
    print("User Created Successfully!")
    print("Enter help for commandlist")
    while(1):
        cmd = input(">>")
        if cmd == "help":
            showmenu()
        elif cmd == "1":
            uobject.register()
        elif cmd == "2":
            uobject.login()
        elif cmd == "3":
            printf(uobject.kvstore)
        elif cmd == "4":
            print("Profile for",uname,":")
            print(uobject.attrs)
        elif cmd == "5":
            None
        elif cmd == "6":
            sys.exit(0)


if __name__=='__main__':
    run()
"""
hackwa = user("hackwa")
print(hackwa.name,hackwa.id,hackwa.vector)
hackwa.collect_data()
hackwa.update_server()
print(hackwa.attrs)
print(list(hackwa.attrs.values()))
print("Get IP list for userids: [A,B]")
hackwa.get_ip_list()
"""
