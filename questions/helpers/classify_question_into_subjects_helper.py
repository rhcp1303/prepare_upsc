import pickle
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import numpy as np

def classify_text(text):
    with open("questions/data/question_classifier/question_classifier_vectorizer.pkl", 'rb') as vec_file:
        vectorizer = pickle.load(vec_file)
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text.lower())
    filtered_words = [word for word in words if word not in stop_words]
    filtered_text = " ".join(filtered_words)
    text_vec = vectorizer.transform([filtered_text])
    with open("questions/data/question_classifier/question_classifier_model.pkl", 'rb') as file:
        loaded_model = pickle.load(file)
    predicted_probs = loaded_model.predict_proba(text_vec)[0]
    print(predicted_probs[np.argmax(predicted_probs)])
    return loaded_model.classes_[np.argmax(predicted_probs)]
