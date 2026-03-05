from flask import Flask, render_template, request, jsonify
import subprocess
import os

app = Flask(__name__, template_folder="templates", static_folder="static")
TEMP_FILE = "temp_code.py"

def run_pylint(code: str) -> str:
    """Run pylint locally and return the output."""
    with open(TEMP_FILE, "w") as f:
        f.write(code)
    try:
        res = subprocess.run(
            ["pylint", TEMP_FILE, "--score=no"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=10
        )
        output = res.stdout + ("\nSTDERR:\n" + res.stderr if res.stderr else "")
    except Exception as e:
        output = f"Pylint failed: {e}"
    finally:
        if os.path.exists(TEMP_FILE):
            os.remove(TEMP_FILE)
    return output

def generate_suggestions(lint_output: str) -> str:
    """Generate simple suggestions based on common pylint messages."""
    suggestions = []
    for line in lint_output.splitlines():
        if "unused-variable" in line:
            suggestions.append("Check for variables that are defined but not used.")
        elif "undefined-variable" in line:
            suggestions.append("Variable used before definition.")
        elif "bad-indentation" in line:
            suggestions.append("Fix indentation; Python requires consistent spacing.")
        elif "import-error" in line:
            suggestions.append("Check that modules are installed or imported correctly.")
        elif "missing-function-docstring" in line:
            suggestions.append("Add docstrings for functions.")
    if not suggestions:
        suggestions.append("No major issues detected; code looks clean.")
    return "\n".join(suggestions)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    code = data.get("code", "").strip()
    if not code:
        return jsonify({"error": "No code provided"}), 400

    lint_output = run_pylint(code)
    suggestions = generate_suggestions(lint_output)

    # Optional logging
    with open("debug_log.txt", "a", encoding="utf-8") as log:
        log.write(f"\n---\nCode:\n{code}\nLint:\n{lint_output}\nSuggestions:\n{suggestions}\n")

    return jsonify({
        "lint": lint_output,
        "suggestions": suggestions
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)