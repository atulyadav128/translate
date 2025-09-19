from flask import Flask, request, jsonify, render_template, session
import openai
import os
import json
import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-change-this')

# In-memory storage for chat history (in production, use a database)
chat_history = {}

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

        # Call the OpenAI Chat API (for openai>=1.0.0)
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are AYBot, a helpful personal assistant."},
                {"role": "user", "content": prompt},
            ],
            #temperature=0.8,
            max_completion_tokens=200,
            top_p=1
        )

        response_text = response.choices[0].message.content.strip()
        
        # Store chat history
        session_id = session.get('session_id', str(datetime.datetime.now().timestamp()))
        session['session_id'] = session_id
        
        if session_id not in chat_history:
            chat_history[session_id] = []
        
        chat_entry = {
            'timestamp': datetime.datetime.now().isoformat(),
            'mode': mode,
            'user_input': text,
            'response': response_text
        }
        chat_history[session_id].append(chat_entry)
        
        return jsonify({
            "response_text": response_text,
            "session_id": session_id,
            "timestamp": chat_entry['timestamp']
        })

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

# Route to get chat history
@app.route('/chat_history', methods=['GET'])
def get_chat_history():
    session_id = session.get('session_id')
    if not session_id or session_id not in chat_history:
        return jsonify({"history": []})
    
    return jsonify({"history": chat_history[session_id]})

# Route to clear chat history
@app.route('/clear_history', methods=['POST'])
def clear_history():
    session_id = session.get('session_id')
    if session_id and session_id in chat_history:
        chat_history[session_id] = []
    return jsonify({"message": "History cleared"})

# Route to export chat history
@app.route('/export_history', methods=['GET'])
def export_history():
    session_id = session.get('session_id')
    if not session_id or session_id not in chat_history:
        return jsonify({"error": "No history found"}), 404
    
    history_data = {
        'session_id': session_id,
        'exported_at': datetime.datetime.now().isoformat(),
        'conversations': chat_history[session_id]
    }
    
    return jsonify(history_data)

# Route to get available modes
@app.route('/modes', methods=['GET'])
def get_modes():
    modes = {
        'default': 'Ask Anything',
        'translator': 'Translator',
        'weather': 'Weather Info',
        'news': 'News Summary',
        'finance': 'Financial Advice',
        'code_helper': 'Code Helper',
        'study_buddy': 'Study Buddy',
        'creative_writer': 'Creative Writer',
        'health_advisor': 'Health Advisor',
        'travel_guide': 'Travel Guide'
    }
    return jsonify(modes)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
