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
    try:
        if request.method == 'POST':
            j_d = request.form['j_d']
            ch_model = request.form['model']
            prompt_type = request.form['prompt_type']
            # print(j_d)
            if len(j_d.strip()) == 0:
                raise Exception("Job Description required")
            else:
                model = 'xlarge'
                if int(ch_model) != 1:
                    model = '544c8386-258a-4615-8fae-ce64d4255556-ft'
                jdpipeline = JDPipeline(j_d, model=model, prompt_type=int(prompt_type))
                response,val = jdpipeline.make_request()
                # print(jdpipeline.pr_data)
                return render_template('home.html', title='Home', error_text='', response=response, process_dict=val)
                
        
        return render_template('home.html', title='Home', error_text='')
    except Exception as e:
        return render_template('home.html', title='Home', error_text=str(e))
        



@app.route('/docs')
def docs():
    return render_template('docs.html', title='Home')



if __name__ == '__main__':  
   app.run(debug = True)  