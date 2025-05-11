import requests

# Set your OMDb API key
OMDB_API_KEY = "ad0e3181"

def get_movie_id(movie_name):
    # Use the OMDb API to fetch movie data based on the movie name
    search_url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&s={movie_name}"

    response = requests.get(search_url)
    data = response.json()

    if data["Response"] == "True":
        # If the movie is found, return the IMDb ID
        movie_id = data["Search"][0]["imdbID"]
        return movie_id
    else:
        print("Movie not found.")
        return None

def get_reviews(movie_id, max_reviews=20):
    # Fetch movie details and reviews using OMDb API
    url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&i={movie_id}&plot=full"
    
    response = requests.get(url)
    movie_data = response.json()

    if movie_data["Response"] == "True":
        # Collect reviews if available (using plot as a placeholder for reviews)
        reviews = []
        
        # Example: Add reviews from the plot (since OMDb doesn't provide direct reviews, you may use 'Plot' or 'Actors' etc.)
        reviews.append(movie_data["Plot"])
        
        # If you want to add more information like actors, directors, etc., you can append here
        reviews.append(f"Actors: {movie_data.get('Actors', 'N/A')}")
        reviews.append(f"Director: {movie_data.get('Director', 'N/A')}")
        reviews.append(f"Rating: {movie_data.get('imdbRating', 'N/A')}")

        return reviews[:max_reviews]
    else:
        print("Error fetching reviews:", movie_data.get("Error", "Unknown error"))
        return []

