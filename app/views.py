from flask import request, jsonify
import numpy as np

from app import app
from featureMatrix import FeatureMatrix

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/update', methods=['POST'])
def update():
    if request.method == 'POST':
        user = request.values['user']

        vector = request.values['vector']
        vector = np.fromstring(vector, dtype=float, sep=',')

        fm = FeatureMatrix()
        # nearest_neighbor = fm.match('A', np.array([.1,.2,.3,.5]))
        nearest_neighbor = fm.match(user, vector)

        return jsonify(result='Success',
                            data=nearest_neighbor)
