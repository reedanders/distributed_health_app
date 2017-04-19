#!/usr/bin/env python3

import requests
import random
import string

endpoint = 'http://127.0.0.1:5000'

class user(object):

    def __init__(self,username):
        global endpoint
        self.name = username;
        self.id = 'A'
        self.password='X'
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
        try:
            requests.post(endpoint+'/register',data={'user':self.id, 'password': self.password})
            requests.post(endpoint+'/login',data={'user':self.id, 'password': self.password})
        except:
            None
    
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
            print(resp.json())
        except:
            print("Unable to update upstream server")

    def get_ip_list(self):
        global endpoint
        requestd = {'user' : self.id, 'userids':['A','B']}
#        try:
        resp = requests.post(endpoint+'/getips',data=requestd)
        print(resp.json())
#        except:
#            print("Unable to update upstream server")
        

hackwa = user("hackwa")
print(hackwa.name,hackwa.id,hackwa.vector)
hackwa.collect_data()
hackwa.update_server()
print(hackwa.attrs)
print(list(hackwa.attrs.values()))
print("Get IP list for userids: [A,B]")
hackwa.get_ip_list()
