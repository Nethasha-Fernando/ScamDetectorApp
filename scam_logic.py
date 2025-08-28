# List of known scam keywords/phrases
scam_keywords = [
    "you've won", "click this link", "urgent", "account suspended",
    "verify your identity", "lottery", "free gift", "OTP", "bank details", "limited time","suspended", "click here", "reactivate", "urgent", "verify", "login now", "reset password"
]

# Function to check if the message contains any scammy keywords
def detect_scam_keywords(message):
    found_keywords = []

    for keyword in scam_keywords:
        if keyword.lower() in message.lower():
            found_keywords.append(keyword)
    return found_keywords

import re

def highlight_keywords(message, keywords):

    for keyword in keywords:
        pattern = re.compile(re.escape(keyword), re.IGNORECASE)
        message = pattern.sub(lambda match: f"<mark>{match.group(0)}</mark>", message)
    return message


import os
import openai

def ask_gpt_if_scam(message):
    demo_mode = os.getenv("DEMO_MODE", "true").lower() == "true"

    if demo_mode:
        # Show this message in the demo version
        return "🧪 This is a public demo. AI analysis via OpenAI is disabled to avoid API charges."

    # If not in demo mode, use real OpenAI API
    openai.api_key = os.getenv("OPENAI_API_KEY")

    try:
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that identifies if a message sounds like a scam."},
                {"role": "user", "content": f"Does this message sound like a scam? '{message}'"}
            ],
            max_tokens=100,
            temperature=0.2
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ GPT error: {str(e)}"


def scam_confidence_score(keywords_found):
    if not keywords_found:
        return 10  # Low scam confidence if nothing was found
    score = min(10 + len(keywords_found) * 20, 100)  # every keyword = 20 points
    return score



