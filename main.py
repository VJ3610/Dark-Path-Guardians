from flask import Flask, render_template, request
import re
import csv
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from flask_cors import CORS

app = Flask(__name__, static_url_path='/static')
CORS(app)  # Enable CORS for all routes

def load_dark_patterns_from_csv(csv_file):
    patterns = {}
    with open(csv_file, 'r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            text = row['text'].strip()
            pattern_category = row['Pattern Category'].strip()
            patterns[text] = pattern_category
    return patterns

def detect_dark_patterns_in_website(url, patterns):
    try:
        # Convert relative URL to absolute URL
        absolute_url = urljoin("https://example.com", url)

        # Fetch the HTML content of the webpage
        response = requests.get(absolute_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
        response.raise_for_status()  # Raise an HTTPError for bad responses

        # Check for successful response
        if response.status_code == 200:
            # Parse the HTML using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract text content from the webpage
            page_text = soup.get_text()

            # Check for the presence of dark patterns
            detected_patterns = []
            for pattern_text, pattern_category in patterns.items():
                if pattern_category.lower() != 'not dark pattern' and re.search(re.escape(pattern_text), page_text, re.IGNORECASE):
                    detected_patterns.append(f"{pattern_text} - {pattern_category}")

            # Return a formatted plain text response with each detected pattern on a new line
            if detected_patterns:
                return '\n'.join(detected_patterns)
            else:
                return 'No dark patterns detected.'
        else:
            return f"Error: Unexpected response status code {response.status_code}"

    except requests.RequestException as e:
        return f"Error connecting to the website: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/')
def index():
    return render_template('popup.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        website_url = request.form['website_url']
        csv_file_path = "dark.csv"  # Replace with the actual path to your CSV file
        patterns = load_dark_patterns_from_csv(csv_file_path)
        result = detect_dark_patterns_in_website(website_url, patterns)

        return result

if __name__ == '__main__':
    app.run(debug=True)
