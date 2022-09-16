import sys
import os
import matplotlib.pyplot as plt
from difflib import SequenceMatcher

sys.path.append(os.path.abspath(os.path.join("./scripts/")))
from logger import logger


class PromptPipeline():

    def __init__(self, currernt_technique='technique1') -> None:
        self.techniques_list = ['technique1']
        self.currernt_technique = currernt_technique

    def send_request_to_cohere(self, co, prompt, model='xlarge'):
        """
            Sends an API request to cohere and reuturns the response
        """
        try:
            response = co.generate( 
                model=model, 
                prompt=prompt, 
                max_tokens=400, 
                temperature=0.5, 
                k=0, 
                p=1, 
                frequency_penalty=0, 
                presence_penalty=0, 
                stop_sequences=["--"], 
                return_likelihoods='NONE')
            logger.info("Rquest successful")
            return response.generations[0].text
        except Exception as e:
            logger.error(e)

    def get_tokens(self, data):
        """
            Returns dictionary form of tokens array in the json
            example:
                "tokens": [
                    {
                        "text": "Bachelor",
                        "entityLabel": "DIPLOMA"
                    },
                    {
                        "text": "Mechanical Engineering",
                        "entityLabel": "DIPLOMA_MAJOR"
                    },
                    {
                        "text": "Physical Science",
                        "entityLabel": "DIPLOMA_MAJOR"
                    },
                    {
                        "text": "3+ years",
                        "entityLabel": "EXPERIENCE"
                    },
                    {
                        "text": "developing",
                        "entityLabel": "SKILLS"
                    },
                    {
                        "text": "fiber optic cables",
                        "entityLabel": "SKILLS"
                    },
                    {
                        "text": "connector related products",
                        "entityLabel": "SKILLS"
                    }

                    in to
                    {
                        "DIPLOMA" : "Bachelor",
                        "DIPLOMA_MAJOR":"Mechanical Engineering, Physical Science",
                        "EXPERIENCE":"3+ years",
                        "SKILLS":"developing, fiber optic cables, connector related products"
                    }
        """
        token_dict = {}
        try:
            for token in data['tokens']:
                entity_label = token['entityLabel']
                if entity_label in token_dict.keys():
                    token_dict[entity_label] += f",{token['text']}"
                else:
                    token_dict[entity_label] = f"{token['text']}"
            logger.info("Tokens converted to Dict")
        except Exception as e:
            logger.error(e)
        return token_dict

    def process_response(self,response):
        """
            convert the response to dict with entities as key and answer as value
            '\nDIPLOMA: Bachelor\nDIPLOMA_MAJOR: Mechanical Engineering,
            Physical Science\nEXPERIENCE: 3+ years\nSKILLS: developing,fiber optic cables,connector related products\n\n--'
            converted to
            {'DIPLOMA': ' Bachelor',
            'DIPLOMA_MAJOR': ' Mechanical Engineering,Physical Science',
            'EXPERIENCE': ' 3+ years',
            'SKILLS': ' developing,fiber optic cables,connector related products'}
            Later used for plotting accuracy
        """
        response = str(response).strip().split('\n')
        response_dict = {}
        for vl in response:
            try:
                splitted_val = vl.split(':')
                response_dict[splitted_val[0]] = splitted_val[1]
            except Exception as e:
                pass

        return response_dict

    def get_prediction_similarity(self, token_dict, response_dict):
        """
            Get each entities prediction similarity ration which is used for plotting similarity
        """
        try:
            prediction_similarity = {}
            for k,v in token_dict.items():
                if k in response_dict.keys():
                    prediction_similarity[k] = SequenceMatcher(None, v, response_dict[k]).ratio()
                else:
                    prediction_similarity[k] = 0.0
            return prediction_similarity
        except Exception as e:
            logger.error(e)
            return {}

    def plot_result(self, result):
        try:
            plt.bar(range(len(result)), list(result.values()), align='center')
            plt.xticks(range(len(result)), list(result.keys()))
            # # for python 2.x:
            # plt.bar(range(len(D)), D.values(), align='center')  # python 2.x
            # plt.xticks(range(len(D)), D.keys())  # in python 2.x
            plt.show()
            logger.info("Plotted result")
        except Exception as e:
            logger.error(e)


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
        try:
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
        except Exception as e:
            logger.error(e)
    



