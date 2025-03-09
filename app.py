"""from flask import Flask, render_template, request
import pickle
import json
import random

app = Flask(__name__)

# Load the trained model and vectorizer
with open('model/chatbot_model.pkl', 'rb') as f:
    best_model = pickle.load(f)

with open('model/vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

# Load the intents data
with open('dataset/intents1.json', 'r') as f:
    intents = json.load(f)

def chatbot_response(user_input):
    input_text = vectorizer.transform([user_input])
    predicted_intent = best_model.predict(input_text)[0]

    for intent in intents['intents']:
        if intent['tag'] == predicted_intent:
            response = random.choice(intent['responses'])
            break

    return response

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input']
    response = chatbot_response(user_input)
    return response

if __name__ == '__main__':
    app.run(debug=True)
"""
'''
from flask import Flask, render_template, request
from joblib import load
import json
import random

app = Flask(__name__)

# Load the trained model (using joblib)
best_model = load('C:/Users/admin/Desktop/College-Chatbot-Using-ML-and-NLP-main/model/chatbot_model.pkl')

# Load the intents data
with open('dataset/intents1.json', 'r') as f:
    intents = json.load(f)


def chatbot_response(user_input):
    predicted_intent = best_model.predict([user_input])[0]

    for intent in intents['intents']:
        if intent['tag'] == predicted_intent:
            response = random.choice(intent['responses'])
            break

    return response


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input']
    response = chatbot_response(user_input)
    return response


if __name__ == '__main__':
    app.run(debug=True)'''

from flask import Flask, render_template, request, jsonify
from joblib import load
import json
import random

app = Flask(__name__)

# Load the trained model and vectorizer
MODEL_PATH = 'C:/Users/admin/Desktop/College-Chatbot-Using-ML-and-NLP-main/model/chatbot_model.pkl'
VECTORIZER_PATH = 'C:/Users/admin/Desktop/College-Chatbot-Using-ML-and-NLP-main/model/vectorizer.pkl'
INTENTS_PATH = 'C:/Users/admin/Desktop/College-Chatbot-Using-ML-and-NLP-main/dataset/intents1.json'

try:
    best_model = load(MODEL_PATH)
    vectorizer = load(VECTORIZER_PATH)
except Exception as e:
    print(f"Error loading model/vectorizer: {e}")
    exit(1)

# Load the intents JSON file
try:
    with open(INTENTS_PATH, 'r', encoding='utf-8') as f:
        intents = json.load(f)
except Exception as e:
    print(f"Error loading intents file: {e}")
    exit(1)

def chatbot_response(user_input):
    """Processes user input, predicts intent, and returns a response."""
    try:
        input_text = vectorizer.transform([user_input])  # Convert text to numerical format
        predicted_intent = best_model.predict(input_text)[0]

        # Find the corresponding response from intents.json
        for intent in intents['intents']:
            if intent['tag'] == predicted_intent:
                return random.choice(intent['responses'])

        return "Sorry, I didn't understand that."

    except Exception as e:
        print(f"Error in chatbot_response: {e}")
        return "I'm having some trouble understanding. Try again!"

@app.route('/')
def home():
    """Renders the chatbot webpage."""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handles chatbot responses."""
    user_input = request.form.get('user_input', '')
    response = chatbot_response(user_input)
    return jsonify({"response": response})  # Returns JSON response

if __name__ == '__main__':
    app.run(debug=True)
