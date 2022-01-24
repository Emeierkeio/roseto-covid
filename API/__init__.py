import flask
from flask import request, jsonify
import json
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


app = flask.Flask(__name__)
app.config["DEBUG"] = True
limiter = Limiter(app, key_func=get_remote_address)

# Open the file roseto.json
with open('../data/roseto.json') as json_file:
    data = json.load(json_file)
    

@app.route('/api/all', methods=['GET'])
def api_all():
    return jsonify(data)

@app.route('/')
def home():
    return '''<h1>Roseto API</h1>
<p>API Roseto.</p>'''



@app.route('/data', methods=['GET'])
@limiter.limit("10/minute")
def api():
    if 'month' in request.args:
        month = request.args['month']
        type = 'm'
    elif 'year' in request.args:
        year = request.args['year']
        type = 'y'
    elif 'day' in request.args:
        day = request.args['day']
        type = 'd'
    else:
        return "Error"

    # Create an empty list for our results
    results = []

    # Loop through the data and match results that fit the requested ID.
    # IDs are unique, but other fields might return many results
    if type == 'm':
        for row in data:
            if '-{}-'.format(month) in row['data']:
                results.append(row)
    elif type == 'd':
        for row in data:
            if row['data'] == day:
                results.append(row)
    elif type == 'y':
        for row in data:
            if '{}-'.format(year) in row['data']:
                results.append(row)


    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(results)

app.run()
