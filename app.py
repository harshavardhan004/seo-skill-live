from flask import Flask, request, jsonify
import subprocess
import traceback

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
        result = subprocess.run(
            ["python", "scripts/generate_report.py", url],
            capture_output=True,
            text=True
        )

        return {
            "status": "Report Generated",
            "output": result.stdout,
            "error": result.stderr
        }

    except Exception as e:
        return {
            "error": str(e),
            "trace": traceback.format_exc()
        }, 500


if __name__ == "__main__":
    app.run()