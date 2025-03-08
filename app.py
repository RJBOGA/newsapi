from flask import Flask, request, jsonify
import re
import os
from dotenv import load_dotenv
import csv
from datetime import datetime, timedelta
from urllib.parse import quote_plus
import requests
from bs4 import BeautifulSoup
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, PunktSentenceTokenizer  # Import PunktSentenceTokenizer
import logging
import shutil  # Import the shutil module
import nltk
nltk.download('punkt_tab')

load_dotenv()

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load uszipcsv.csv data
US_DATA_FILE = "uszipcsv.csv"
us_zip_data = {}

try:
    with open(US_DATA_FILE, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                zipcode = row['\ufeffzipcode']
                us_zip_data[zipcode] = {
                    "city": row['city'],
                    "state": row['state'],
                    "latitude": row['latitude'],
                    "longitude": row['longitude'],
                    "country": "US",
                    "zip": zipcode
                }
            except Exception as e:
                logging.error(f"Error reading row: {row}. The exception was {e}")

except FileNotFoundError:
    logging.error(f"Error: US data file not found at {US_DATA_FILE}")
    us_zip_data = {}

news_api_key = os.getenv("NEWSAPI_KEY")

if not news_api_key:
    raise ValueError("NewsAPI key not found in .env file. Please create a .env file with NEWSAPI_KEY=YOUR_API_KEY")

# Download NLTK resources (do this only once)
try:
    nltk.data.find('corpora/vader_lexicon')
except LookupError:
    logging.info("Downloading vader_lexicon...")
    nltk.download('vader_lexicon')

try:
    nltk.data.find('stopwords')
except LookupError:
    logging.info("Downloading stopwords...")
    nltk.download('stopwords')

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    logging.info("Downloading punkt...")
    nltk.download('punkt')


# THIS IS THE NEW SECTION TO CLEAR OUT NLTK DATA
nltk_data_path = nltk.data.path[0]  # Assumes the first path is the main one
punkt_path = os.path.join(nltk_data_path, 'tokenizers', 'punkt')  # path to punkt

try:
    if os.path.exists(punkt_path):
        logging.warning(f"Deleting punkt directory: {punkt_path}")
        shutil.rmtree(punkt_path)  # Delete the directory and all its contents
    else:
        logging.info("Punkt directory not found. Skipping deletion.")
except Exception as e:
    logging.error(f"Error deleting punkt directory: {e}")

def is_valid_zipcode(zipcode):
    """Validates a US zipcode format."""
    return bool(re.match(r"^\d{5}$", zipcode))

def get_location_info_from_zipcode(zipcode):
    """Retrieves location information from local data."""
    if not us_zip_data:
        logging.warning("US Data file is not loaded.")
        return None
    location_info = us_zip_data.get(zipcode)
    return location_info

def get_news_articles(city):
    """Fetches news articles from News API using an exact phrase search."""
    today = datetime.now().date()
    week_ago = today - timedelta(days=7)

    from_date_str = week_ago.strftime("%Y-%m-%d")
    to_date_str = today.strftime("%Y-%m-%d")

    encoded_city = quote_plus(f'"{city}"')

    news_url = (
        f"https://newsapi.org/v2/everything?q={encoded_city}"
        f"&from={from_date_str}&to={to_date_str}"
        f"&apiKey={news_api_key}"
    )

    try:
        response = requests.get(news_url)
        response.raise_for_status()
        data = response.json()

        if data["status"] == "ok":
            return data["articles"]
        else:
            logging.error(f"News API error: {data.get('message', 'Unknown error')}")
            return None
    except requests.exceptions.RequestException as e:
        logging.error(f"Error retrieving news articles: {e}")
        return None

def clean_text(text):
    """Cleans the text by removing HTML tags, punctuation, and stop words."""
    if not text:  # Handle None or empty strings
        return ""

    try:
        soup = BeautifulSoup(text, "html.parser")
        text = soup.get_text(separator=" ")  # Get text and replace <br/> tags with spaces

        text = re.sub(r'[^\w\s]', '', text) # Remove punctuation

        text = text.lower()
        stop_words = set(stopwords.words('english'))

        # Load PunktSentenceTokenizer explicitly
        try:
            sent_tokenizer = PunktSentenceTokenizer()
        except Exception as e:
            logging.error(f"Error loading PunktSentenceTokenizer: {e}")
            return ""

        word_tokens = word_tokenize(text,  # Pass the text
                                   )  # Ensure punkt is used
        filtered_text = [w for w in word_tokens if not w in stop_words]
        return " ".join(filtered_text)
    except Exception as e:
        logging.error(f"Error during text cleaning: {e}")
        return ""


@app.route('/location_local', methods=['GET'])
def location_local():
    """
    GET /location_local?zipcode=XXXXX
    Returns location information from the local uszipcsv.csv file.
    """
    zipcode = request.args.get('zipcode')

    if not zipcode or not is_valid_zipcode(zipcode):
        return jsonify({"error": "Invalid or missing zipcode"}), 400

    if not us_zip_data:
        return jsonify({"error": "US Data file is not loaded."}), 500

    location_info = us_zip_data.get(zipcode)

    if location_info:
        return jsonify(location_info), 200
    else:
        return jsonify({"error": "Could not retrieve location information for this zipcode"}), 404

@app.route('/news/zipcode/<zipcode>')
def news_by_zipcode(zipcode):
    """GET /news/zipcode/XXXXX - Returns news articles based on zipcode."""

    if not is_valid_zipcode(zipcode):
        return jsonify({"error": "Invalid zipcode format"}), 400

    location_info = get_location_info_from_zipcode(zipcode)

    if not location_info:
        return jsonify({"error": "Could not retrieve location information"}), 500

    city = location_info["city"]

    news_articles = get_news_articles(city)

    if not news_articles:
        return jsonify({"error": "Could not retrieve news articles"}), 500

    return jsonify(news_articles)


@app.route('/news/zipcode/<zipcode>/filtered_sentiment')
def news_filtered_sentiment(zipcode):
    """
    GET /news/zipcode/XXXXX/filtered_sentiment
    Returns news articles filtered by keywords related to crime, violence, etc.,
    with sentiment analysis.
    """
    if not is_valid_zipcode(zipcode):
        return jsonify({"error": "Invalid zipcode format"}), 400

    location_info = get_location_info_from_zipcode(zipcode)
    if not location_info:
        return jsonify({"error": "Could not retrieve location information"}), 404

    city = location_info["city"]
    news_articles = get_news_articles(city)
    if not news_articles:
        return jsonify({"error": "Could not retrieve news articles"}), 500

    keywords = ["crime", "violence", "accident", "death", "murder", "assault", "robbery", "shooting", "crash", "injury", "fatal", "killed", "victim", "police", "arrest", "investigation", "homicide"]

    filtered_articles = []
    try:
        sid = SentimentIntensityAnalyzer()
    except Exception as e:
        logging.error(f"Error initializing SentimentIntensityAnalyzer: {e}")
        return jsonify({"error": "Failed to initialize sentiment analyzer"}), 500
    total_sentiment = 0
    article_count = 0

    for article in news_articles:
        try:
            description = article.get('description', '')
            title = article.get('title', '')
            combined_text = f"{title} {description}"  # Combine title and description
            cleaned_text = clean_text(combined_text)

            # Check for keywords (case-insensitive)
            if any(keyword in cleaned_text for keyword in keywords):
                sentiment_scores = sid.polarity_scores(cleaned_text)
                compound_sentiment = sentiment_scores['compound']

                filtered_article = {
                    "title": article.get('title'),
                    "description": article.get('description'),
                    "content": article.get('content'),
                    "url": article.get('url'),
                    "publishedAt": article.get('publishedAt'),
                    "sentiment_score": compound_sentiment,
                    "source": article.get('source')
                }
                filtered_articles.append(filtered_article)
                total_sentiment += compound_sentiment
                article_count += 1

        except Exception as e:
            logging.error(f"Error processing article: {e}")
            continue  # Skip the error and continue processing articles.

    average_sentiment = total_sentiment / article_count if article_count > 0 else 0

    response_data = {
        "articles": filtered_articles,
        "average_sentiment": average_sentiment
    }

    logging.info(f"Returning {len(filtered_articles)} filtered articles with average sentiment: {average_sentiment}")
    return jsonify(response_data)


if __name__ == '__main__':
    app.run(debug=True)