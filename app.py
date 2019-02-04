from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

secret_endpoint = os.environ['secret_endpoint']

from models import *
from graphs import SensorGrapher

def root_dir():  # pragma: no cover
    return os.path.abspath(os.path.dirname(__file__))

def get_file(filename):  # pragma: no cover
    try:
        src = os.path.join(root_dir(), filename)
        # Figure out how flask returns static files
        # Tried:
        # - render_template
        # - send_file
        # This should not be so non-obvious
        return open(src).read()
    except IOError as exc:
        return str(exc)

@app.route('/')
def hello():
    path = os.path.join(root_dir(), 'templates/index.html')
    return render_template('index.html')

@app.route('/'+secret_endpoint)
def make_graphs():
    grapher = SensorGrapher()
    grapher.fetch_df()
    grapher.plot_moisture_data()    
    grapher.plot_temp_data()
    grapher.plot_light_data()
    grapher.plot_humid_data()
    return "graphs made"
    

if __name__ == '__main__':
    app.run(debug=True)
