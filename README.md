# ContentCraft #

AI-powered social media content generation platform.

 Overview-
ContentCraft helps content creators, marketers, and students generate 
high-quality social media content instantly using AI.

 Features-
- User Registration & Login (JWT Authentication)
- AI Content Generation using Groq API (LLaMA 3.3-70b)
- Multiple Content Types — Instagram Caption, Tweet, Blog Post
- Tone Selection — Professional, Casual, Funny, Inspirational
- Language Support — English, Hindi, Hinglish
- Platform Optimization — Instagram, Twitter, LinkedIn, YouTube
- Content Scoring & Analysis
- Generation History

 Tech Stack-
| Layer | Technology |
|-------|-----------|
| Backend | Python, Flask |
| Database | MongoDB Atlas |
| Authentication | JWT |
| AI Model | Groq API (LLaMA 3.3) |
| Frontend | HTML, CSS, JavaScript |

How It Works-
1. User registers and logs in
2. Selects content type, tone, language and platform
3. Enters topic or idea
4. AI generates optimized content
5. User can copy, score or view history

 Installation-
```bash
git clone https://github.com/rudraa-shinde/ContentCraft.git
cd ContentCraft/backend
pip install -r requirements.txt
python app.py