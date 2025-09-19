from flask import Flask, request, jsonify, render_template
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

# Route for the homepage
@app.route('/')
def index():
    return render_template('index.html')

# Route for generating a response using OpenAI
@app.route('/generate_response', methods=['POST'])
def generate_response():
    try:
        data = request.json
        mode = data.get("mode", "default")
        text = data.get("text", "")
        language = data.get("language", "Spanish")
        if mode == 'translator' and not text:
            return jsonify({"error": "Text is required for translation"}), 400
        if mode == 'default' and not text:
            return jsonify({"error": "Prompt is required"}), 400

        print(f"Prompt received: {text} (mode: {mode})")  # Log the received prompt

        # Prompt templates for each mode
        if mode == 'translator':
            prompt = f"Translate the following text to {language}: {text}"
        elif mode == 'weather':
            prompt = "What is the weather today?"
        elif mode == 'news':
            prompt = "Summarize the latest news headlines."
        elif mode == 'finance':
            prompt = "Give me a tip to save money or manage my finances better."
        else:
            prompt = text

        # Call the OpenAI Chat API (for openai>=1.0.0)
        response = openai.chat.completions.create(
            model="gpt-5-mini",
            messages=[
                {"role": "system", "content": "You are AYBot, a helpful personal assistant."},
                {"role": "user", "content": prompt},
            ],
            #temperature=0.8,
            max_completion_tokens=200,
            top_p=1
        )

        response_text = response.choices[0].message.content.strip()
        return jsonify({"response_text": response_text})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
