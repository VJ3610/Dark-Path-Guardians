from flask import Flask, render_template, request, redirect, url_for
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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    input_paragraph = request.form['paragraph']
    input_data = [input_paragraph]
    prediction = model.predict(input_data)[0]

    # Redirect to a different route to avoid form resubmission
    return redirect(url_for('result', prediction=prediction))

@app.route('/result')
def result():
    prediction = request.args.get('prediction')
    return render_template('result.html', prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)
