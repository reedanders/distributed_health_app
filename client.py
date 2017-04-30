#!/usr/bin/env python3

import requests
import random
import string
import threading
import sys
import json
from time import sleep
import os
import hashlib
import subprocess
import signal

endpoint = 'http://127.0.0.1:5000'

def alarm_handler(signum, frame):
    raise Exception("TimeoutExpired")

def input_with_timeout(timeout):
    # set signal handler
    signal.signal(signal.SIGALRM, alarm_handler)
    signal.alarm(timeout) # produce SIGALRM in `timeout` seconds
    try:
        return input("")
    except:
        return None
    finally:
        signal.alarm(0) # cancel alarm

def send_msg(usr_name, fromUsr, proc):
    print('Enter message: ', end='')
    msg = None
    while True:
        msg = input_with_timeout(1)
        if proc.poll() is not None:
            print("")
            return None
        elif msg is not None:
            break
    file_name = str(usr_name)
    f = open(file_name, 'a')
    f.write(fromUsr + ': '+ msg + '\n')
    f.close()
    return msg

def chat_history_update(usr_name,msgs):
    file_name = str(usr_name)
    f = open(file_name, 'a')
    for line in msgs:
        f.write(usr_name + ": " + line + '\n')
    f.close()

class user(object):

    def __init__(self,username,pwd):
        global endpoint
        self.name = username;
        self.id = username
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
        self.stop_polling = 0

    def register(self):
        try:
            r = requests.post(endpoint+'/register',data={'user':self.id, 'password': self.password})
            if r.status_code == 200:
                print("Registered with server")
            else:
                print("Register Failed")
        except:
            print("Register Failed")

    def login(self):
        try:
            r = requests.post(endpoint+'/login',data={'user':self.id, 'password': self.password})
            if r.status_code == 200:
                print("Login Successful")
            else:
                print("Login Failed")
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
        print("Starting background poll thread")
        while True:
            if self.stop_polling:
                return
            request_vector = ', '.join([str(y) for y in self.vector])
            #try:
            if True:
                resp = requests.post(endpoint+'/update',data={'user':self.id, 'vector': request_vector})
                if resp.status_code == 200:
                    self.kvstore = {}
                    for k in resp.json():
                        self.kvstore[k] = None
                sleep(5)
            #except:
                #print("Update Server: Unable to update upstream server")
                #sleep(5)

    def get_ip_list(self):
        global endpoint
        requestd = {'user' : self.id, 'userids':['A','B']}
        #try:
        if True:
            resp = requests.post(endpoint+'/getips',data=requestd)
            self.compat_ip_list = resp
            for k in resp.json.keys():
                self.kvstore[k] = resp.json()[k]
        #except:
            #print("Get IP: Unable to update upstream server")

    def get_messages(self):
        global endpoin
        while True:
            sleep(2)
            if self.stop_polling:
                return
            #try:
            if True:
                resp = requests.get(endpoint+'/getmessages', data={'user':self.id})
                if resp.status_code == 200:
                    msgDict = {}
                    msgList = resp.json()['messages']
                    for msgData in msgList:
                        sender, msg = json.loads(msgData).popitem()
                        if sender not in msgDict:
                            msgDict[sender] = []
                        msgDict[sender].append(msg)
                    for sender, msgList in msgDict.items():
                        chat_history_update(sender,msgList)
            #except:
                #print("Get Message: Unable to update upstream server")

    def send_message(self, toUID, message):
        global endpoint
        #try:
        if True:
            resp = requests.post(endpoint+'/postmessages', data={'fromuser':self.id, 'touser':toUID, 'message':message})
            if resp.status_code == 200 and resp.json()['result'] == "Success":
                print("Message sent")
            else:
                print("Message not sent")
        #except:
            #print("Send Message: Unable to update upstream server")


def showmenu():
    print("""1. Register
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
    uobject.collect_data()
    print("User Created Successfully!")
    print("Enter help for commandlist")
    poller = None
    while(1):
        cmd = input(">>")
        if cmd == "help":
            showmenu()
        elif cmd == "1":
            uobject.register()
        elif cmd == "2":
            uobject.login()
            if poller is None:
                poller = threading.Thread(target=uobject.get_messages)
                poller.start()
        elif cmd == "3":
            print(uobject.kvstore)
        elif cmd == "4":
            usr_name = input('Enter Username: ')
            #os.system("x-terminal-emulator -e watch -t cat " + usr_name)
            proc = subprocess.Popen(['gnome-terminal --disable-factory -x watch -t cat '+ usr_name], shell = True)
            while(1):
                msg = send_msg(usr_name, uobject.id, proc)
                if msg == None:
                    break
                uobject.send_message(usr_name, msg)
        elif cmd == "5":
            print("Profile for",uname,":")
            print(uobject.attrs)
        elif cmd == "6":
            uobject.stop_polling = 1
            print("Waiting for poll thread to exit")
            poller.join()
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
