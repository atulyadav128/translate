# AYBot - Personal AI Assistant

A Flask-based chatbot that provides various AI-powered services including translation, weather updates, news summaries, and general conversation.

## Features

- 🤖 General AI chat
- 🌍 Text translation
- 🌤️ Weather information
- 📰 News summaries
- 💰 Financial tips

## Local Development

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```
4. Run the app: `python app.py`
5. Access at `http://localhost:5000`

## Deployment on Render

### Method 1: Using render.yaml (Recommended)

1. Push your code to GitHub
2. Connect your GitHub repo to Render
3. Render will automatically detect the `render.yaml` file
4. Add your `OPENAI_API_KEY` environment variable in Render dashboard
5. Deploy!

### Method 2: Manual Setup

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Python Version**: 3.11+
4. Add environment variable:
   - **Key**: `OPENAI_API_KEY`
   - **Value**: Your OpenAI API key
5. Deploy!

## Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required)

## Tech Stack

- Flask (Python web framework)
- OpenAI GPT API
- Gunicorn (WSGI server)
- HTML/CSS/JavaScript (frontend)
