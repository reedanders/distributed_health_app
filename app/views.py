from flask import request, jsonify

from app import app
from featureMatrix import FeatureMatrix

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/update', methods=['GET','POST'])
def update():
    if request.method == 'POST':
        user = request.args.get('user')
        vector = request.args.get('vector')


        import pdb; pdb.set_trace()

        fm = FeatureMatrix()

        # nearest_neighbor = fm.match('A', np.array([.1,.2,.3,.5]))
        nearest_neighbor = fm.match(user, vector)

        return jsonify(result='Success',
                            data=nearest_neighbor)
