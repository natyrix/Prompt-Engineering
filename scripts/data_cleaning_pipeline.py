import json
import sys
import os

sys.path.append(os.path.abspath(os.path.join("./scripts/")))
from logger import logger

class DataCleaningPipeline():
    def __init__(self) -> None:
        pass

    def loader(self, file_path="../data/job_description_train.json"):
        try:
            data = []
            with open(file_path) as f:
                data = json.loads(f.read())
            
            return data
        except Exception as e:
            logger.error(e)

