from flask import Flask, render_template, request, jsonify
from model_handler import debugger

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

# THIS IS THE CRITICAL PART FOR THE BUTTON:
@app.route('/debug', methods=['POST'])
def debug_code():
    data = request.json
    code = data.get('code')
    language = data.get('language')
    
    if not code:
        return jsonify({"error": "No code provided"}), 400
    
    try:
        # This talks to your AI model
        analysis = debugger.analyze_code(code, language)
        return jsonify({"analysis": analysis})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # We turn off reloader to prevent the "Double Load" crash
    app.run(debug=True, use_reloader=False, port=5000)