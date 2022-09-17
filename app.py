from crypt import methods
from pyexpat import model
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


"""
API
"""
@app.route('/api/bnewscore', methods=['GET', 'POST'])
def bnewscore():
    if request.method == "GET":
        return jsonify({
            "success": True,
            "message": "Send news on post method to see results \n got to api/docs for more info"
        })
    else:
        return jsonify({
            "success": True,
            "message": "POSTED ON NEWS"
        })

@app.route('/api/jdentities', methods=['GET', 'POST'])
def jdentities():
    if request.method == "GET":
        return jsonify({
            "success": True,
            "message": "Send Job Description on post method to see results\n got to api/docs for more info"
        })
    else:
        try:
            data = request.json 
            j_d = data['j_d']
            ch_model = data.get('model') if data.get('model') else 'xlarge'
            pr_type = data.get('prompt_type') if data.get('prompt_type') else 1

            if j_d:
                model = 'xlarge'
                if ch_model != 1 and ch_model != 'xlarge':
                    model = '544c8386-258a-4615-8fae-ce64d4255556-ft'
                if ch_model == 1:
                    model = 'xlarge'
                if pr_type == 1 or pr_type == 2:
                    jdpipeline = JDPipeline(j_d, model=model, prompt_type=int(pr_type))
                    response,val = jdpipeline.make_request()

                    return jsonify({
                        "success": True,
                        "message": "Entity Extracted",
                        "response": response
                    })
                else:
                    return jsonify({
                        "success": False,
                        "message": "Invalid prompt type. 1 or 2 is accpeted"
                    })
            else:
                return jsonify({
                    "success": False,
                    "message": "Job Description Required."
                })
        except Exception as e:
            return jsonify({
                    "success": False,
                    "message": str(e)
                })


if __name__ == '__main__':  
   app.run(debug = True)  