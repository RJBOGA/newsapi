# Crime News API Documentation

## Introduction

This API provides access to news articles filtered by keywords related to crime, violence, accidents, and death, along with sentiment analysis of the filtered articles.

## Base URL

The base URL for all API endpoints is: `/`

## Endpoints

### 1. Get Location Information by Zipcode

*   **Endpoint:** `/location_local`
*   **Method:** `GET`
*   **Description:** Returns location information (city, state, latitude, longitude) for a given US zipcode from a local data file.
*   **Parameters:**
    *   `zipcode` (required): A 5-digit US zipcode.
*   **Request Example:**

    ```
    GET /location_local?zipcode=10001
    ```

*   **Response Example (Success - 200 OK):**

    ```json
    {
      "city": "New York",
      "state": "NY",
      "latitude": "40.7143",
      "longitude": "-74.006",
      "country": "US",
      "zip": "10001"
    }
    ```

*   **Response Example (Error - 400 Bad Request):**

    ```json
    {
      "error": "Invalid or missing zipcode"
    }
    ```

*   **Response Example (Error - 404 Not Found):**

    ```json
    {
      "error": "Could not retrieve location information for this zipcode"
    }
    ```

### 2. Get News Articles by Zipcode

*   **Endpoint:** `/news/zipcode/{zipcode}`
*   **Method:** `GET`
*   **Description:** Returns news articles for a given US zipcode, fetched from the News API.
*   **Parameters:**
    *   `zipcode` (required): A 5-digit US zipcode.
*   **Request Example:**

    ```
    GET /news/zipcode/10001
    ```

*   **Response Example (Success - 200 OK):**

    ```json
    [
      {
        "source": {
          "id": "associated-press",
          "name": "Associated Press"
        },
        "author": "Jake Bleiberg",
        "title": "Federal appeals court rules Texas must remove buoys placed in Rio Grande to deter migrants",
        "description": "A federal appeals court has ruled that Texas must remove a floating barrier that was placed in the Rio Grande to deter migrants from crossing into the U.S. from Mexico.",
        "url": "https://apnews.com/article/texas-rio-grande-buoys-migrants-greg-abbott-779546695d95072247b629946575a844",
        "urlToImage": "https://dims.apnews.com/dims4/default/29c8d69/2147483647/strip/true/crop/4688x2637+0+244/resize/1440x810!/quality/90/?url=https%3A%2F%2Fassets.apnews.com%2F37%2F3c%2F909975c9e438d16a4497909c4470%2F6e4b703436634a83b2486a6c5917c6ca",
        "publishedAt": "2023-12-01T00:46:22Z",
        "content": "A federal appeals court has ruled that Texas must remove a floating barrier that was placed in the Rio Grande to deter migrants from crossing into the U.S. from Mexico.\r\nThe 5th U.S. Circuit Court of Appeals… [+4439 chars]"
      },
      // ... more articles
    ]
    ```

*   **Response Example (Error - 400 Bad Request):**

    ```json
    {
      "error": "Invalid zipcode format"
    }
    ```

*   **Response Example (Error - 500 Internal Server Error):**

    ```json
    {
      "error": "Could not retrieve location information"
    }
    ```

### 3. Get Filtered News Articles with Sentiment Analysis by Zipcode

*   **Endpoint:** `/news/zipcode/{zipcode}/filtered_sentiment`
*   **Method:** `GET`
*   **Description:** Returns news articles filtered by keywords related to crime, violence, accidents, and death, along with sentiment analysis scores for the filtered articles.
*   **Parameters:**
    *   `zipcode` (required): A 5-digit US zipcode.
*   **Request Example:**

    ```
    GET /news/zipcode/10001/filtered_sentiment
    ```

*   **Response Example (Success - 200 OK):**

    ```json
    {
      "articles": [
        {
          "title": "Man arrested after stabbing in downtown Seattle",
          "description": "A man was arrested after a stabbing in downtown Seattle on Wednesday night. Police responded to reports of a stabbing at 3rd Avenue and Pine Street at 8:10 p.m. When officers arrived, they found a man with multiple stab wounds. The victim was taken to Harborview Medical …",
          "url": "https://mynorthwest.com/3916944/man-arrested-after-stabbing-in-downtown-seattle/",
          "sentiment_score": -0.7579,
          "publishedAt": "2023-11-30T18:00:31Z"
        },
        // ... more articles
      ],
      "average_sentiment": -0.6215
    }
    ```

*   **Response Example (Error - 400 Bad Request):**

    ```json
    {
      "error": "Invalid zipcode format"
    }
    ```

*   **Response Example (Error - 404 Not Found):**

    ```json
    {
      "error": "Could not retrieve location information"
    }
    ```

*   **Response Example (Error - 500 Internal Server Error):**

    ```json
    {
      "error": "Could not retrieve news articles"
    }
    ```

## Data Structures

### Article Object

```json
{
  "title": "Article Title",
  "description": "Article Description",
  "url": "Article URL",
  "sentiment_score": -0.4588,
  "publishedAt": "2023-11-30T18:00:31Z"
}