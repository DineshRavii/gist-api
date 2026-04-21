import logging
import os
import requests
from flask import Flask, jsonify
from prometheus_flask_exporter import PrometheusMetrics


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
metrics = PrometheusMetrics(app)


@app.route('/health')
def health():
    logger.info("Health check called")
    return jsonify({"status": "healthy"}), 200

GITHUB_API_BASE = "https://api.github.com"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")

@app.route('/<username>')
def get_gists(username):
    logger.info(f"Fetching gists for user: {username}")
    
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"
    
    response = requests.get(
        f"{GITHUB_API_BASE}/users/{username}/gists",
        headers=headers
    )
    
    if response.status_code == 404:
        logger.warning(f"User not found: {username}")
        return jsonify({"error": f"User '{username}' not found"}), 404
    
    if response.status_code != 200:
        logger.error(f"GitHub API error: {response.status_code}")
        return jsonify({"error": "GitHub API error", "status": response.status_code}), 502
    
    gists = response.json()
    logger.info(f"Found {len(gists)} gists for user: {username}")
    
    result = [
        {
            "id": gist["id"],
            "description": gist["description"],
            "url": gist["html_url"],
            "created_at": gist["created_at"],
            "updated_at": gist["updated_at"],
            "files": list(gist["files"].keys())
        }
        for gist in gists
    ]
    
    return jsonify(result), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)