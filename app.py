from flask import Flask, render_template, request, jsonify
from chatbot import ask_database

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json(silent=True) or {}
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"error": "Please enter a question."}), 400

    try:
        results = ask_database(question)
        return jsonify({"answer": results})
    except Exception:
        app.logger.exception("Chatbot request failed")
        return jsonify({
            "error": "Sorry, something went wrong while processing your question."
        }), 500


if __name__ == "__main__":
    app.run(debug=True)