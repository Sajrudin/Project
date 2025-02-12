# 🎬 Movie Recommendation System

This project is a Movie Recommendation System built using Flask, Pandas, Scikit-learn, and The Movie Database (TMDb) API. It provides personalized movie recommendations based on content similarity, allowing users to input a movie title and receive suggestions for similar movies along with their posters.
🚀 Features

    📌 Movie Search: Users can search for a movie from a dataset.
    🎭 Content-Based Recommendations: Suggests movies based on genres, keywords, cast, tagline, and director.
    🖼 Movie Posters: Fetches posters using TMDb API to enhance the user experience.
    🌐 Web Interface: Simple and interactive UI using Flask and HTML templates.

# 🛠 Technologies Used

    Python (Flask, Pandas, NumPy, Scikit-learn)
    Flask (for web framework)
    TfidfVectorizer & Cosine Similarity (for content-based filtering)
    The Movie Database (TMDb) API (for fetching movie posters)
    HTML, CSS, JavaScript (for frontend)
    
#  🎯 How It Works

    1.Dataset Loading: Reads movies.csv, which contains movie details.
    2.Feature Processing: Combines genres, keywords, cast, and director information.
    3.Vectorization: Uses TF-IDF Vectorizer to convert text into numerical form.
    4.Similarity Calculation: Computes cosine similarity between movies.
    5.Find Closest Matches: Identifies the most similar movies based on user input.
    6.Fetch Posters: Calls TMDb API to get posters for recommended movies.
    7.Display Results: Shows the recommendations along with their posters.
