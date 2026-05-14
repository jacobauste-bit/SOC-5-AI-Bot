# SeaTalk AI Bot (Powered by Claude)

A simple SeaTalk bot that replies to messages using Claude AI.

---

## Files
- `app.py` — Main bot code
- `requirements.txt` — Python dependencies
- `Procfile` — Tells Render how to start the app

---

## Setup & Deploy on Render (Free)

### Step 1: Upload to GitHub
1. Create a free account at https://github.com
2. Create a new repository (e.g. `seatalk-bot`)
3. Upload all 3 files: `app.py`, `requirements.txt`, `Procfile`

### Step 2: Deploy on Render
1. Go to https://render.com and sign up for free
2. Click **New → Web Service**
3. Connect your GitHub repo
4. Set these settings:
   - **Environment:** Python
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`

### Step 3: Set Environment Variables in Render
Under your service → **Environment**, add:
- `ANTHROPIC_API_KEY` = your Anthropic API key
- `SEATALK_BOT_TOKEN` = your SeaTalk bot token (from SeaTalk Developer Portal)

### Step 4: Get your Webhook URL
After deploying, Render gives you a URL like:
```
https://your-bot-name.onrender.com
```
Your webhook endpoint will be:
```
https://your-bot-name.onrender.com/webhook
```

### Step 5: Set Webhook in SeaTalk
1. Go to the SeaTalk Developer Portal
2. Open your bot settings
3. Paste your webhook URL:
   `https://your-bot-name.onrender.com/webhook`
4. Save — your bot is live! 🎉

---

## How it works
1. User sends a message to your bot in SeaTalk
2. SeaTalk sends the message to your webhook URL
3. Your server sends it to Claude AI
4. Claude replies and your bot sends the reply back to SeaTalk
