from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)

with open('site_text.txt', 'r', encoding='utf-8') as f:
    website_text = f.read()

qa_pipeline = pipeline('question-answering')

@app.route('/ask', methods=['POST'])
def ask():
    question = request.json.get('question', '')
    if not question:
        return jsonify({'answer': "Please ask a question."})
    result = qa_pipeline(question=question, context=website_text)
    answer = result.get('answer', 'Sorry, I could not find an answer.')
    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(debug=True)
