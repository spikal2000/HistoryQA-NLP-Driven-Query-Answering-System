# -*- coding: utf-8 -*-
"""
Created on Thu Jun  8 22:53:36 2023

@author: spika
"""

import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
import time
import faiss
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import csv
import nltk
# nltk.download('stopwords')

# Function Definitions
def preprocess_text(text, porter):
    line = text.strip()
    tokens = word_tokenize(line)
    words = [word.lower() for word in tokens if word.isalpha()]
    tokens_without_sw = [word for word in words if not word in stopwords.words('english')]
    stemmed = [porter.stem(word) for word in tokens_without_sw]
    return " ".join(stemmed)

def get_similar_lyrics(q, df2, df):
    # Convert the query become a vector
    q = [q]
    q_vec = vectorizer.transform(q).toarray().reshape(df2.shape[0],)
    sim = {}
    # Calculate the similarity
    for i in range(df2.shape[1]):
        sim[i] = np.dot(df2.loc[:, i].values, q_vec) / np.linalg.norm(df2.loc[:, i]) * np.linalg.norm(q_vec)
  
    # Sort the values 
    sim_sorted = sorted(sim.items(), key=lambda x: x[1], reverse=True)
    # Print the lyrics and their similarity values
    x = 0
    top_50_tfidf = []
    last_v = 0.0
    for k, v in sim_sorted:
        if v != 0.0:
            if v != last_v:
                last_v = v
                top_50_tfidf.append(df.iloc[k])
                x += 1
                if x == 50:
                    break;
            else:
                continue
    return top_50_tfidf

def search(query, top_k, index, model):
    t=time.time()
    query_vector = model.encode([query])
    top_k = index.search(query_vector, top_k)
    print('>>>> Results in Total Time: {}'.format(time.time()-t))
    top_k_ids = top_k[1].tolist()[0]
    top_k_ids = list(np.unique(top_k_ids))
    results =  [fetch_lyric_info(idx) for idx in top_k_ids]
    return results

def fetch_lyric_info(dataframe_idx):
    info = df.iloc[dataframe_idx]
    meta_dict = dict()
    meta_dict['number'] = info['number']
    meta_dict['title'] = info['title']
    meta_dict['body_text'] = info['body_text'][:500]
    return meta_dict

# Processing Step 1 - TF-IDF
# Loading and preprocessing the data
porter = PorterStemmer()
df = pd.read_csv ('output.csv', names=['index','number','title','body_text'], sep=',', skiprows=1, encoding='latin-1')

# Preprocessing body_text
df['body_text_processed'] = df['body_text'].apply(lambda x: preprocess_text(x, porter))

# Creating TfidfVectorizer object and transforming the data
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df['body_text_processed'])
X = X.T.toarray()
df2 = pd.DataFrame(X, index=vectorizer.get_feature_names_out())

# Processing the query
query = 'what can you tell me about Greece'
query_processed = preprocess_text(query, porter)

# Calling TF-IDF based matching function
tfidf_results = get_similar_lyrics(query_processed, df2, df)

# Processing Step 2 - Using Sentence Transformers for semantic matching
model = SentenceTransformer('msmarco-distilbert-base-dot-prod-v3')

# Encoding the data and building FAISS index
encoded_data = model.encode(df.body_text.tolist())
encoded_data = np.asarray(encoded_data.astype('float32'))
index = faiss.IndexIDMap(faiss.IndexFlatIP(768))
index.add_with_ids(encoded_data, np.array(range(0, len(df))).astype(np.int64))

# Calling semantic matching function
semantic_results=search(query, top_k=5, index=index, model=model)

for result in tfidf_results:
    print('\t',result)

for result in semantic_results:
    print('\t',result)