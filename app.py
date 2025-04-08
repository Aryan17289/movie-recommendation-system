from flask import Flask, request, jsonify, render_template
import pandas as pd
import nltk
import string
import os
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask_cors import CORS
import requests




TMDB_API_KEY ="e06bfc0fd91ea4a6f7fe4eead5f896fe"

def get_movie_poster(movie_title):
    """Fetch movie poster from TMDb API"""
    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={movie_title}&language=en-US"
    response = requests.get(url).json()
    
    if response["results"]:
        poster_path = response["results"][0].get("poster_path")
        if poster_path:
            return [f"https://image.tmdb.org/t/p/w500{poster_path}"]

    return ["static/image2.jpg"]  # Fallback image if no poster found


# Initialize Flask app
app = Flask(__name__, static_folder="static")
CORS(app, resources={r"/*": {"origins": "*"}})

# Ensure necessary NLTK data is available
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')
    nltk.download('punkt')

# Load dataset safely
csv_path = "movies.csv"
if not os.path.exists(csv_path):
    print(f"Error: CSV file '{csv_path}' not found! Exiting.")
    exit(1)

print("Loading dataset...")
movies = pd.read_csv(csv_path)
print(f"Dataset loaded: {movies.shape}")

# Ensure required columns exist
required_columns = {'title', 'overview', 'genre', 'release_date', 'vote_average', 'original_language'}
missing_columns = required_columns - set(movies.columns)

if missing_columns:
    print(f"Error: Missing columns in dataset: {missing_columns}")
    exit(1)

# Preprocess text function
def preprocess_text(text):
    if not isinstance(text, str):  # Handle NaN or non-string values
        return ""
    text = text.lower().translate(str.maketrans('', '', string.punctuation))
    words = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]
    return " ".join(words)

# Apply preprocessing
print("Processing text...")
movies['processed_overview'] = movies['overview'].apply(preprocess_text)
print("Text processing completed.")

# Convert text to numerical features using TF-IDF
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(movies['processed_overview'])

# Compute cosine similarity
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
print("Cosine similarity calculated.")

# Recommendation function
def recommend_movies(title, genre=None, year=None, rating=None):
    try:
        index = movies[movies['title'].str.lower() == title.lower()].index[0]
    except IndexError:
        return [{"error": "Movie not found in database"}]

    similarity_scores = list(enumerate(cosine_sim[index]))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)[1:11]  # Top 10 recommendations
    recommended_movies = movies.iloc[[i[0] for i in similarity_scores]].copy()

    # Apply filters safely
    if genre:
        recommended_movies = recommended_movies[recommended_movies['genre'].str.contains(genre, case=False, na=False)]
    if year:
        recommended_movies = recommended_movies[recommended_movies['release_date'].astype(str).str.contains(str(year), na=False)]
    if rating:
        try:
            rating_threshold = float(rating.split("+")[0])
            recommended_movies = recommended_movies[recommended_movies['vote_average'] >= rating_threshold]
        except ValueError:
            return [{"error": "Invalid rating format"}]

    # Fetch posters for each movie
    recommendations = recommended_movies[['id', 'title', 'genre', 'original_language', 'release_date', 'vote_average']].to_dict(orient='records')
    for movie in recommendations:
        poster_urls = get_movie_poster(movie["title"])
        movie["poster_path"] = poster_urls[0]  # Primary poster

    return recommendations


# Serve HTML page
@app.route('/')
def home():
    return render_template('index.html')  # This will load templates/index.html

@app.route('/recommend', methods=['GET'])
def recommend():
    movie_title = request.args.get('movie')
    genre = request.args.get('genre')
    year = request.args.get('year')
    rating = request.args.get('rating')

    if not movie_title:
        return jsonify({"error": "Please provide a movie title"}), 400

    recommendations = recommend_movies(movie_title, genre, year, rating)
    return jsonify(recommendations)

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
