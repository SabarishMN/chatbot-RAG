from flask import Flask, request, jsonify
from flask_cors import CORS
import PyPDF2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
CORS(app)  # This allows all origins

# Initialize an empty document store
document_store = {}

@app.route('/upload', methods=['POST'])
def upload_document():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file and file.filename.endswith('.pdf'):
        # Process and store the PDF content
        content = extract_text_from_pdf(file)
        document_store[file.filename] = content
        return jsonify({"message": "File uploaded successfully"}), 200
    return jsonify({"error": "Invalid file format"}), 400

@app.route('/query', methods=['POST'])
def query_chatbot():
    query = request.json.get('query')
    if not query:
        return jsonify({"error": "No query provided"}), 400
    
    # Perform similarity search and return the most relevant answer
    answer = find_most_relevant_answer(query)
    return jsonify({"answer": answer}), 200

def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def find_most_relevant_answer(query):
    if not document_store:
        return "I'm sorry, but I don't have any information yet. Please upload some documents first."
    
    vectorizer = TfidfVectorizer()
    corpus = list(document_store.values()) + [query]
    tfidf_matrix = vectorizer.fit_transform(corpus)
    cosine_similarities = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1]).flatten()
    most_similar_doc_index = cosine_similarities.argmax()
    return list(document_store.values())[most_similar_doc_index]

def run_backend():
    app.run(debug=False)

if __name__ == '__main__':
    run_backend()