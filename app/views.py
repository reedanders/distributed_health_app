from flask import request, jsonify,abort
import numpy as np
import redis
import json

from app import app
from featureMatrix import FeatureMatrix

import querySpark

registered_ids = {}
logged_in=[]

r = redis.StrictRedis(host='localhost', port=6379, db=0)

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/update', methods=['POST'])
def update():
    if request.method == 'POST':
        user = request.values['user']
        vector = request.values['vector']
        if user not in logged_in:
            abort(404)
        vector = np.fromstring(vector, dtype=float, sep=',')

        if True:
            fm = FeatureMatrix()
            # nearest_neighbor = fm.match('A', np.array([.1,.2,.3,.5]))
            nearest_neighbor = fm.match(user, vector)
        else:
            nearest_neighbor = querySpark.match(user, vector)

        return jsonify(result='Success',
                            neighbor=nearest_neighbor)


@app.route('/login',methods=['POST'])
def login():
    if request.method == 'POST':
        remote_ip = request.remote_addr
        print("Login from client IP",remote_ip)
        user = request.values['user']
        pwd = request.values['password']
        if user in logged_in:
            return jsonify(result='Success')
        if user in registered_ids.keys():
            if registered_ids[user] == pwd:
                print("logging in",user)
                logged_in.append(user)
                #r.set(user,str(remote_ip))
                return jsonify(result='Success')
        else:
            abort(404)

@app.route('/logout',methods=['POST'])
def logout():
    if request.method == 'POST':
        user = request.values['user']
        print("logging out",user)
        logged_in.remove(user)
        return jsonify(result='Success')

@app.route('/register',methods=['POST'])
def register():
    if request.method == 'POST':
        user = request.values['user']
        pwd = request.values['password']
        print("Registering",user)
        if user not in registered_ids.keys():
            registered_ids[user] = pwd
        return jsonify(result='Success')

@app.route('/getips',methods=['POST'])
def getips():
    user = request.values['user']
    userids = request.values['userids']
    print("username:",user)
    if user not in logged_in:
        abort(404)
    returnvalue = {}
    for uid in userids:
        returnvalue[uid] = r.get(uid)
    return jsonify(returnvalue)

@app.route('/postmessages',methods=['POST'])
def postmessages():
    fromuser = request.values['fromuser']
    touser = request.values['touser']
    message = request.values['message']
#    if touser not in logged_in:
#        abort(404)
    if r.lpush(touser,json.dumps({fromuser:message})) > 0 :
        return jsonify(result='Success')
    else:
        return jsonify(result='Failure')

@app.route('/getmessages',methods=['GET'])
def getmessages():
    user = str(request.values['user'])
    print(user)
    resp = {'messages': []}
#    if user not in logged_in:
#        abort(404)
    while True:
        data = r.rpop(user)
        if data is not None:
            resp['messages'].append(data.decode())
        else:
            return jsonify(resp)
