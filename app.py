from flask import Flask, request, jsonify
import anthropic
import requests
import os

app = Flask(__name__)

# Load from environment variables (set these in Render)
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
SEATALK_BOT_TOKEN = os.environ.get("SEATALK_BOT_TOKEN")  # From SeaTalk Developer Portal

# Anthropic client
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


def send_seatalk_message(conversation_id, text):
    """Send a message back to SeaTalk."""
    url = "https://openapi.seatalk.io/messaging/v2/single_chat"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {SEATALK_BOT_TOKEN}"
    }
    payload = {
        "conversation_id": conversation_id,
        "message": {
            "tag": "text",
            "text": {"content": text}
        }
    }
    response = requests.post(url, json=payload, headers=headers)
    return response


def ask_claude(user_message):
    """Send a message to Claude and get a response."""
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        messages=[
            {"role": "user", "content": user_message}
        ]
    )
    return message.content[0].text


@app.route("/webhook", methods=["POST"])
def webhook():
    """Receive messages from SeaTalk and reply using Claude."""
    data = request.json

    # Basic validation
    if not data:
        return jsonify({"status": "no data"}), 400

    # Handle SeaTalk verification challenge
    if "seatalk_challenge" in data:
        return jsonify({"seatalk_challenge": data["seatalk_challenge"]}), 200

    try:
        # Extract message details from SeaTalk payload
        event = data.get("event", {})
        message_type = event.get("type")

        # Only handle incoming text messages
        if message_type != "message_created":
            return jsonify({"status": "ignored"}), 200

        message = event.get("message", {})
        text = message.get("text", {}).get("content", "")
        conversation_id = event.get("conversation_id", "")

        if not text or not conversation_id:
            return jsonify({"status": "missing fields"}), 400

        # Get Claude's reply
        reply = ask_claude(text)

        # Send it back to SeaTalk
        send_seatalk_message(conversation_id, reply)

        return jsonify({"status": "ok"}), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/", methods=["GET"])
def health():
    return "SeaTalk AI Bot is running!", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
