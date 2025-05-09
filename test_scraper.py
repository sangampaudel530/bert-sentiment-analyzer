from utils.scraper import get_movie_id, get_reviews

title = "Inception"
movie_id = get_movie_id(title)
print("Movie ID:", movie_id)

if movie_id:
    reviews = get_reviews(movie_id)
    print(f"Total reviews fetched: {len(reviews)}")
    for r in reviews[:5]:
        print("-", r)
