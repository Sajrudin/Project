from flask import Flask, request, jsonify, render_template
import numpy as np
import pandas as pd
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import requests
import webbrowser
import threading

app = Flask(__name__)

# Load and validate the dataset
try:
    movies_data = pd.read_csv('movies.csv')
    required_columns = ['genres', 'keywords', 'tagline', 'cast', 'director', 'title']
    for col in required_columns:
        if col not in movies_data.columns:
            raise ValueError(f"Missing column: {col}")
except Exception as e:
    raise RuntimeError(f"Failed to load movies.csv: {e}")

# Fill NaN and combine features
selected_features = ['genres', 'keywords', 'tagline', 'cast', 'director']
movies_data[selected_features] = movies_data[selected_features].fillna('')
combined_features = movies_data['genres'] + ' ' + movies_data['keywords'] + ' ' + \
                    movies_data['tagline'] + ' ' + movies_data['cast'] + ' ' + movies_data['director']

# Convert text to vectors and compute similarity
vectorizer = TfidfVectorizer()
feature_vectors = vectorizer.fit_transform(combined_features)
similarity = cosine_similarity(feature_vectors)

# Fetch movie poster
def fetch_movie_poster(movie_title):
    try:
        api_key = 'ee983e73525efed3d4b7cad1e91dd7cb'
        base_url = 'https://api.themoviedb.org/3'
        search_url = f'{base_url}/search/movie'
        params = {'api_key': api_key, 'query': movie_title}
        response = requests.get(search_url, params=params)
        response.raise_for_status()
        results = response.json().get('results')
        if results:
            poster_path = results[0].get('poster_path')
            return f'https://image.tmdb.org/t/p/w500{poster_path}' if poster_path else ''
    except requests.exceptions.RequestException as e:
        print(f"Error fetching poster: {e}")
    return ''

# Get movie recommendations
def get_movie_recommendations(movie_name):
    list_of_all_titles = movies_data['title'].tolist()
    find_close_match = difflib.get_close_matches(movie_name, list_of_all_titles)

    if not find_close_match:
        return []

    close_match = find_close_match[0]
    index_of_the_movie = movies_data[movies_data.title == close_match].index[0]
    similarity_score = list(enumerate(similarity[index_of_the_movie]))
    sorted_similar_movies = sorted(similarity_score, key=lambda x: x[1], reverse=True)

    recommended_movies = []
    for movie in sorted_similar_movies[1:6]:
        index = movie[0]
        title = movies_data.iloc[index]['title']
        poster_url = fetch_movie_poster(title)
        recommended_movies.append((title, poster_url))

    return recommended_movies

@app.route('/')
def index():
    movie_titles = movies_data['title'].tolist()
    return render_template('index.html', movies=movie_titles)

@app.route('/recommendations', methods=['GET'])
def recommendations():
    movie_name = request.args.get('movie')
    if not movie_name:
        return jsonify({'error': 'No movie title provided.'}), 400

    recommended_movies = get_movie_recommendations(movie_name)
    if not recommended_movies:
        return jsonify({'error': 'No recommendations found.'}), 404

    response = [{'title': title, 'poster': poster} for title, poster in recommended_movies]
    return jsonify(response)

def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')

if __name__ == '__main__':
    open_browser()
    app.run()
