from flask import Flask, render_template, request, redirect, url_for
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin  # Add this import
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline

app = Flask(__name__)

# Load the dataset
dataset = pd.read_csv('dark.csv')

# Separate features (X) and target variable (y)
X_train = dataset['text']
y_train = dataset['Pattern Category']

# Create a pipeline with TfidfVectorizer and SVC
model = make_pipeline(TfidfVectorizer(), SVC())

# Fit the model with the training data
model.fit(X_train, y_train)

def download_file(url, folder):
    response = requests.get(url)
    if response.status_code == 200:
        filename = os.path.join(folder, os.path.basename(url))
        with open(filename, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded: {url}")
        return filename
    else:
        print(f"Failed to download: {url}")
        return None

def extract_html_and_js(url, output_folder):
    response = requests.ge
