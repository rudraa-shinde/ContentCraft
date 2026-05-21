from flask import Blueprint, request, jsonify
from database import users_collection
import bcrypt
import jwt
import os
from datetime import datetime, timedelta

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if users_collection.find_one({"email": email}):
        return jsonify({"error": "Email already registered!"}), 400

    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    users_collection.insert_one({
        "name": name,
        "email": email,
        "password": hashed.decode("utf-8"),  # string me save karo
        "created_at": datetime.utcnow()
    })

    return jsonify({"message": "Account created successfully!"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = users_collection.find_one({"email": email})
    if not user:
        return jsonify({"error": "User not found!"}), 404

    # string ya bytes dono handle karo
    stored = user["password"]
    if isinstance(stored, str):
        stored = stored.encode("utf-8")

    if not bcrypt.checkpw(password.encode("utf-8"), stored):
        return jsonify({"error": "Wrong password!"}), 401

    token = jwt.encode({
        "user_id": str(user["_id"]),
        "email": email,
        "name": user["name"],
        "exp": datetime.utcnow() + timedelta(days=7)
    }, os.getenv("JWT_SECRET"), algorithm="HS256")

    return jsonify({
        "message": "Login successful!",
        "token": token,
        "name": user["name"]
    }), 200