import unittest
import pandas as pd
import sys
import os
import json


#Prompt-Engineering
sys.path.append(os.path.abspath(os.path.join("../Prompt-Engineering/")))

from scripts import data_cleaning_pipeline

class TestDataClean(unittest.TestCase):
    def setUp(self) -> None:
        self.cleaner = data_cleaning_pipeline.DataCleaningPipeline()
        with open('./tests/sample.json', 'r') as f:
            self.data = json.loads(f.read())

    def test_remove_irrelevant_pairs(self):
        self.cleaner.remove_irrelevant_pairs(self.data, 'relations')
        self.assertEqual(list(self.data.keys()), ['document', 'tokens'])


if __name__ == "__main__":
    unittest.main()
