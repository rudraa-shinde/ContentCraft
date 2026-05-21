import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("JWT_SECRET")
CORS(app, supports_credentials=True, origins="*")
from routes.auth import auth_bp
from routes.content import content_bp

app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(content_bp, url_prefix="/api/content")

# Frontend ka sahi path
FRONTEND = os.path.join(os.path.dirname(__file__), '..', 'frontend')

@app.route("/")
def home():
    return {"message": "ContentCraft API is running!"}

@app.route('/login')
def login_page():
    return send_from_directory(f'{FRONTEND}/pages', 'login.html')

@app.route('/register')
def register_page():
    return send_from_directory(f'{FRONTEND}/pages', 'register.html')

@app.route('/dashboard')
def dashboard_page():
    return send_from_directory(f'{FRONTEND}/pages', 'index.html')

@app.route('/history')
def history_page():
    return send_from_directory(f'{FRONTEND}/pages', 'history.html')

@app.route('/frontend/<path:filename>')
def frontend_files(filename):
    return send_from_directory(FRONTEND, filename)

@app.route('/css/<path:filename>')
def css_files(filename):
    return send_from_directory(f'{FRONTEND}/css', filename)

@app.route('/js/<path:filename>')
def js_files(filename):
    return send_from_directory(f'{FRONTEND}/js', filename)

if __name__ == "__main__":
    app.run(debug=True, port=5000)