from flask import *
import pandas as pd
import numpy as np
import pickle
import os,sys
import json

sys.path.append(os.path.abspath(os.path.join("./scripts/")))
from logger import logger
from dashboard_pipeline import JDPipeline

app = Flask(__name__, static_folder='staticFiles') 



@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':

        return render_template('home.html', title='Home')
    
    return render_template('home.html', title='Home')
    



@app.route('/docs')
def docs():
    return render_template('docs.html', title='Home')



if __name__ == '__main__':  
   app.run(debug = True)  