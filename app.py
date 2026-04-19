from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route("/")
def home():
    return {"status": "SEO API Running"}

@app.route("/seo-audit", methods=["GET"])
def seo_audit():
    url = request.args.get("url")

    if not url:
        return {"error": "URL parameter missing"}, 400

    try:
        subprocess.run(["python", "scripts/generate_report.py", url])
        return {"status": "Report Generated", "url": url}

    except Exception as e:
        return {"error": str(e)}, 500


if __name__ == "__main__":
    app.run()