# movie-recommender

# 🎬 Content-Based Movie Recommendation System

A machine learning web app that recommends similar movies based on a user’s selection. Built with **Streamlit**, **scikit-learn**, and the **TMDB 5000 dataset**. This project demonstrates how recommendation engines work behind platforms like Netflix and Amazon Prime.

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)

---

## 🚀 Live Demo

👉 [Click here to try the app](https://movie-recommendation-system-mfop.onrender.com)  
*(Note: Free tier may take 20-30 seconds to wake up)*

---

## 📌 Features

- 🎯 **Content‑based filtering** – recommends movies based on plot, genres, cast, crew, and keywords  
- 🖼️ **Live posters** – fetches posters from the TMDB API  
- ⚡ **Fast recommendations** – pre‑computed cosine similarity matrix loaded with `pickle`  
- 🧹 **Clean UI** – built with Streamlit, responsive design  
- 🌍 **Deployed on Render** – accessible from anywhere  

---

## 🛠️ Tech Stack

| Category       | Technology                              |
|----------------|-----------------------------------------|
| Language       | Python 3.9+                             |
| Framework      | Streamlit                               |
| ML & Data      | scikit-learn, Pandas, NumPy, Pickle     |
| API            | TMDB API (posters & details)            |
| Deployment     | Render                                  |

---

## 📂 Dataset

- **TMDB 5000 Movies Dataset** (Kaggle)  
- Contains ~5000 movies with metadata: cast, crew, keywords, budget, revenue, posters, etc.  
- [Download from Kaggle](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata)

---

## ⚙️ How It Works

1. **Preprocessing** – combine `genres`, `keywords`, `cast` (top 3), `director`, and `overview` into a single “tags” column.  
2. **Vectorization** – convert tags into numerical vectors using `TfidfVectorizer`.  
3. **Similarity** – compute **cosine similarity** between all movies.  
4. **Recommendation** – given a movie, return the top N movies with highest similarity scores.  
5. **UI & API** – Streamlit dropdown → fetch posters via TMDB API → display results.

---

## 🏗️ Project Structure
