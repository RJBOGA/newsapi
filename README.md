# Crime News API

This API provides access to news articles filtered by keywords related to crime, violence, accidents, and death, and performs sentiment analysis on those articles.

## Table of Contents

1.  [Introduction](#introduction)
2.  [Requirements](#requirements)
3.  [Installation](#installation)
4.  [Configuration](#configuration)
5.  [Running the Application](#running-the-application)
6.  [API Endpoints](#api-endpoints)
7.  [Swagger Documentation](#swagger-documentation)
8.  [Example Usage](#example-usage)
9.  [Contributing](#contributing)
10. [License](#license)

## Introduction

The Crime News API allows you to retrieve news articles based on a specific location (zipcode), filter these articles for content related to crime, violence, accidents, and death, and analyze the sentiment of the filtered articles. This can be useful for various applications, such as analyzing the overall sentiment of news in a particular area or identifying news events related to specific keywords.

## Requirements

*   Python 3.7+
*   pip (Python package installer)

## Installation

1.  Clone the repository:

    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  Create a virtual environment (recommended):

    ```bash
    python -m venv venv
    ```

3.  Activate the virtual environment:

    *   On Windows:

        ```bash
        venv\Scripts\activate
        ```

    *   On macOS and Linux:

        ```bash
        source venv/bin/activate
        ```

4.  Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

    (Make sure you create the `requirements.txt` that contains the libraries)
    ```
    Flask
    python-dotenv
    requests
    beautifulsoup4
    nltk
    flasgger
    ```

## Configuration

1.  Create a `.env` file in the root directory of the project.

2.  Add your News API key to the `.env` file:

    ```
    NEWSAPI_KEY=YOUR_NEWSAPI_KEY
    ```

    Replace `YOUR_NEWSAPI_KEY` with your actual News API key. You can obtain a News API key from [https://newsapi.org/](https://newsapi.org/).

3.  Download the `uszipcsv.csv` file and place it in the root directory of the project. You may need to find a suitable CSV file containing US zipcode data with city, state, latitude, and longitude information.

## Running the Application

1.  Activate the virtual environment (if you haven't already).

2.  Run the Flask application:

    ```bash
    python app.py
    ```

    This will start the Flask development server. You can access the API endpoints at `http://127.0.0.1:5000/` (or the address shown in the terminal output).

## API Endpoints

### 1. Get Location Information by Zipcode

*   **Endpoint:** `/location_local`
*   **Method:** `GET`
*   **Description:** Returns location information (city, state, latitude, longitude) for a given US zipcode from a local data file.
*   **Parameters:**
    *   `zipcode` (required): A 5-digit US zipcode (passed as a query parameter).
*   **Example:**

    ```
    GET /location_local?zipcode=10001
    ```

### 2. Get News Articles by Zipcode

*   **Endpoint:** `/news/zipcode/{zipcode}`
*   **Method:** `GET`
*   **Description:** Returns news articles for a given US zipcode, fetched from the News API.
*   **Parameters:**
    *   `zipcode` (required): A 5-digit US zipcode (passed as a path parameter).
*   **Example:**

    ```
    GET /news/zipcode/10001
    ```

### 3. Get Filtered News Articles with Sentiment Analysis by Zipcode

*   **Endpoint:** `/news/zipcode/{zipcode}/filtered_sentiment`
*   **Method:** `GET`
*   **Description:** Returns news articles filtered by keywords related to crime, violence, accidents, and death, along with sentiment analysis scores for the filtered articles.
*   **Parameters:**
    *   `zipcode` (required): A 5-digit US zipcode (passed as a path parameter).
*   **Example:**

    ```
    GET /news/zipcode/10001/filtered_sentiment
    ```

## Swagger Documentation

The API includes Swagger/OpenAPI documentation, which allows you to explore the API endpoints and their parameters in an interactive interface.

1.  Run the Flask application (see [Running the Application](#running-the-application)).

2.  Open your web browser and go to `http://127.0.0.1:5000/apidocs` (or the address where your Flask app is running).

3.  You should see the Swagger UI, which provides an interactive documentation for your API.

## Example Usage

Here's an example of how you can use the API to retrieve filtered news articles with sentiment analysis for a specific zipcode using `curl`:

```bash
curl http://127.0.0.1:5000/news/zipcode/10001/filtered_sentiment