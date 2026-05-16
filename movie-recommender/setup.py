import pandas as pd
import pickle
import ast
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

movies = pd.read_csv('tmdb_5000_movies.csv')
credits = pd.read_csv('tmdb_5000_credits.csv')
movies = movies.merge(credits, on='title')
movies = movies[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]

def extract_names(obj):
    try:
        if isinstance(obj, str):
            obj = ast.literal_eval(obj)
        return [item['name'] for item in obj]
    except:
        return []

def extract_director(obj):
    try:
        if isinstance(obj, str):
            obj = ast.literal_eval(obj)
        for item in obj:
            if item['job'] == 'Director':
                return [item['name']]
        return []
    except:
        return []

def extract_top_actors(obj, top=3):
    try:
        if isinstance(obj, str):
            obj = ast.literal_eval(obj)
        return [item['name'] for item in obj[:top]]
    except:
        return []

movies['genres'] = movies['genres'].apply(extract_names)
movies['keywords'] = movies['keywords'].apply(extract_names)
movies['cast'] = movies['cast'].apply(lambda x: extract_top_actors(x, top=3))
movies['crew'] = movies['crew'].apply(extract_director)

def create_tags(row):
    tags = []
    tags.extend(row['genres'])
    tags.extend(row['keywords'])
    tags.extend(row['cast'])
    tags.extend(row['crew'])
    if isinstance(row['overview'], str):
        tags.append(row['overview'])
    return ' '.join(tags).lower()

movies['tags'] = movies.apply(create_tags, axis=1)

vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
vectors = vectorizer.fit_transform(movies['tags'])
similarity = cosine_similarity(vectors)

os.makedirs('model', exist_ok=True)
movie_data = movies[['movie_id', 'title']]
with open('model/movie_data.pkl', 'wb') as f:
    pickle.dump((movie_data, similarity), f)

movie_list = movies['title'].values
with open('model/movie_list.pkl', 'wb') as f:
    pickle.dump(movie_list, f)

print("✅ Setup complete. Now run: streamlit run app.py")