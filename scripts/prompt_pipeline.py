import sys
import os

sys.path.append(os.path.abspath(os.path.join("./scripts/")))
from logger import logger
class PromptPipeline():
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
        s: str = 'Job Description: '
        try:
            for d in data:
                s+=d['text']
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
                    if token['entityLabel'] in token_dict.keys():
                        token_dict['entityLabel']+=f",{token['text']}"
                dict_str = ''
                for key,value in token_dict.iteritems():
                    dict_str+=f"{key}: {value}\n"
                s+=dict_str
                s+='\n--\n'
            logger.info("Values extracted.")
            return s
        except Exception as e:
            logger.error(e)
    
    


