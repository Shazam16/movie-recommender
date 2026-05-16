import streamlit as st
import pickle
import requests
import concurrent.futures

st.set_page_config(page_title="🎬 Movie Recommender", page_icon="🎥", layout="wide")

@st.cache_resource
def load_model():
    with open('model/movie_data.pkl', 'rb') as f:
        movies_df, similarity_matrix = pickle.load(f)
    with open('model/movie_list.pkl', 'rb') as f:
        movie_list = pickle.load(f)
    return movies_df, similarity_matrix, movie_list

movies_df, similarity, movie_list = load_model()

TMDB_API_KEY = st.secrets.get("TMDB_API_KEY", "YOUR_API_KEY_HERE")
POSTER_BASE = "https://image.tmdb.org/t/p/w500"

@st.cache_data(ttl=3600, show_spinner=False)
def fetch_movie_details(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US"
        res = requests.get(url, timeout=5)
        res.raise_for_status()
        data = res.json()
        poster_path = data.get("poster_path")
        poster_url = f"{POSTER_BASE}{poster_path}" if poster_path else "https://via.placeholder.com/300x450?text=No+Poster"
        rating = data.get("vote_average", "N/A")
        year = data.get("release_date", "N/A")[:4] if data.get("release_date") else "N/A"
        return poster_url, rating, year
    except:
        return "https://via.placeholder.com/300x450?text=Error", "N/A", "N/A"

def recommend_movies(title, top_n=6):
    idx = movies_df[movies_df['title'] == title].index[0]
    sim_scores = list(enumerate(similarity[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:top_n+1]
    movie_indices = [s[0] for s in sim_scores]
    recommended_ids = movies_df.iloc[movie_indices]['movie_id'].values
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        details = list(executor.map(fetch_movie_details, recommended_ids))
    
    results = []
    for i, idx in enumerate(movie_indices):
        results.append({
            'title': movies_df.iloc[idx]['title'],
            'poster': details[i][0],
            'rating': details[i][1],
            'year': details[i][2],
        })
    return results

st.markdown("<h1 style='text-align: center;'>🎬 Movie Recommender System</h1>", unsafe_allow_html=True)
selected_movie = st.selectbox("Select a movie you like", movie_list)
if st.button("Recommend"):
    with st.spinner("Finding similar movies..."):
        recs = recommend_movies(selected_movie)
    cols = st.columns(3)
    for i, rec in enumerate(recs):
        with cols[i % 3]:
            st.image(rec['poster'], use_container_width=True)
            st.markdown(f"**{rec['title']}**<br>⭐ {rec['rating']}  •  {rec['year']}", unsafe_allow_html=True)