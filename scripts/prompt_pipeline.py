import sys
import os

sys.path.append(os.path.abspath(os.path.join("./scripts/")))
from logger import logger
class PromptPipeline():
    def __init__(self, currernt_technique='technique1') -> None:
        self.techniques_list = ['technique1']
        self.currernt_technique = currernt_technique

    def send_request_to_cohere(self, co, prompt):
        """
            Sends an API request to cohere and reuturns the response
        """
        response = co.generate( 
            model='xlarge', 
            prompt=prompt, 
            max_tokens=400, 
            temperature=0.5, 
            k=0, 
            p=1, 
            frequency_penalty=0, 
            presence_penalty=0, 
            stop_sequences=["--"], 
            return_likelihoods='NONE')
        
        return response.generations[0].text

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

    def process_response(response):
        response = str(response).strip()


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
                s+=d['document']
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
    



