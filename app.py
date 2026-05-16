from flask import Flask, render_template, request, Response, jsonify
from prometheus_client import Counter, generate_latest
from dotenv import load_dotenv

import traceback

from flipkart.data_ingestion import DataIngestor
from flipkart.rag_agent import RAGAgentBuilder

# Load environment variables
load_dotenv()

# Prometheus Metrics
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP Requests"
)

PREDICTION_COUNT = Counter(
    "model_predictions_total",
    "Total Model Predictions"
)


def create_app():

    app = Flask(
        __name__,
        template_folder="frontend/templates",
        static_folder="frontend/static"
    )

    app.secret_key = "super-secret-key"

    print("Loading vector store...")

    # Load vector database
    vector_store = DataIngestor().ingest(
        load_existing=True
    )

    print("Building RAG Chain...")

    # Build RAG Chain
    rag_chain = RAGAgentBuilder(
        vector_store
    ).build_agent()

    print("Application started successfully.")

    # ROUTES

    @app.route("/")
    def index():

        REQUEST_COUNT.inc()

        return render_template("index.html")

    @app.route("/get", methods=["POST"])
    def get_response():

        REQUEST_COUNT.inc()

        user_input = request.form.get("msg")

        if not user_input:
            return "No message received", 400

        # Convert to lowercase for greeting check
        cleaned_input = user_input.lower().strip()

        # Greeting handling
        greetings = [
            "hi",
            "hello",
            "hey",
            "hii",
            "good morning",
            "good evening",
            "good afternoon"
        ]

        if cleaned_input in greetings:

            return (
                "Hello 👋\n\n"
                "Welcome to Flipkart Chatbot!\n\n"
                "I can help you with:\n"
                "• Product recommendations\n"
                "• Product reviews\n"
                "• Budget shopping suggestions\n"
                "• Product comparisons\n"
                "• General queries\n\n"
                "Try asking:\n"
                "'Best earbuds under 2000'"
            )

        try:

            # Invoke RetrievalQA chain
            response = rag_chain.invoke(user_input)

            PREDICTION_COUNT.inc()

            if not response:
                return (
                    "Sorry, I couldn't generate a response."
                )

            assistant_message = response.get(
                "result",
                "No response generated."
            )

            return assistant_message

        except Exception as e:

            print("\n[ERROR] RAG invocation failed:\n")

            traceback.print_exc()

            return (
                f"An error occurred while "
                f"processing your request: {str(e)}",
                500
            )

    @app.route("/health")
    def health():

        return jsonify(
            {
                "status": "healthy"
            }
        ), 200

    @app.route("/metrics")
    def metrics():

        return Response(
            generate_latest(),
            mimetype="text/plain"
        )

    return app


# MAIN

if __name__ == "__main__":

    app = create_app()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )