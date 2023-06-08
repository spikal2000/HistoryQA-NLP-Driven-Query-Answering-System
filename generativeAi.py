# -*- coding: utf-8 -*-
"""
Created on Thu Jun  8 23:06:00 2023

@author: spika
"""
from IRmodel import TextSearchEngine
import openai

search_engine = TextSearchEngine('output.csv')
query = 'what can you tell me about Greece'
results = search_engine.search(query, 5)
# for result in results:
#     print(result)

openai.api_key = ''


prompts = [
    "Explain the specific events"
    ]


for prompt in prompts:
    
    full_prompt = f"{prompt} {query}"
    
    response = openai