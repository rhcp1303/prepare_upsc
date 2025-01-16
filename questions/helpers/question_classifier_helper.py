from pathlib import Path
import numpy as np
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import json
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pickle
from nltk.stem import PorterStemmer

question_classifier_vectorizer_path = Path("questions/data/question_classifier/question_classifier_vectorizer.pkl")
question_classifier_model_path = Path("questions/data/question_classifier/question_classifier_model.pkl")


def classify_question(text):
    with open(question_classifier_vectorizer_path, 'rb') as vec_file:
        vectorizer = pickle.load(vec_file)
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text.lower())
    filtered_words = [word for word in words if word not in stop_words]
    filtered_text = " ".join(filtered_words)
    text_vec = vectorizer.transform([filtered_text])
    with open(question_classifier_model_path, 'rb') as file:
        loaded_model = pickle.load(file)
    predicted_probs = loaded_model.predict_proba(text_vec)[0]
    print(predicted_probs[np.argmax(predicted_probs)])
    return loaded_model.classes_[np.argmax(predicted_probs)]


def train_question_classifier(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    print(len(data))
    texts = []
    labels = []
    for item in data:
        label = item['subject']
        feature_text = item['question_text']
        texts.append(feature_text)
        labels.append(label)

    stop_words = set(stopwords.words('english'))
    redundant_words = ['consider', 'following', 'statements', 'statement', 'only', 'how', 'many', 'which', 'one',
                       'select', 'match', 'pair', 'pairs', 'paired', 'reference', 'respect', 'respectively', 'correct',
                       'correctly', 'incorrect', 'code', 'can', 'with', 'given', 'above', 'using', 'about',
                       'below']
    combined_stop_words = stop_words.union(set(redundant_words))
    filtered_texts = []
    stemmer = PorterStemmer()
    for text in texts:
        words = word_tokenize(text.lower())
        stemmed_words = [stemmer.stem(word) for word in words]
        filtered_text = " ".join(stemmed_words)
        filtered_texts.append(filtered_text)
    X_train, X_test, y_train, y_test = train_test_split(filtered_texts, labels, test_size=0.2, random_state=42)
    vectorizer = CountVectorizer(lowercase=True, ngram_range=(1, 2), stop_words=list(combined_stop_words))
    X_train_vec = vectorizer.fit_transform(X_train, y_train)
    X_test_vec = vectorizer.transform(X_test)
    model = MultinomialNB(alpha=0.5)
    model.fit(X_train_vec, y_train)
    with open(question_classifier_vectorizer_path, 'wb') as vec_file:
        pickle.dump(vectorizer, vec_file)
    train_score = accuracy_score(y_train, model.predict(X_train_vec))
    print("---------------------------------------------------------")
    print("training accuracy: " + str(train_score))
    print("---------------------------------------------------------")
    print(classification_report(y_train, model.predict(X_train_vec)))
    test_score = accuracy_score(y_test, model.predict(X_test_vec))
    print("---------------------------------------------------------")
    print("test accuracy: " + str(test_score))
    print("---------------------------------------------------------")
    print(classification_report(y_test, model.predict(X_test_vec)))
    with open(question_classifier_model_path, 'wb') as file:
        pickle.dump(model, file)
