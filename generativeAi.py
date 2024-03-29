# -*- coding: utf-8 -*-
"""
Created on Thu Jun  8 23:06:00 2023

@author: spika
"""
from IRmodel import TextSearchEngine
import openai

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

search_engine = TextSearchEngine('output.csv')
query = 'what is the Berlin wall? '
results = search_engine.search(query, 5)
# for result in results:
#     print(result)
doc = [result['body_text'] for result in results]

doc_text = ' '.join(doc)

openai.api_key = ''
#Bert
# Load the model
model = SentenceTransformer('all-MiniLM-L6-v2')
# Calculate embedding for the query
query_embedding = model.encode([query])

all_generated_answers = []
# Calculate cosine similarity between the query and each generated answer
similarities = []


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
            messages=[{"role": "system", "content": "You are a friendly and helpful teaching assistant. You explain concepts about world history only based on the doc provided."},
                      {"role": "system", "content": f"{doc_text}"},
                      {"role": "user", "content": f"{full_prompt}"},],
            max_tokens = 50,
            n=1,
            temperature = 0.7
        )
    
    generated_answer = response['choices'][0]['message']['content']
    all_generated_answers.append(generated_answer)
    
    # Calculate embedding for the answer
    answer_embedding = model.encode([generated_answer])
    
    # Calculate and save the cosine similarity
    similarity = cosine_similarity(query_embedding, answer_embedding)
    similarities.append(similarity[0][0])

# Find the answer with the highest similarity
best_answer_index = np.argmax(similarities)
best_answer = all_generated_answers[best_answer_index]

