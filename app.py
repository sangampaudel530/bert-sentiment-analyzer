import pandas as pd
import streamlit
from utils.scraper import get_reviews
from streamlit_lottie import st_lottie
import requests
from utils.predict import predict_sentiment_with_score

# Page configuration
streamlit.set_page_config(page_title="🎬 Movie Review Sentiment App", layout="wide", page_icon="🎥")

# Load Lottie animation
def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_url = "https://assets1.lottiefiles.com/packages/lf20_qp1q7mct.json"
lottie_movie = load_lottie_url(lottie_url)

# Initialize section state
if "active_section" not in streamlit.session_state:
    streamlit.session_state.active_section = "dataset"

# Custom CSS with hover effects
streamlit.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }
    .main-title {
        font-size: 3rem;
        text-align: center;
        font-weight: 700;
        color: #007BFF;
        margin-bottom: 1.5rem;
        animation: fadeIn 2s ease-out;
        text-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
    }
    .main-title span {
        color: #FF6347;
    }
    @keyframes fadeIn {
        0% { opacity: 0; }
        100% { opacity: 1; }
    }
    .nav-bar {
        display: flex;
        justify-content: center;
        background-color: #007BFF;
        padding: 15px;
        border-radius: 8px;
        margin-top: 20px;
        margin-bottom: 20px;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
    }
    .review-box {
        background-color: #f8f9fa;
        color: #000000;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 15px;
        border: 1px solid #dee2e6;
    }
    @media (prefers-color-scheme: dark) {
        .review-box {
            background-color: #1e1e1e;
            color: #f1f1f1;
            border: 1px solid #333;
        }
    }
    button[kind="secondary"] {
        transition: background-color 0.3s ease, transform 0.2s ease;
    }
    button[kind="secondary"]:hover {
        background-color: #0056b3 !important;
        color: white !important;
        transform: scale(1.03);
    }
    button[type="submit"] {
        background-color: #28a745;
        color: white;
        font-weight: 600;
        transition: background-color 0.3s ease, transform 0.2s ease;
        border-radius: 6px;
    }
    button[type="submit"]:hover {
        background-color: #218838;
        transform: scale(1.04);
    }
    </style>
""", unsafe_allow_html=True)

# Centered Lottie animation
col1, col2, col3 = streamlit.columns([1.3, 0.8, 1])
with col2:
    st_lottie(lottie_movie, speed=1, height=200, width=200, key="movie")

# Title
streamlit.markdown("<div class='main-title'>Movie Review Sentiment <span>App</span></div>", unsafe_allow_html=True)

# Navigation bar
streamlit.markdown("<div class='nav-bar'>", unsafe_allow_html=True)
col1, col2, col3 = streamlit.columns(3)
with col1:
    if streamlit.button("📁 Dataset"):
        streamlit.session_state.active_section = "dataset"
with col2:
    if streamlit.button("🎬 IMDb Reviews"):
        streamlit.session_state.active_section = "imdb"
with col3:
    if streamlit.button("✍️ Manual Input"):
        streamlit.session_state.active_section = "manual"
streamlit.markdown("</div>", unsafe_allow_html=True)

# Section: Dataset Upload
if streamlit.session_state.active_section == "dataset":
    streamlit.subheader("📁 Analyze Sentiment from Dataset")
    streamlit.write("Upload your dataset file (CSV or Excel) containing movie reviews.")
    dataset_file = streamlit.file_uploader("Upload your dataset file", type=["csv", "xlsx"])

    if dataset_file:
        try:
            if dataset_file.name.endswith(".csv"):
                df = pd.read_csv(dataset_file)
            else:
                df = pd.read_excel(dataset_file)

            streamlit.success("Dataset uploaded successfully!")

            # Auto-detect review column
            possible_cols = [col for col in df.columns if col.strip().lower() in ["review", "reviews"]]
            if possible_cols:
                review_column = possible_cols[0]
                streamlit.success(f"Auto-detected review column: {review_column}")
            else:
                review_column = streamlit.selectbox("Select the column containing reviews", df.columns)

            max_rows = len(df)
            num_rows = streamlit.slider("Select number of rows to analyze", min_value=10, max_value=max_rows, value=min(100, max_rows), step=10)

            if review_column:
                df_subset = df[[review_column]].astype(str).iloc[:num_rows]

                if streamlit.button("🔍 Predict Sentiment"):
                    with streamlit.spinner("Analyzing sentiment..."):
                        predictions = predict_sentiment_with_score(df_subset[review_column].tolist())
                        df_subset["Sentiment"] = [pred[0] for pred in predictions]
                        df_subset["Confidence"] = [pred[1] for pred in predictions]

                    streamlit.subheader("📊 Sentiment Predictions (Preview)")
                    streamlit.dataframe(df_subset)

                    csv = df_subset.to_csv(index=False)
                    streamlit.download_button(
                        label="📥 Download Predictions as CSV",
                        data=csv,
                        file_name="movie_reviews_sentiment_results.csv",
                        mime="text/csv"
                    )

        except Exception as e:
            streamlit.error(f"Error processing file: {e}")

# Section: IMDb Reviews
elif streamlit.session_state.active_section == "imdb":
    streamlit.subheader("🎬 Fetch Reviews from IMDb")
    movie_title = streamlit.text_input("Enter a movie title", placeholder="e.g. Inception")
    if streamlit.button("Fetch Reviews"):
        if not movie_title:
            streamlit.warning("Please enter a movie title.")
        else:
            with streamlit.spinner("Fetching data..."):
                # Use OMDb API to fetch poster
                api_key = "ad0e3181"
                omdb_url = f"http://www.omdbapi.com/?t={movie_title}&apikey={api_key}"
                omdb_response = requests.get(omdb_url)
                movie_data = omdb_response.json()
                poster_url = movie_data.get("Poster", None)
                
                # Fetch reviews directly using the movie title
                reviews = get_reviews(movie_title, max_reviews=20)
                
                if poster_url:
                    streamlit.image(poster_url, caption=f"Poster of {movie_title}", use_container_width=True)
                
                if reviews:
                    streamlit.success(f"Fetched {len(reviews)} reviews for '{movie_title}'")
                    streamlit.subheader("📃 Reviews")
                    for i, review in enumerate(reviews, 1):
                        sentiment_score = predict_sentiment_with_score([review])
                        sentiment, score = sentiment_score[0]
                        color = "green" if sentiment == "Positive" else "red"
                        streamlit.markdown(
                            f"<div class='review-box' style='color:{color};'><strong>Review {i}:</strong><br>{review}<br><br><strong>Sentiment:</strong> {sentiment} with confidence score: {score:.2f}</div>",
                            unsafe_allow_html=True)
                else:
                    streamlit.error("No reviews found or failed to scrape reviews.")

# Section: Manual Input
elif streamlit.session_state.active_section == "manual":
    streamlit.subheader("✍️ Paste Reviews Manually")
    with streamlit.form("manual_input_form"):
        manual_reviews = streamlit.text_area("Paste the movie reviews here (one or more paragraphs)", height=200)
        submitted = streamlit.form_submit_button("Analyze Sentiment")
        if submitted and manual_reviews.strip():
            with streamlit.spinner("Analyzing sentiment..."):
                predictions = predict_sentiment_with_score([manual_reviews])
                sentiment, score = predictions[0]
                color = "green" if sentiment == "Positive" else "red"
                streamlit.markdown(
                    f"<div class='review-box' style='color:{color};'><strong>Sentiment:</strong> {sentiment} with confidence score: {score:.2f}</div>",
                    unsafe_allow_html=True)
        elif submitted:
            streamlit.warning("Please enter a review before submitting.")

# Footer
streamlit.markdown("""
    <hr style="margin-top: 3rem;"/>
    <div style='text-align: center; font-size: 0.9rem; color: grey;'>
        Built with ❤️ using Streamlit | © 2025 Sangam Paudel
    </div>
""", unsafe_allow_html=True)
