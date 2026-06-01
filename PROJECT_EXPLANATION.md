# BingeWise Project Flow

1. User enters a movie name in the search bar.

2. Flask receives the request using POST method.

3. Flask sends a request to the OMDb API.

4. OMDb returns movie details in JSON format.

5. Flask displays movie posters, title, year, and ratings.

6. User can click a movie to view detailed information.

7. Recommendation engine:
   - Reads movie dataset.
   - Uses CountVectorizer on Genre column.
   - Converts genres into vectors.
   - Calculates cosine similarity.
   - Finds top similar movies.
   - Fetches their details from OMDb.

8. User can add movies to Watchlist.

9. Watchlist is stored in SQLite database.

10. User can remove movies from Watchlist.