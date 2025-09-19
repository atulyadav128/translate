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
        
        # Check if API key is available
        if not openai.api_key:
            return jsonify({"error": "OpenAI API key not configured. Please add OPENAI_API_KEY to your .env file."}), 500
        
        if mode == 'translator' and not text:
            return jsonify({"error": "Text is required for translation"}), 400
        if mode == 'default' and not text:
            return jsonify({"error": "Prompt is required"}), 400

        print(f"Prompt received: {text} (mode: {mode})")

        # Prompt templates for each mode
        if mode == 'translator':
            prompt = f"Translate the following text to {language}: {text}"
        elif mode == 'weather':
            prompt = f"Provide current weather information for {text if text else 'my location'}. Include temperature, conditions, and a brief forecast."
        elif mode == 'news':
            prompt = f"Summarize the latest news headlines{f' about {text}' if text else ''}. Focus on major events and important updates."
        elif mode == 'finance':
            prompt = f"Give me practical financial advice{f' about {text}' if text else ''}. Include tips for saving money, budgeting, or investment strategies."
        elif mode == 'code_helper':
            prompt = f"I need help with programming{f' related to {text}' if text else ''}. Provide code examples, explanations, and best practices."
        elif mode == 'study_buddy':
            prompt = f"Help me study{f' {text}' if text else ''}. Provide explanations, examples, and study tips to help me understand the topic better."
        elif mode == 'creative_writer':
            prompt = f"Help me with creative writing{f' about {text}' if text else ''}. Provide inspiration, structure suggestions, and writing tips."
        elif mode == 'health_advisor':
            prompt = f"Provide general health and wellness advice{f' about {text}' if text else ''}. Note: This is for informational purposes only, not medical advice."
        elif mode == 'travel_guide':
            prompt = f"Provide travel information and tips{f' for {text}' if text else ''}. Include recommendations for places to visit, activities, and travel tips."
        else:
            prompt = text

        # Call the OpenAI Chat API
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are AYBot, a helpful personal assistant."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=500,
            temperature=0.7
        )

        response_text = response.choices[0].message.content.strip()
        return jsonify({"response_text": response_text})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)