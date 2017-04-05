from flask import request, jsonify,abort
import numpy as np

from app import app
from featureMatrix import FeatureMatrix

registered_ids = {}
logged_in=[]

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
        fm = FeatureMatrix()
        # nearest_neighbor = fm.match('A', np.array([.1,.2,.3,.5]))
        nearest_neighbor = fm.match(user, vector)
        return jsonify(result='Success',
                            neighbor=nearest_neighbor)

@app.route('/login',methods=['POST'])
def login():
    if request.method == 'POST':
        user = request.values['user']
        pwd = request.values['password']
        if user in logged_in:
            return jsonify(result='Success')
        if user in registered_ids.keys():
            if registered_ids[user] == pwd:
                print("logging in",user)
                logged_in.append(user)
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
