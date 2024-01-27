from flask import Flask, render_template, request
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline
import requests

app = Flask(__name__)

# Load the dark patterns dataset
dark_data = pd.read_csv('dark.csv')

# Print columns in dark_data for debugging
print("Columns in dark_data:", dark_data.columns)

X_train = dark_data['text']
y_train = dark_data['label']

# Create and train the model
model = make_pipeline(TfidfVectorizer(), SVC(kernel='linear'))
model.fit(X_train, y_train)

def get_page_source(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Error fetching page: {e}"

def find_dark_patterns(page_source):
    try:
        predictions = model.predict([page_source])
        matching_patterns = dark_data[dark_data['label'].isin(predictions)]['Pattern']
        return matching_patterns
    except Exception as e:
        return f"Error predicting: {e}"

@app.route('/')
def index():
    return render_template('index.html', prediction=None)

@app.route('/predict', methods=['POST'])
def predict():
    url = request.form.get('paragraph')
    
    if not url.startswith('http'):
        url = 'http://' + url
    
    page_source = get_page_source(url)
    
    if page_source.startswith('Error'):
        return render_template('index.html', prediction=None, error=page_source)

    # print("Page Source:", page_source)

    try:
        matching_patterns = find_dark_patterns(page_source)
        print("Matching Patterns:", matching_patterns)
        return render_template('index.html', prediction=matching_patterns, url=url, count=len(matching_patterns))
    except Exception as e:
        return render_template('index.html', prediction=None, error=f"Error predicting: {e}")

if __name__ == '__main__':
    app.run(debug=True)
