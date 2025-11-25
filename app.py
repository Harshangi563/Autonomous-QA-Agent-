# -------------------------------
# Load environment variables FIRST
# -------------------------------
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, request, jsonify
from agent.ingestion import ingest_documents
from agent.test_case_agent import generate_test_case
from agent.script_agent import generate_selenium_script
import traceback
import json

app = Flask(__name__)
rag_engine = None  # Global RAG engine instance

# 📁 Upload Files + Build Knowledge Base
@app.route("/upload_files", methods=["POST"])
def upload_files():
    files = request.files.getlist("files")
    html_file = request.files.get("html")

    if not files or not html_file:
        return jsonify({"error": "Upload both support documents and checkout.html"}), 400

    global rag_engine
    try:
        rag_engine = ingest_documents(files, html_file)
        return jsonify({"message": "Knowledge Base built successfully"}), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": f"Error during ingestion: {str(e)}"}), 500


# 🧪 Test Case Generation
@app.route("/generate_test_cases", methods=["POST"])
def generate_cases():
    global rag_engine
    query = request.json.get("query")

    if not rag_engine:
        return jsonify({"error": "Knowledge Base not built yet"}), 400

    if not query or not isinstance(query, str):
        return jsonify({"error": "Invalid input. Please provide a query string."}), 400

    try:
        results = generate_test_case(query, rag_engine)
        return jsonify(results), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": f"Test case generation failed: {str(e)}"}), 500


# 🛠 Selenium Script Generation (Markdown-based)
@app.route("/generate_script", methods=["POST"])
def generate_script():
    global rag_engine
    test_case_row = request.json.get("test_case_row")  # ⬅ Expect Markdown format

    if not rag_engine:
        return jsonify({"error": "Knowledge Base not built yet"}), 400

    if not test_case_row or not isinstance(test_case_row, str):
        return jsonify({
            "error": "Invalid test case. Provide a valid Markdown row string."
        }), 400

    try:
        result = generate_selenium_script(test_case_row, rag_engine)
        return jsonify({
            "script": result["script"], 
            "file_path": result["file_path"]
        }), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": f"Script generation failed: {str(e)}"}), 500


# 🚀 Start Flask Server
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
