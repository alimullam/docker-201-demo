"""Docker 201 demo app.

A tiny inventory service with a friendly face. The homepage is a real
HTML page (nice on a webinar screen), and the API endpoints return JSON.
"""

import os
import platform
import sys

from flask import Flask, jsonify, render_template

app = Flask(__name__)

INVENTORY = [
    {"id": 1, "name": "whale-plush", "stock": 42},
    {"id": 2, "name": "container-mug", "stock": 17},
    {"id": 3, "name": "compose-stickers", "stock": 250},
]


@app.route("/")
def index():
    return render_template(
        "index.html",
        python_version=platform.python_version(),
        platform_info=platform.machine(),
        variant=os.environ.get("APP_VARIANT", "standard"),
    )


@app.route("/inventory")
def inventory():
    return jsonify(INVENTORY)


@app.route("/health")
def health():
    return jsonify(status="ok", python=sys.version.split()[0], variant=os.environ.get("APP_VARIANT", "standard"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
