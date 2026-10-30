"""Small report-generation web app."""

import logging
import os

from flask import Flask, jsonify, request, send_from_directory
from openai import OpenAI, OpenAIError
from dotenv import load_dotenv

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)
load_dotenv()

app = Flask(__name__, static_folder="static")

MAX_TOPIC_LENGTH = 200
DEFAULT_MODEL = "gpt-4o-mini"


def generate_report(topic: str) -> str:
    """Generate a report with the configured OpenAI model."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is not configured")

    client = OpenAI(api_key=api_key, timeout=30.0, max_retries=1)
    response = client.responses.create(
        model=os.getenv("OPENAI_MODEL", DEFAULT_MODEL),
        instructions=(
            "Write a clear, useful, medium-length report about the topic provided. "
            "Use these headings: Title, Overview, Key Points, and Conclusion. "
            "Use plain text, with headings on separate lines. Do not invent precise "
            "statistics, quotations, or citations. If a detail is uncertain, say so."
        ),
        input=topic,
        max_output_tokens=1000,
    )
    return (response.output_text or "").strip()


@app.get("/")
def home():
    """Serve the single-page frontend."""
    return send_from_directory(app.static_folder, "index.html")


@app.get("/healthz")
def health_check():
    """Basic container health endpoint; does not call the AI provider."""
    return jsonify(status="ok")


@app.post("/api/generate")
def api_generate():
    """Generate one report from a topic supplied as JSON."""
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify(error="Send a JSON object containing a topic."), 400

    topic = payload.get("topic")
    if not isinstance(topic, str) or not topic.strip():
        return jsonify(error="Enter a report topic."), 400

    topic = topic.strip()
    if len(topic) > MAX_TOPIC_LENGTH:
        return jsonify(error=f"Topic must be {MAX_TOPIC_LENGTH} characters or fewer."), 400

    if not os.getenv("OPENAI_API_KEY"):
        return jsonify(error="OPENAI_API_KEY is not configured for this application."), 503

    try:
        report = generate_report(topic)
    except OpenAIError:
        logger.exception("The AI provider failed to generate a report")
        return jsonify(error="Report generation failed. Check the API key, quota, or provider status."), 502
    except ValueError:
        logger.exception("Report generation configuration error")
        return jsonify(error="Report generation is not configured correctly."), 503

    if not report:
        logger.error("The AI provider returned an empty report")
        return jsonify(error="The AI provider returned an empty report. Please try again."), 502

    return jsonify(topic=topic, report=report)


if __name__ == "__main__":
    # For local development only. The Docker image uses Gunicorn.
    app.run(host="127.0.0.1", port=5000, debug=False)
