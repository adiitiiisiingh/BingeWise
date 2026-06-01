from flask import Flask, render_template, request, redirect
import requests
import pandas as pd
import sqlite3
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

API_KEY = "1ca9c1a8"

# ==========================
# DATABASE FUNCTIONS
# ==========================

def get_watchlist():

    conn = sqlite3.connect("bingewise.db")
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM watchlist")

    movies = cursor.fetchall()

    conn.close()

    return movies


def add_movie_to_db(movie):

    conn = sqlite3.connect("bingewise.db")

    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR IGNORE INTO watchlist
    (title, poster, year, rating)
    VALUES (?, ?, ?, ?)
    """, (
        movie.get("Title"),
        movie.get("Poster"),
        movie.get("Year"),
        movie.get("imdbRating")
    ))

    conn.commit()
    conn.close()


def remove_movie_from_db(title):

    conn = sqlite3.connect("bingewise.db")

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM watchlist WHERE title=?",
        (title,)
    )

    conn.commit()
    conn.close()

# ==========================
# RECOMMENDATION ENGINE
# ==========================

movies_data = pd.read_csv("data/movies.csv")

movies_data = movies_data[['Series_Title', 'Genre']]

movies_data = movies_data.dropna()

cv = CountVectorizer()

vector = cv.fit_transform(
    movies_data['Genre']
).toarray()

similarity = cosine_similarity(vector)


def recommend(movie_name):

    recommended_movies = []

    try:

        movie_index = movies_data[
            movies_data['Series_Title'].str.lower()
            == movie_name.lower()
        ].index[0]

        distances = similarity[movie_index]

        movie_list = sorted(
            list(enumerate(distances)),
            reverse=True,
            key=lambda x: x[1]
        )[1:6]

        for movie in movie_list:

            movie_title = movies_data.iloc[
                movie[0]
            ].Series_Title

            url = f"http://www.omdbapi.com/?t={movie_title}&apikey={API_KEY}"

            response = requests.get(url)

            movie_data = response.json()

            recommended_movies.append(movie_data)

    except:
        pass

    return recommended_movies

# ==========================
# HOME
# ==========================

@app.route("/", methods=["GET", "POST"])
def home():

    movies = []

    recommendations = []

    if request.method == "POST":

        movie_name = request.form["movie"]

        url = f"http://www.omdbapi.com/?s={movie_name}&apikey={API_KEY}"

        response = requests.get(url)

        data = response.json()

        if "Search" in data:

            movies = data["Search"]

        recommendations = recommend(movie_name)

    return render_template(
        "index.html",
        movies=movies,
        recommendations=recommendations,
        watchlist=get_watchlist()
    )

# ==========================
# MOVIE DETAILS
# ==========================

@app.route("/movie/<movie_name>")
def movie_details(movie_name):

    url = f"http://www.omdbapi.com/?t={movie_name}&apikey={API_KEY}"

    response = requests.get(url)

    movie = response.json()

    return render_template(
        "movie_details.html",
        movie=movie
    )

# ==========================
# ADD WATCHLIST
# ==========================

@app.route("/add_to_watchlist/<movie_name>")
def add_to_watchlist(movie_name):

    url = f"http://www.omdbapi.com/?t={movie_name}&apikey={API_KEY}"

    response = requests.get(url)

    movie = response.json()

    add_movie_to_db(movie)

    return redirect("/")

# ==========================
# REMOVE WATCHLIST
# ==========================

@app.route("/remove_from_watchlist/<movie_name>")
def remove_from_watchlist(movie_name):

    remove_movie_from_db(movie_name)

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)