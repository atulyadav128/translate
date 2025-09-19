# AYBot Setup Guide

## Quick Start

### 1. Create .env File
Create a file named `.env` in your project folder with your OpenAI API key:

```
OPENAI_API_KEY=your_actual_openai_api_key_here
```

### 2. Get OpenAI API Key
1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in
3. Go to API Keys section
4. Create a new API key
5. Copy the key and paste it in your `.env` file

### 3. Run the App
```bash
# Activate virtual environment
venv\Scripts\activate

# Run the app
python app.py
```

### 4. Access Your Bot
- **Local**: http://localhost:5000
- **Mobile**: http://192.168.1.209:5000 (replace with your computer's IP)

## Features

- 🤖 **10 AI Modes**: Ask Anything, Translator, Weather, News, Finance, Code Helper, Study Buddy, Creative Writer, Health Advisor, Travel Guide
- 📱 **Mobile-Friendly**: Works perfectly on phones
- 💬 **Real-time Chat**: Instant responses
- 🎨 **Modern UI**: Clean, professional interface

## Troubleshooting

### "No response generated" Error
- Check if your `.env` file exists and has the correct API key
- Make sure you have internet connection
- Verify your OpenAI account has credits

### "Module not found" Error
- Make sure virtual environment is activated: `venv\Scripts\activate`
- Install dependencies: `pip install -r requirements.txt`

## Deployment to Render

1. Push your code to GitHub
2. Go to [render.com](https://render.com)
3. Create new Web Service
4. Connect your GitHub repo
5. Add environment variable: `OPENAI_API_KEY`
6. Deploy!

Your AYBot will be live at a public URL!
