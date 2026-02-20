# 🌾 कृषी सहाय्यक — Krishi Sahayak
### AI-Powered Smart Farming Assistant | FA-2 Project
**Streamlit + Google Gemini 2.5 Flash · Marathi · Hindi · English**

---

## 🔗 Live App

> **Deployed URL:** *(Add your Streamlit Cloud URL here after deployment)*

---

## 📌 Overview

**Krishi Sahayak** (meaning "Farming Helper") is an AI-powered agricultural assistant built for Maharashtra farmers. It supports three languages — Marathi, Hindi, and English — and uses Google Gemini 2.5 Flash to provide real-time, contextual farming advice including crop planning, pest control, soil health, weather interpretation, and sustainable farming.

This project is built as a **single-file Streamlit application** — all logic, UI, styles, translations, and AI integration live inside one file: `app.py`.

Originally developed as a **FA-2 Generative AI Course Project**, converted from a React/TypeScript prototype to a full Python Streamlit application.

---

## 📸 Screenshots

> **How to add your screenshots:**
> 1. Take screenshots of your running app
> 2. Save them in a `/screenshots` folder in your repo
> 3. Replace the placeholder paths below with your actual image filenames

### 🔐 Login Page
![Login Page](screenshots/login.png)
*Animated glassmorphism login screen with language selection*

### 🏠 Dashboard
![Dashboard](screenshots/dashboard.png)
*Main dashboard with weather widget, stats row, and feature cards*

### 💬 Chat Interface
![Chat](screenshots/chat.png)
*In-feature AI chat with quick prompts and image upload*

### ✅ Model Validation
![Validation](screenshots/validation.png)
*6-prompt validation tab with auto quality scoring*

### 📊 Feedback Checklist
![Checklist](screenshots/checklist.png)
*10-criteria feedback checklist with grade report and CSV export*

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔐 **Login Screen** | Name + mobile number login with animated glassmorphism UI |
| 🌍 **3 Languages** | Full UI + AI responses in Marathi, Hindi, and English |
| 🌡️ **Live Weather Widget** | Gemini-simulated weather for Pune with farming tips |
| 🌱 **Crop Advice Chat** | Region-specific sowing, spacing, and variety recommendations |
| 🐛 **Pest Control Chat** | Organic-first pest identification and management advice |
| ☁️ **Weather Chat** | Climate interpretation for irrigation and field decisions |
| 🧪 **Soil Health Chat** | Soil testing guidance and fertilizer recommendations |
| 🍃 **Eco Farming Chat** | Sustainable, organic, and environment-friendly practices |
| 📷 **Image Upload** | Send a crop photo for AI visual disease diagnosis |
| 💬 **Chat History** | Per-feature persistent chat with download as `.txt` |
| ✅ **Model Validation** | 6 pre-built test prompts (India / Canada / Ghana) with auto-scoring |
| 📊 **Feedback Checklist** | 10-criteria quality evaluation with CSV export and grade report |
| 💡 **Did You Know** | Rotating farming facts with next button |
| 📅 **Season Tracker** | Visual Kharif/Rabi calendar highlighting the current month |

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Frontend | Streamlit (Python) |
| AI Model | Google Gemini 2.5 Flash (`gemini-2.5-flash`) |
| AI SDK | `google-genai` >= 1.0.0 |
| Image Processing | Pillow (PIL) |
| Data & Export | Pandas |
| Language | Python 3.10+ |
| Deployment | Streamlit Cloud + GitHub |

---

## 📁 Project Structure

```
krishi-sahayak/
├── app.py              # Entire application — UI, logic, styles, AI, translations
├── requirements.txt    # Python dependencies
├── README.md           # This file
├── screenshots/        # Add your app screenshots here
└── .streamlit/
    └── secrets.toml    # API key (local only — DO NOT commit)
```

> 💡 **Single-file design:** Everything — CSS injection, language strings, session state, Gemini API calls, chat rendering, validation, and checklist — is written inside `app.py`. This makes it easy to share, review, and deploy with zero import errors.

---

## 📦 Local Setup

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/krishi-sahayak.git
cd krishi-sahayak
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

> ⚠️ **Important:** This project uses the **`google-genai`** package (new SDK).  
> Do **not** install `google-generativeai` — it is a different, older package and will cause import errors.

### 3. Add your Gemini API Key

**Option A — Sidebar (easiest for local dev):**  
Paste your key into the API Key field in the app sidebar. No file setup needed.

**Option B — secrets.toml (recommended):**
```bash
mkdir -p .streamlit
```
Create `.streamlit/secrets.toml`:
```toml
GEMINI_API_KEY = "your_gemini_api_key_here"
```

### 4. Run the app
```bash
streamlit run app.py
```
Open → [http://localhost:8501](http://localhost:8501)

---

## ☁️ Deploy to Streamlit Cloud

### Step 1 — Push to GitHub
```bash
git init
git add app.py requirements.txt README.md
git commit -m "🌾 Krishi Sahayak — FA-2 Smart Farming Assistant"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/krishi-sahayak.git
git push -u origin main
```

> ⚠️ Never push your API key. Add secrets to `.gitignore`:
> ```bash
> echo ".streamlit/secrets.toml" >> .gitignore
> ```

### Step 2 — Deploy on Streamlit Cloud
1. Go to [streamlit.io/cloud](https://streamlit.io/cloud) → sign in with GitHub
2. Click **"New app"**
3. Select your repository → set **Main file path** to `app.py`
4. Click **"Deploy!"**

### Step 3 — Add the API Key secret
1. In your deployed app → **Settings → Secrets**
2. Paste:
```toml
GEMINI_API_KEY = "your_gemini_api_key_here"
```
3. Save → the app will automatically reload ✅

---

## 🔑 Getting a Free Gemini API Key

1. Go to [aistudio.google.com](https://aistudio.google.com)
2. Click **"Get API Key"** → create or select a project
3. Copy the key (starts with `AIza...`)

> ### ⚠️ API Rate Limit Notice
>
> This app uses the **Google Gemini API Free Tier**, which has the following limits:
>
> | Limit | Free Tier |
> |---|---|
> | Requests per minute (RPM) | 15 |
> | Tokens per minute (TPM) | 1,000,000 |
> | Requests per day (RPD) | 1,500 |
>
> **What this means for users:**
> - If you send messages rapidly, you may see a `429 Resource Exhausted` error — wait 10–15 seconds and try again.
> - If your key stops working with an `API key expired` error — regenerate it at [aistudio.google.com](https://aistudio.google.com).
> - Heavy usage across chat + weather + validation can exhaust your daily quota faster.
>
> **Tips to avoid hitting limits:**
> - Wait a moment between messages instead of sending rapidly.
> - For production or high-traffic use, upgrade to a paid plan at [ai.google.dev/pricing](https://ai.google.dev/pricing).

---

## 🌍 Language Support

| Language | Code | UI | AI Responses |
|---|---|---|---|
| मराठी (Marathi) | `mr` | ✅ Full | ✅ Full |
| हिंदी (Hindi) | `hi` | ✅ Full | ✅ Full |
| English | `en` | ✅ Full | ✅ Full |

Language can be switched from the sidebar or the login page at any time. Switching language clears the weather cache and re-fetches in the new language.

---

## 🧪 Model Validation — 6 Test Prompts

| # | Flag | Region | Season | Crop |
|---|---|---|---|---|
| 1 | 🇮🇳 | Rajasthan, India | August | Millet |
| 2 | 🇮🇳 | Punjab, India | November | Wheat |
| 3 | 🇨🇦 | Ontario, Canada | May | Canola |
| 4 | 🇨🇦 | Saskatchewan, Canada | July | Barley |
| 5 | 🇬🇭 | Northern Ghana | June | Maize |
| 6 | 🇬🇭 | Ashanti, Ghana | March | Cocoa |

**Auto-scoring checks:** Crop-specific content · Has reasoning ("Why:") · Numbered list · Word count (60–500 words)

---

## 📊 Feedback Checklist — 10 Criteria

| # | Criterion |
|---|---|
| 1 | Is the advice specific to the input region/location? |
| 2 | Does the output provide valid and logical reasoning? |
| 3 | Is the language simple enough for a layperson? |
| 4 | Are outputs free from being too generic or technical? |
| 5 | Does the model avoid misleading or unsafe advice? |
| 6 | Are numbered recommendations clearly listed? |
| 7 | Is each recommendation followed by a 'Why' justification? |
| 8 | Is the response relevant to the current season/crop stage? |
| 9 | Would a farmer be able to act on this advice immediately? |
| 10 | Is the response free of hallucinated or unverifiable facts? |

Scoring: `(Yes × 1 + Partial × 0.5) / 10 × 100%`  
Grades: **A 🏆** ≥ 80% · **B ✅** ≥ 60% · **C ⚠️** < 60%

---

## 📚 References

- [Google AI Studio — Gemini API](https://aistudio.google.com)
- [google-genai Python SDK](https://pypi.org/project/google-genai/)
- [Streamlit Documentation](https://docs.streamlit.io)
- [ICAR — Indian Council of Agricultural Research](https://www.icar.org.in)
- [Maharashtra Agriculture Department](https://krishi.maharashtra.gov.in)
- [FAO Crop Calendar](https://www.fao.org/agriculture/seed/cropcalendar/welcome.do)

---

## 👥 Project Info

> **FA-2 Project** · Generative AI Course, Year 1  
> Single-file Streamlit app — all code in `app.py`  
> Built with Streamlit + Google Gemini 2.5 Flash  
> Supports Marathi · Hindi · English  
> Converted from React (Vite + TypeScript) → Python (Streamlit)
