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
doc = [result['body_text'] for result in results]

doc_text = ' '.join(doc)

openai.api_key = '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'


prompts = [
    "Explain the specific events"
    ]


for prompt in prompts:
    
    full_prompt = f"{prompt} {query}"
    
    response = openai.Completion.create(
            model = 'gpt-3.5-turbo',
            prompt = full_prompt,
            documents=doc_text,
            max_tokens = 20,
            n=1,
            stop=None,
            temperature = 0.7
        )
    
generated_answer = response.choices[0].message.content

