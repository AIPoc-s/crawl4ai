import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
import numpy as np
from config import ML_MODEL_PATH

# Load or train the ML model
def load_model():
    try:
        with open(ML_MODEL_PATH, 'rb') as f:
            model, vectorizer = pickle.load(f)
        return model, vectorizer
    except FileNotFoundError:
        # Train a simple model if no saved model exists
        training_data = [
            ("/api/v1/users", 1),
            ("/docs/css/style.css", 0),
            ("/api/v1/products", 1),
            ("/images/logo.png", 0),
        ]
        vectorizer = CountVectorizer(analyzer='char', ngram_range=(2, 4))
        X = vectorizer.fit_transform([url for url, label in training_data])
        y = np.array([label for url, label in training_data])
        model = RandomForestClassifier()
        model.fit(X, y)
        with open(ML_MODEL_PATH, 'wb') as f:
            pickle.dump((model, vectorizer), f)
        return model, vectorizer

model, vectorizer = load_model()

def is_endpoint(link):
    """Predict if a link is an API endpoint."""
    features = vectorizer.transform([link])
    return model.predict(features)[0] == 1