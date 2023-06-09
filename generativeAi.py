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

openai.api_key = ''


prompts = [
    "Discuss the historical significance and impact of",
    "Explain the major factors that contributed to",
    "Explore the key individuals who played a significant role in",
    "Describe the social, political, and economic changes during"
    ]

for prompt in prompts:
    
    full_prompt = f"{prompt} {query}"
    
    response = openai.ChatCompletion.create(
            model = 'gpt-3.5-turbo',
            messages=[{"role": "system", "content": "You are a friendly and helpful teaching assistant. You explain concepts about world history based on the doc provided."},
                      {"role": "system", "content": f"{doc_text}"},
                      {"role": "user", "content": f"{full_prompt}"},],
            max_tokens = 50,
            n=1,
            temperature = 0.7
        )
    
generated_answer = response['choices'][0]['message']['content']

