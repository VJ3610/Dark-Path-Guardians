from flask import Flask, render_template, request
import re
import csv
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

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
        # Fetch the HTML content of the webpage
        response = requests.get(url)
        html_content = response.text

        # Parse the HTML using BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Extract text content from the webpage
        page_text = soup.get_text()

        # Check for the presence of dark patterns
        detected_patterns = []
        for pattern_text, pattern_category in patterns.items():
            if pattern_category.lower() != 'not dark pattern' and re.search(re.escape(pattern_text), page_text, re.IGNORECASE):
                detected_patterns.append({
                    "Pattern": pattern_text,
                    "PatternCategory": pattern_category
                })

        return detected_patterns

    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        website_url = request.form['website_url']
        csv_file_path = "dark.csv"  # Replace with the actual path to your CSV file
        patterns = load_dark_patterns_from_csv(csv_file_path)
        detected_patterns = detect_dark_patterns_in_website(website_url, patterns)

        if detected_patterns:
            return render_template('index.html', detected_patterns=detected_patterns)
        else:
            return render_template('index.html', message="No dark patterns detected.")

if __name__ == '__main__':
    app.run(debug=True)
