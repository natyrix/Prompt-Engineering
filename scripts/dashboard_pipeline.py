import sys
import os
import matplotlib.pyplot as plt
from difflib import SequenceMatcher

sys.path.append(os.path.abspath(os.path.join("./scripts/")))
from logger import logger


class JDPipeline():
    def __init__(self, inputval, model='xlarge') -> None:
        self.data = {}


