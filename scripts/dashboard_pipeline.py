from select import select
import sys
import os
import json
from urllib import response
import matplotlib.pyplot as plt
import operator
import cohere
from cohere.classify import Example
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.svm import SVC
from sklearn import preprocessing
import cohere
import random
from dotenv import load_dotenv
from difflib import SequenceMatcher

sys.path.append(os.path.abspath(os.path.join("./scripts/")))
from logger import logger


class JDPipeline():
    def __init__(self, inputval, model='xlarge', prompt_type=1,num_tokens=100, example_num=3) -> None:
        self.data = {}
        with open('./data/job_description_train_cleaned_1.json', 'r') as f:
            self.data = json.loads(f.read())
        self.inputval = inputval
        self.model = model
        self.num_tokens = num_tokens
        self.example_num = example_num
        self.prompt_type = prompt_type
        API_KEY = os.getenv('API_KEY')
        self.co = cohere.Client(API_KEY)
    
    def make_request(self):
        self.preprocess()
        self.prepare_prompt()
        response = self.send_request()
        trial = 0
        max_tries = 3
        response = response.replace('--', '').strip()
        while len(response) < 10:
            trial+=1
            if trial > max_tries:
                break
            response = self.send_request()
            response = response.replace('--', '').strip()
        if len(response) < 10:
            raise Exception("Can not get a meaningful response, please try to use different model")
        else:
            if self.model=='xlarge':
                return self.post_process(response), True
            return response, False

    def post_process(self, response):
        response = str(response).strip().split('\n')
        response_dict = {}
        for vl in response:
            try:
                splitted_val = vl.split(':')
                response_dict[splitted_val[0]] = splitted_val[1]
            except Exception as e:
                pass

        return response_dict




    def send_request(self):
        prompt = self.pr_data
        prompt+=f'Job Description: {self.inputval}'
        # logger.info(prompt)

        # try:
        response = self.co.generate( 
            model=self.model, 
            prompt=prompt, 
            max_tokens=self.num_tokens, 
            temperature=0.5, 
            k=0, 
            p=1, 
            frequency_penalty=0, 
            presence_penalty=0, 
            stop_sequences=["--"], 
            return_likelihoods='NONE')
        logger.info("Rquest successful")
        return response.generations[0].text
        # except Exception as e:
        #     logger.error(e)

    
    def preprocess(self):
        self.inputval = str(self.inputval).strip().replace('/n', ' ')

    def prepare_prompt(self):
        p_val = self.prompt_type
        if p_val == 1:
            prompt_data = []
            similarity = {}
            for i, d in enumerate(self.data):
                similarity[i] = SequenceMatcher(None, self.inputval, d['document']).ratio()
            sorted_dict = dict( sorted(similarity.items(), key=operator.itemgetter(1),reverse=True))
            max_p = self.example_num
            i = 0
            for k,v in sorted_dict.items():
                prompt_data.append(self.data[k])
                i+=1
                if i>=max_p: break
            self.pr_data = self.extract_values(prompt_data)
        else:
            rand_items = random.sample(self.data, self.example_num)
            self.pr_data = self.extract_values(rand_items)
    

    def extract_values(self, data):
        """
            We will extract the values from each json dictionaries and
            convert them to a prompt types as the following

            Job Description: Bachelor's degree in Mechanical Engineering or Physical Science 3+ years track record of developing or 
            specifying fiber optic cables and connector related products Knowledge of fiber optic component, cabling,
            and interconnect products, technologies, and standards Experience in statistical data analysis Experience
            with product life cycle management (PLM) process Experience providing solutions to problems and meeting
            deadlines Experience engaging stakeholders PREFERRED Advanced degree Experience using a software tool
            for statistical data analysis such as JMP Experience using Agile as product life-cycle management tool Data center
            or other mission critical development experience

            DIPLOMA: Bachelor
            DIPLOMA_MAJOR: Mechanical Engineering, Physical Science
            EXPERIENCE: 3+ years
            SKILLS: developing, fiber optic cables, connector related products
        """
        s: str = ''
        # try:
        for d in data:
            s+='Job Description: '
            s+=str(d['document']).strip().replace('\n', ' ').strip()
            s+='\n'
            """
                Extract entities from tokens
                to conver them to the following 
                    DIPLOMA: Bachelor
                    DIPLOMA_MAJOR: Mechanical Engineering, Physical Science
                    EXPERIENCE: 3+ years
                    SKILLS: developing, fiber optic cables, connector related products
            """
            token_dict = {}
            for token in d['tokens']:
                entity_label = token['entityLabel']
                if entity_label in token_dict.keys():
                    token_dict[entity_label] += f",{token['text']}"
                else:
                    token_dict[entity_label] = f"{token['text']}"
            dict_str = ''
            for key,value in token_dict.items():
                dict_str+=f"{key}: {value}\n"
            s+=dict_str
            s+='\n--\n'
        logger.info("Values extracted.")
        return s
        # except Exception as e:
        #     logger.error(e)
    


class NewsPipeline():
    def __init__(self, title, desc, body, model=1) -> None:
        self.title = title
        self.desc = desc
        self.body = body
        self.model = model
        self.df = pd.read_csv('./data/news_processed.csv')
        API_KEY = os.getenv('API_KEY')
        self.co = cohere.Client(API_KEY)

    def make_score(self):
        self.preprocess_inputs()
        if self.model == 1:
            result = self.do_classify()
            return self.post_process(result)
        else:
            result = self.do_embed()
            return result[0]

    def post_process(self, res):
        result = str(res).split('__')
        print(result)
        num_result = ''
        num_result += str(int(result[1].split('_')[1]) - 1)
        num_result +='.'
        num_result += str(int(result[2].split('_')[1]) - 1)
        num_result += str(int(result[3].split('_')[1]) - 1)
        return num_result




    def preprocess_inputs(self):
        self.title = str(self.title).strip().replace('\n', ' ').strip()
        self.body = str(self.body).strip().replace('\n', ' ').strip()
        self.desc = str(self.desc).strip().replace('\n', ' ').strip()

    def do_classify(self):
        X,y = self.df['Title'], self.df['final_score']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=1, random_state=21)
        intents = y_train.unique().tolist()
        ex_texts, ex_labels = [], []
        for intent in intents:
            ex_texts += X_train.tolist()
            ex_labels += y_train.tolist()
        examples = list()
        for txt, lbl in zip(ex_texts,ex_labels):
            examples.append(Example(txt,lbl))
        def classify_text(text,examples):
            classifications = self.co.classify(
                model='xlarge',
                inputs=[text],
                examples=examples
                )
            return classifications.classifications[0].prediction
        return classify_text(self.title, examples=examples)

    
    def do_embed(self):
        X,y = self.df['desc_context_txt'], self.df['final_score']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=1, random_state=21)
        def embed_text(text):
            output = self.co.embed(model='medium',texts=text)
            return output.embeddings
        X_train_emb = np.array(embed_text(X_train.tolist()))
        X_test_emb = np.array(embed_text([self.desc]))

        le = preprocessing.LabelEncoder()
        le.fit(y_train)
        y_train_le = le.transform(y_train)
        y_test_le = le.transform(y_test)

        # Initialize the model
        svm_classifier = SVC(class_weight='balanced')

        # Fit the training dataset to the model
        svm_classifier.fit(X_train_emb, y_train_le)

        return svm_classifier.predict(X_test_emb)


