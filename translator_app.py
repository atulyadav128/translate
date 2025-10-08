from flask import Flask, request, jsonify, render_template
import openai
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

# Supported languages
LANGUAGES = {
    'en': 'English',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'it': 'Italian',
    'pt': 'Portuguese',
    'nl': 'Dutch',
    'ru': 'Russian',
    'zh': 'Chinese',
    'ja': 'Japanese',
    'ko': 'Korean',
    'ar': 'Arabic',
    'hi': 'Hindi',
    'tr': 'Turkish',
    'pl': 'Polish',
    'sv': 'Swedish',
    'no': 'Norwegian',
    'da': 'Danish',
    'fi': 'Finnish',
    'el': 'Greek'
}

@app.route('/')
def index():
    return render_template('translator.html')

@app.route('/api/translate', methods=['POST'])
def translate():
    try:
        data = request.json
        text = data.get('text', '').strip()
        source_lang = data.get('source_lang', 'auto')
        target_lang = data.get('target_lang', 'en')
        
        if not text:
            return jsonify({'error': 'Text is required'}), 400
        
        if not openai.api_key:
            return jsonify({'error': 'OpenAI API key not configured'}), 500
        
        # Build the prompt based on source language
        if source_lang == 'auto':
            # For auto-detect, first detect the language, then set smart target
            prompt = f"""Detect the language of this text.

Text: {text}

Respond ONLY with a JSON object in this exact format (no additional text):
{{
    "detected_language": "language name",
    "detected_language_code": "ISO 639-1 code"
}}"""
            
            # Detect language first
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a language detection expert. Always respond with valid JSON only, no additional text."
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=100
            )
            
            result_text = response.choices[0].message.content.strip()
            if result_text.startswith('```'):
                lines = result_text.split('\n')
                result_text = '\n'.join(lines[1:-1]) if len(lines) > 2 else result_text
                result_text = result_text.replace('```json', '').replace('```', '').strip()
            
            detection_result = json.loads(result_text)
            detected_code = detection_result.get('detected_language_code', 'unknown').lower()
            
            # Smart target language selection: Spanish <-> English
            if detected_code in ['es', 'spa', 'spanish']:
                target_lang = 'en'
                target_lang_name = 'English'
            elif detected_code in ['en', 'eng', 'english']:
                target_lang = 'es'
                target_lang_name = 'Spanish'
            else:
                # For other languages, default to English
                target_lang = 'en'
                target_lang_name = 'English'
            
            # Now translate with detected language
            detected_lang_name = detection_result.get('detected_language', 'Unknown')
            prompt = f"""Translate this text from {detected_lang_name} to {target_lang_name}.

Text: {text}

Respond ONLY with a JSON object in this exact format (no additional text):
{{
    "detected_language": "{detected_lang_name}",
    "detected_language_code": "{detected_code}",
    "translated_text": "the translation"
}}"""
        else:
            source_lang_name = LANGUAGES.get(source_lang, source_lang)
            target_lang_name = LANGUAGES.get(target_lang, target_lang)
            prompt = f"""Translate this text from {source_lang_name} to {target_lang_name}.

Text: {text}

Respond ONLY with a JSON object in this exact format (no additional text):
{{
    "detected_language": "{source_lang_name}",
    "detected_language_code": "{source_lang}",
    "translated_text": "the translation"
}}"""
        
        # Call OpenAI API
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system", 
                    "content": "You are a professional translator. Always respond with valid JSON only, no additional text or explanations."
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1000
        )
        
        result_text = response.choices[0].message.content.strip()
        
        # Parse the JSON response
        # Remove markdown code blocks if present
        if result_text.startswith('```'):
            lines = result_text.split('\n')
            result_text = '\n'.join(lines[1:-1]) if len(lines) > 2 else result_text
            result_text = result_text.replace('```json', '').replace('```', '').strip()
        
        result = json.loads(result_text)
        
        return jsonify({
            'success': True,
            'original_text': text,
            'translated_text': result.get('translated_text', ''),
            'detected_language': result.get('detected_language', 'Unknown'),
            'detected_language_code': result.get('detected_language_code', 'unknown'),
            'target_language': LANGUAGES.get(target_lang, target_lang),
            'target_language_code': target_lang
        })
        
    except json.JSONDecodeError as e:
        print(f"JSON Parse Error: {e}")
        print(f"Response was: {result_text}")
        return jsonify({
            'error': 'Failed to parse translation response',
            'details': str(e)
        }), 500
    except Exception as e:
        print(f"Translation Error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/detect-language', methods=['POST'])
def detect_language():
    try:
        data = request.json
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({'error': 'Text is required'}), 400
        
        if not openai.api_key:
            return jsonify({'error': 'OpenAI API key not configured'}), 500
        
        prompt = f"""Detect the language of this text: "{text}"

Respond ONLY with a JSON object in this exact format (no additional text):
{{
    "language": "language name",
    "language_code": "ISO 639-1 code",
    "confidence": "high/medium/low"
}}"""
        
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a language detection expert. Always respond with valid JSON only."
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            max_tokens=100
        )
        
        result_text = response.choices[0].message.content.strip()
        
        # Remove markdown code blocks if present
        if result_text.startswith('```'):
            lines = result_text.split('\n')
            result_text = '\n'.join(lines[1:-1]) if len(lines) > 2 else result_text
            result_text = result_text.replace('```json', '').replace('```', '').strip()
        
        result = json.loads(result_text)
        
        return jsonify({
            'success': True,
            'language': result.get('language', 'Unknown'),
            'language_code': result.get('language_code', 'unknown'),
            'confidence': result.get('confidence', 'medium')
        })
        
    except Exception as e:
        print(f"Language Detection Error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/languages', methods=['GET'])
def get_languages():
    return jsonify({'languages': LANGUAGES})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=True)


