from flask import Blueprint, request, jsonify
from database import content_collection
from datetime import datetime
from groq import Groq
import os
import re
from dotenv import load_dotenv

load_dotenv()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

content_bp = Blueprint("content", __name__)


@content_bp.route("/generate", methods=["POST"])
def generate_content():
    data = request.get_json()
    content_type = data.get("type")
    topic = data.get("topic")
    tone = data.get("tone", "professional")
    platform = data.get("platform", "youtube")
    user_id = data.get("user_id")
    language = data.get("language", "english")
    if language == "hindi":
        prompt = f"""Aap ek professional content creator hain.
{platform} ke liye {content_type} likhiye topic: {topic}
Tone: {tone}
Hindi mein likhiye. Creative aur engaging rakho."""
    elif language == "hinglish":
        prompt = f"""You are a content creator.
Write {content_type} for {platform} about: {topic}
Tone: {tone}
Write in Hinglish mix of Hindi and English. Keep it relatable."""
    else:
        prompt = f"""You are a professional content creator.
Generate {content_type} for {platform} about: {topic}
Tone: {tone}
Be creative, engaging and optimized for {platform}."""

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500
    )
    generated_text = response.choices[0].message.content

    content_collection.insert_one({
        "user_id": user_id,
        "type": content_type,
        "topic": topic,
        "tone": tone,
        "platform": platform,
        "language": language,
        "output": generated_text,
        "created_at": datetime.utcnow()
    })

    return jsonify({"success": True, "output": generated_text}), 200


@content_bp.route("/history", methods=["GET"])
def get_history():
    user_id = request.args.get("user_id")
    contents = list(content_collection.find(
        {"user_id": user_id},
        {"_id": 0}
    ).sort("created_at", -1).limit(20))
    return jsonify({"history": contents}), 200


@content_bp.route("/score", methods=["POST"])
def get_score():
    data = request.get_json()
    content = data.get("content", "")
    content_type = data.get("type", "")
    platform = data.get("platform", "")

    prompt = f"""Analyze this {content_type} for {platform}:
"{content}"
Respond ONLY in this exact format:
READABILITY: [number]
ENGAGEMENT: [number]
SEO: [number]
LENGTH: [number]
TONE: [number]
SUGGESTION: [one line tip]"""

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200
    )

    output = response.choices[0].message.content
    scores = {}

    for line in output.split('\n'):
        if ':' in line:
            key, val = line.split(':', 1)
            key = key.strip().lower()
            val = val.strip()
            if key in ['readability', 'engagement', 'seo', 'length', 'tone']:
                nums = re.findall(r'\d+', val)
                scores[key] = min(int(nums[0]), 100) if nums else 70
            elif key == 'suggestion':
                scores['suggestion'] = val

    return jsonify({"success": True, "scores": scores}), 200


@content_bp.route("/analyze-tone", methods=["POST"])
def analyze_tone():
    data = request.get_json()
    content = data.get("content", "")

    prompt = f"""Analyze the tone of this content:
"{content}"
Respond ONLY in this exact format:
TONE: [one word]
SENTIMENT: [Positive/Negative/Neutral]
CONFIDENCE: [number 0-100]
SUMMARY: [one sentence]
IMPROVE: [one tip]"""

    response = groq_client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150
    )

    output = response.choices[0].message.content
    result = {}

    for line in output.split('\n'):
        if ':' in line:
            key, val = line.split(':', 1)
            result[key.strip().lower()] = val.strip()

    return jsonify({"success": True, "analysis": result}), 200