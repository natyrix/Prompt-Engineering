# Prompt-Engineering
Prompt Engineering: In-context learning with GPT-3 and other Large Language Models 

**Table of Contents**

- [Prompt-Engineering](#Prompt-Engineering)
  - [Overview](#overview)
  - [About](#about)
  - [Project Structure](#project-structure)
    - [.dvc](#.dvc)
    - [.github](#.github)
    - [data](#data)
    - [notebooks](#notebooks)
    - [scripts](#scripts)
    - [tests](#tests)
    - [root folder](#root-folder)
  - [Installation guide](#Installation-guide)

***

## Overview

This repository is used for week 4 challenge of 10Academy. The instructions for this project can be found in the challenge document.

Large Language Models coupled with multiple AI capabilities are able to generate images and text, and also approach/achieve human level performance on a number of tasks.  The world is going through a revolution in art (DALL-E, MidJourney, Imagine, etc.), science (AlphaFold), medicine, and other key areas, and this approach is playing a role in this revolution.

## About
In-context learning, popularized by the team behind the GPT-3 LLM, brought a new revolution for using LLMs in many tasks that the LLM was not originally not trained for. This stands in contrast to the usual fine-tuning that used to be required to equip AI models to improve performance in tasks they were not trained for. 

With in-context learning, LLMs are able to constantly adjust their performance on a task depending on the prompt - from structured input that can be considered partly a few-shot training and partly a test input. This has opened up many applications.

The task is to systematically explore strategies that help generate prompts for LLMs to extract relevant entities from job descriptions and also to classify web pages given only a few examples of human scores.


![Alt text](img.png?raw=true "Propmt Engineering")



## Project Structure
The repository has a number of files including python scripts, jupyter notebooks, raw and cleaned data, and text files. Here is their structure with a brief explanation.


### .dvc
- Data Version Control configurations

### .github
- a configuration file for github actions and workflow
- `workflows/CML.yml` continous machine learning configuration

### data
- the folder where the raw, and cleaned datasets' csv files are stored

### notebooks
- `job_description_eda.ipynb`: a jupyter notebook that Explanatory Data Analysis
- `job_description_prompt.ipynb`: a jupyter notebook for testing different techniques of engineering a prompt for out LLM


### scripts
- Different python utility scripts that have different purposes.

### tests
- `test_cleaner.py`: Unittest script for cleaning job description json data

### root folder
- `requirements.txt`: a text file lsiting the projet's dependancies
- `.gitignore`: a text file listing files and folders to be ignored
- `README.md`: Markdown text with a brief explanation of the project and the repository structure.
- `app.py`: Entry point of our flask application.


## Installation guide
Option 1
```
git clone https://github.com/natyrix/Prompt-Engineering
cd Prompt-Engineering
pip install -r requirements.txt 
```
Option 2
```
git clone https://github.com/natyrix/Prompt-Engineering
cd Prompt-Engineering
pip install .
```

