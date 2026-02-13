# app.py
import os
import tempfile
import subprocess
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import openai
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__, template_folder=".")

SYSTEM_PROMPT = """You are an expert Python developer and debugger. The user gives you:
1) the original Python source code
2) static analyzer output (pylint)
Your job:
- Provide a concise diagnosis (2-4 lines)
- Provide a clear, minimal code fix (show only the changed function or a patch)
- Explain root cause in simple terms (2-4 sentences)
- Provide 1 simple test or command the user can run to verify the fix

Use markdown and a code block for any code. Be short and actionable.
"""

def run_pylint_on_code(code: str) -> str:
    with tempfile.NamedTemporaryFile(suffix=".py", delete=False, mode="w") as tf:
        tf.write(code)
        tmpname = tf.name
    try:
        # Run pylint; you can also use flake8
        res = subprocess.run(
            ["pylint", tmpname, "--score=no"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=10
        )
        output = res.stdout + ("\nSTDERR:\n" + res.stderr if res.stderr else "")
    except Exception as e:
        output = f"Pylint run failed: {e}"
    finally:
        try:
            os.unlink(tmpname)
        except Exception:
            pass
    return output

def ask_llm(code: str, lint_output: str) -> str:
    prompt = f"""User code:
```\n{code}\n```

Pylint output:
```\n{lint_output}\n```

Follow the SYSTEM instructions provided earlier strictly."""
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini", # replace if you want another model
        messages=[
            {"role":"system","content":SYSTEM_PROMPT},
            {"role":"user","content":prompt}
        ],
        max_tokens=800,
        temperature=0.1,
    )
    return response.choices[0].message.content

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    code = data.get("code", "")
    if not code:
        return jsonify({"error":"No code provided"}), 400

    lint_out = run_pylint_on_code(code)
    try:
        llm_reply = ask_llm(code, lint_out)
    except Exception as e:
        return jsonify({"error":"LLM call failed", "detail": str(e)}), 500

    return jsonify({
        "lint": lint_out,
        "analysis": llm_reply
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
