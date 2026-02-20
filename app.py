import streamlit as st
from google import genai
from google.genai import types
import base64
import json
import datetime
import random
from PIL import Image
import io

# ===================================================═══════════
#  PAGE CONFIG
# ===================================================═══════════
st.set_page_config(
    page_title="कृषी सहाय्यक – Krishi Sahayak",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ===================================================═══════════
#  LANGUAGE STRINGS
# ===================================================═══════════
UI = {
    "en": {
        "app_name": "Krishi Sahayak", "tagline": "Smart Farming Assistant",
        "greeting": "Hello", "hero_sub": "Today is a great day to tend your cotton and soybean crops.",
        "location": "Maharashtra, India",
        "login_welcome": "Welcome to Krishi Sahayak", "login_sub": "Your AI-powered digital farming partner",
        "name_label": "Your Name", "phone_label": "Mobile Number",
        "login_btn": "Enter Farm →", "name_ph": "Enter your name", "phone_ph": "Enter 10-digit number",
        "daily_tip": "🌿 Today's Tip", "rain": "Rain Chance",
        "tip": "Using neem oil can naturally prevent pest attacks on soybean crops. It is a cost-effective alternative to chemical pesticides.",
        "features": ["🌱 Crop Advice", "🐛 Pest Control", "☁️ Weather", "🧪 Soil Health", "🍃 Eco Farming"],
        "feat_ids": ["crop", "pest", "weather", "soil", "eco"],
        "chat_ph": "Ask anything about farming...", "send": "Send ➤",
        "thinking": "Assistant is thinking...", "greeting_chat": "Hello! I am Krishi Sahayak. How can I help you today?",
        "upload_img": "📷 Upload Crop Photo", "img_caption": "Photo attached",
        "validation_title": "Model Validation", "checklist_title": "Feedback Checklist",
        "run_test": "▶ Run Test", "logout": "← Change User",
        "api_missing": "⚠️ Please enter your Gemini API Key in the sidebar.",
        "api_label": "Gemini API Key", "api_help": "Get a free key at aistudio.google.com",
        "lang_label": "Language", "error_msg": "Connection trouble. Please check your API key.",
        "back": "← Back", "clear_chat": "🗑 Clear", "download_chat": "⬇ Download",
        "quick_prompts": ["What to grow this season?", "How to remove pests naturally?", "Best fertilizer for my crop?", "When to irrigate?", "Improve soil quality"],
        "stats": ["Crops Covered", "States Supported", "Languages", "AI Model"],
        "stat_vals": ["50+", "5+", "3", "Gemini"],
        "did_you_know": [
            "💡 Crop rotation can improve soil health by up to 30%.",
            "💡 Neem-based pesticides are 95% effective against common crop pests.",
            "💡 Drip irrigation saves 40-60% more water than flood irrigation.",
            "💡 Intercropping soybean with cotton improves nitrogen in the soil.",
            "💡 Early morning watering reduces fungal disease risk significantly.",
        ],
        "season_label": "Season Tracker", "humidity": "Humidity",
        "open_chat": "Open Chat →",
    },
    "hi": {
        "app_name": "कृषि सहायक", "tagline": "स्मार्ट खेती सहायक",
        "greeting": "नमस्ते", "hero_sub": "आज कपास और सोयाबीन की फसल की देखभाल के लिए अच्छा दिन है।",
        "location": "महाराष्ट्र, भारत",
        "login_welcome": "कृषि सहायक में आपका स्वागत है", "login_sub": "बेहतर खेती के लिए आपका AI डिजिटल साथी",
        "name_label": "आपका नाम", "phone_label": "मोबाइल नंबर",
        "login_btn": "खेत में प्रवेश करें →", "name_ph": "अपना नाम दर्ज करें", "phone_ph": "10-अंकीय नंबर",
        "daily_tip": "🌿 आज की टिप", "rain": "बारिश की संभावना",
        "tip": "नीम के तेल का उपयोग सोयाबीन पर कीटों के प्रकोप को स्वाभाविक रूप से रोकता है।",
        "features": ["🌱 फसल सलाह", "🐛 कीट प्रबंधन", "☁️ मौसम", "🧪 मिट्टी स्वास्थ्य", "🍃 जैविक खेती"],
        "feat_ids": ["crop", "pest", "weather", "soil", "eco"],
        "chat_ph": "खेती के बारे में कुछ भी पूछें...", "send": "भेजें ➤",
        "thinking": "सहायक सोच रहा है...", "greeting_chat": "नमस्ते! मैं कृषि सहायक हूँ। आज क्या सहायता करूँ?",
        "upload_img": "📷 फसल फोटो अपलोड करें", "img_caption": "फोटो संलग्न",
        "validation_title": "मॉडल सत्यापन", "checklist_title": "फीडबैक चेकलिस्ट",
        "run_test": "▶ परीक्षण चलाएं", "logout": "← बदलें",
        "api_missing": "⚠️ साइडबार में Gemini API Key डालें।",
        "api_label": "Gemini API Key", "api_help": "aistudio.google.com पर key पाएं",
        "lang_label": "भाषा", "error_msg": "कनेक्शन में समस्या। API key जाँचें।",
        "back": "← वापस", "clear_chat": "🗑 साफ़", "download_chat": "⬇ डाउनलोड",
        "quick_prompts": ["इस मौसम में क्या उगाएं?", "कीट प्राकृतिक रूप से कैसे हटाएं?", "सबसे अच्छा उर्वरक?", "सिंचाई कब करें?", "मिट्टी की गुणवत्ता सुधारें"],
        "stats": ["फसलें", "राज्य", "भाषाएं", "AI मॉडल"],
        "stat_vals": ["50+", "5+", "3", "Gemini"],
        "did_you_know": [
            "💡 फसल चक्र से मिट्टी की उर्वरता 30% तक बढ़ सकती है।",
            "💡 नीम-आधारित कीटनाशक 95% प्रभावी हैं।",
            "💡 ड्रिप सिंचाई 40-60% पानी बचाती है।",
            "💡 सोयाबीन और कपास की अंतर-फसल मिट्टी में नाइट्रोजन बढ़ाती है।",
            "💡 सुबह सिंचाई से कवक रोगों का खतरा कम होता है।",
        ],
        "season_label": "मौसम ट्रैकर", "humidity": "आर्द्रता",
        "open_chat": "चैट खोलें →",
    },
    "mr": {
        "app_name": "कृषी सहाय्यक", "tagline": "स्मार्ट फार्मिंग असिस्टंट",
        "greeting": "नमस्कार", "hero_sub": "आज कापूस आणि सोयाबीन पिकाची काळजी घेण्यासाठी उत्तम दिवस आहे.",
        "location": "महाराष्ट्र, भारत",
        "login_welcome": "कृषी सहाय्यकमध्ये स्वागत आहे", "login_sub": "स्मार्ट शेतीसाठी तुमचा AI डिजिटल जोडीदार",
        "name_label": "तुमचे नाव", "phone_label": "मोबाईल नंबर",
        "login_btn": "प्रवेश करा →", "name_ph": "नाव टाका", "phone_ph": "१० अंकी नंबर",
        "daily_tip": "🌿 आजची टीप", "rain": "पावसाची शक्यता",
        "tip": "कडुलिंबाच्या तेलाचा वापर केल्यास सोयाबीनवरील किडींचा प्रादुर्भाव नैसर्गिकरित्या रोखता येतो.",
        "features": ["🌱 पीक सल्ला", "🐛 कीड नियंत्रण", "☁️ हवामान", "🧪 माती आरोग्य", "🍃 नैसर्गिक शेती"],
        "feat_ids": ["crop", "pest", "weather", "soil", "eco"],
        "chat_ph": "शेतीबद्दल काहीही विचारा...", "send": "पाठवा ➤",
        "thinking": "सहाय्यक विचार करत आहे...", "greeting_chat": "नमस्कार! मी कृषी सहाय्यक आहे. आज कशी मदत करू?",
        "upload_img": "📷 पिकाचा फोटो अपलोड करा", "img_caption": "फोटो जोडला",
        "validation_title": "मॉडेल व्हॅलिडेशन", "checklist_title": "फीडबॅक चेकलिस्ट",
        "run_test": "▶ चाचणी चालवा", "logout": "← बदला",
        "api_missing": "⚠️ साइडबारमध्ये Gemini API Key टाका.",
        "api_label": "Gemini API Key", "api_help": "aistudio.google.com वर key मिळवा",
        "lang_label": "भाषा", "error_msg": "कनेक्शनमध्ये अडथळा. API key तपासा.",
        "back": "← परत", "clear_chat": "🗑 साफ", "download_chat": "⬇ डाउनलोड",
        "quick_prompts": ["या हंगामात काय पिकवावे?", "किडी नैसर्गिकरित्या कसे काढावे?", "सर्वोत्तम खत कोणते?", "सिंचन कधी करावे?", "मातीची गुणवत्ता सुधारा"],
        "stats": ["पिके", "राज्ये", "भाषा", "AI मॉडेल"],
        "stat_vals": ["50+", "5+", "3", "Gemini"],
        "did_you_know": [
            "💡 पीक फेरपालटामुळे मातीची सुपीकता ३०% वाढू शकते.",
            "💡 कडुलिंब-आधारित कीटकनाशके ९५% प्रभावी आहेत.",
            "💡 ठिबक सिंचनाने ४०-६०% पाणी वाचते.",
            "💡 सोयाबीन-कापूस आंतरपिकामुळे मातीत नायट्रोजन वाढतो.",
            "💡 सकाळी पाणी दिल्यास बुरशीजन्य रोगांचा धोका कमी होतो.",
        ],
        "season_label": "हंगाम ट्रॅकर", "humidity": "आर्द्रता",
        "open_chat": "चॅट उघडा →",
    },
}

SYSTEM_PROMPTS = {
    "en": "You are Krishi Sahayak, a professional agricultural assistant for Maharashtra farmers. ALWAYS respond in English. Provide clear, step-by-step farming advice using bullet points. Suggest organic solutions first for pest queries. Be concise and practical.",
    "hi": "आप कृषि सहायक हैं, महाराष्ट्र के किसानों के लिए। हमेशा हिंदी में उत्तर दें। बुलेट पॉइंट के साथ स्पष्ट खेती की सलाह दें। कीटों के लिए जैविक समाधान पहले सुझाएं।",
    "mr": "तुम्ही कृषी सहाय्यक आहात, महाराष्ट्रातील शेतकऱ्यांसाठी. नेहमी मराठीतच उत्तरे द्या. बुलेट पॉइंट्स वापरून स्पष्ट सल्ला द्या. कीड नियंत्रणासाठी सेंद्रिय उपाय प्रथम सुचवा.",
}

FEATURE_PROMPTS = {
    "crop":    {"en":"crop recommendation and planting advice","hi":"फसल सिफारिश और रोपण सलाह","mr":"पीक शिफारस आणि लागवड सल्ला"},
    "pest":    {"en":"pest identification and management","hi":"कीट पहचान और प्रबंधन","mr":"कीड ओळख आणि व्यवस्थापन"},
    "weather": {"en":"weather and climate farming advice","hi":"मौसम और जलवायु खेती सलाह","mr":"हवामान आणि शेती सल्ला"},
    "soil":    {"en":"soil health and fertilizer guidance","hi":"मिट्टी स्वास्थ्य और उर्वरक","mr":"माती आरोग्य आणि खत मार्गदर्शन"},
    "eco":     {"en":"sustainable and organic farming methods","hi":"टिकाऊ और जैविक खेती","mr":"शाश्वत आणि सेंद्रिय शेती"},
}

FEAT_THEME = {
    "crop":    ("#059669", "#10b981", "#d1fae5", "#ecfdf5", "🌱"),
    "pest":    ("#dc2626", "#f87171", "#fee2e2", "#fff5f5", "🐛"),
    "weather": ("#2563eb", "#60a5fa", "#dbeafe", "#eff6ff", "☁️"),
    "soil":    ("#d97706", "#fbbf24", "#fef3c7", "#fffbeb", "🧪"),
    "eco":     ("#65a30d", "#a3e635", "#d9f99d", "#f7ffe4", "🍃"),
}

# ===================================================═══════════
#  CSS
# ===================================================═══════════
def inject_css():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@600;700;900&family=Noto+Sans+Devanagari:wght@400;600;700&family=Inter:wght@400;500;600;700&display=swap');

html, body { font-family:'Inter','Noto Sans Devanagari',sans-serif; color:#111827; }
[data-testid="stAppViewContainer"] { background:#f5f7ff; min-height:100vh; color:#111827; }
[data-testid="stMainBlockContainer"] { color:#111827; }
[data-testid="stHeader"], #MainMenu, footer, [data-testid="stDecoration"] { display:none !important; }
.block-container { padding:1.5rem 2rem 5rem !important; max-width:1100px !important; }

[data-testid="stAppViewContainer"]::before {
    content:''; position:fixed; top:0; left:0; width:100%; height:100%;
    background:
        radial-gradient(circle at 10% 20%, rgba(99,102,241,0.12) 0%, transparent 40%),
        radial-gradient(circle at 85% 15%, rgba(16,185,129,0.1) 0%, transparent 45%),
        radial-gradient(circle at 50% 80%, rgba(245,158,11,0.08) 0%, transparent 50%),
        radial-gradient(circle at 80% 90%, rgba(239,68,68,0.07) 0%, transparent 35%),
        radial-gradient(circle at 20% 60%, rgba(168,85,247,0.09) 0%, transparent 42%);
    pointer-events:none; z-index:0;
    animation: particleFloat 25s ease-in-out infinite;
}
@keyframes particleFloat {
    0%, 100% { transform: translate(0, 0) scale(1); opacity: 1; }
    25% { transform: translate(30px, -40px) scale(1.05); opacity: 0.85; }
    50% { transform: translate(-25px, 30px) scale(0.95); opacity: 0.9; }
    75% { transform: translate(40px, 20px) scale(1.03); opacity: 0.8; }
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1e1b4b 0%, #312e81 50%, #1e3a5f 100%) !important;
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div:not(input):not(select),
[data-testid="stSidebar"] h1,[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,[data-testid="stSidebar"] h4 { color:#e0e7ff !important; }
[data-testid="stSidebar"] a { color:#a5b4fc !important; }
[data-testid="stSidebar"] input {
    background:#3730a3 !important; border:1px solid #6366f1 !important;
    color:#ffffff !important; border-radius:10px !important;
}
[data-testid="stSidebar"] input::placeholder { color:#a5b4fc !important; }
[data-testid="stSidebar"] label { color:#a5b4fc !important; font-weight:700 !important; font-size:0.8rem !important; letter-spacing:0.05em !important; text-transform:uppercase !important; }
[data-testid="stSidebar"] .stRadio > div { gap:6px !important; }
[data-testid="stSidebar"] .stRadio label { background:rgba(99,102,241,0.15) !important; border-radius:10px !important; padding:6px 12px !important; transition:all 0.2s !important; color:#e0e7ff !important; }
[data-testid="stSidebar"] .stRadio label:hover { background:rgba(99,102,241,0.35) !important; }
[data-testid="stSidebar"] .stButton button { background:rgba(99,102,241,0.25) !important; color:#e0e7ff !important; border:1px solid rgba(165,180,252,0.3) !important; }
[data-testid="stSidebar"] .stButton button:hover { background:rgba(99,102,241,0.45) !important; color:#ffffff !important; }

.hero {
    background: linear-gradient(135deg, #1e1b4b 0%, #3730a3 30%, #1d4ed8 60%, #0369a1 100%);
    border-radius:28px; padding:2.5rem 2.8rem; color:#ffffff !important;
    margin-bottom:1.8rem; position:relative; overflow:hidden;
    box-shadow: 0 20px 60px rgba(30,27,75,0.35), 0 0 0 1px rgba(255,255,255,0.08);
    animation: heroGlow 4s ease-in-out infinite alternate;
}
.hero * { color:#ffffff !important; }
@keyframes heroGlow {
    from { box-shadow: 0 20px 60px rgba(30,27,75,0.35), 0 0 40px rgba(99,102,241,0.15), 0 0 0 1px rgba(255,255,255,0.08); }
    to { box-shadow: 0 20px 60px rgba(30,27,75,0.35), 0 0 80px rgba(99,102,241,0.3), 0 0 0 1px rgba(255,255,255,0.12); }
}
.hero::before {
    content:''; position:absolute; top:-60%; right:-10%;
    width:500px; height:500px;
    background: radial-gradient(circle, rgba(255,255,255,0.15) 0%, rgba(255,255,255,0.05) 30%, transparent 65%);
    border-radius:50%; pointer-events:none;
    animation: orbFloat 8s ease-in-out infinite;
}
@keyframes orbFloat {
    0%, 100% { transform: translate(0, 0) scale(1); opacity: 0.8; }
    50% { transform: translate(-30px, 20px) scale(1.1); opacity: 1; }
}
.hero::after {
    content:'🌾'; position:absolute; bottom:-10px; right:2.5rem;
    font-size:7rem; opacity:0.12; line-height:1;
    filter: drop-shadow(0 0 20px rgba(255,255,255,0.3));
    animation: float 6s ease-in-out infinite, wheatGlow 3s ease-in-out infinite;
    pointer-events:none;
}
@keyframes float { 0%,100%{transform:translateY(0) rotate(-5deg);} 50%{transform:translateY(-12px) rotate(5deg);} }
@keyframes wheatGlow {
    0%, 100% { opacity: 0.12; filter: drop-shadow(0 0 20px rgba(255,255,255,0.3)); }
    50% { opacity: 0.18; filter: drop-shadow(0 0 30px rgba(255,255,255,0.5)); }
}
.hero-badge {
    display:inline-flex; align-items:center; gap:6px; color:#ffffff !important;
    background:rgba(255,255,255,0.15); border:1px solid rgba(255,255,255,0.25);
    border-radius:20px; padding:4px 14px; margin-bottom:0.8rem;
    font-size:0.72rem; font-weight:700; letter-spacing:0.1em; text-transform:uppercase;
    backdrop-filter:blur(10px);
}
.hero-name {
    font-family:'Poppins',sans-serif; font-size:2.6rem; font-weight:900;
    line-height:1.1; margin:0; color:#ffffff !important;
    text-shadow: 0 2px 20px rgba(0,0,0,0.3), 0 0 30px rgba(255,255,255,0.2);
}
.hero-sub { font-size:1rem; color:rgba(255,255,255,0.85) !important; margin-top:0.5rem; max-width:480px; line-height:1.6; }
.weather-pill {
    display:inline-flex; align-items:center; gap:16px;
    background:rgba(255,255,255,0.12); backdrop-filter:blur(20px);
    border:1px solid rgba(255,255,255,0.2); border-radius:18px;
    padding:0.9rem 1.4rem; margin-top:1.2rem; color:#ffffff !important;
}
.w-temp { font-family:'Poppins',sans-serif; font-size:2.6rem; font-weight:900; line-height:1; color:#ffffff !important; }
.w-info { font-size:0.82rem; line-height:1.7; color:rgba(255,255,255,0.9) !important; }
.w-bar-wrap { width:90px; height:6px; background:rgba(255,255,255,0.2); border-radius:3px; overflow:hidden; margin-top:3px; }
.w-bar { height:100%; border-radius:3px; }

.stats-row { display:grid; grid-template-columns:repeat(4,1fr); gap:12px; margin:1.4rem 0; }
.stat-card {
    border-radius:18px; padding:1.1rem 1rem; text-align:center;
    border:1.5px solid rgba(255,255,255,0.7); backdrop-filter:blur(10px);
    box-shadow: 0 4px 16px rgba(0,0,0,0.07);
    transition:transform 0.2s, box-shadow 0.2s; 
    animation: fadeUp 0.5s ease both;
    position: relative; overflow: hidden;
}
.stat-card:hover { transform:translateY(-3px); box-shadow: 0 10px 28px rgba(0,0,0,0.12); }
@keyframes fadeUp { from{opacity:0;transform:translateY(12px);} to{opacity:1;transform:translateY(0);} }
.stat-val { font-family:'Poppins',sans-serif; font-size:1.8rem; font-weight:900; line-height:1; }
.stat-lbl { font-size:0.72rem; font-weight:700; letter-spacing:0.06em; text-transform:uppercase; margin-top:4px; }

.feat-card {
    border-radius:22px; padding:1.4rem 0.8rem; text-align:center; cursor:pointer;
    border:2px solid transparent; 
    transition:all 0.3s cubic-bezier(0.34,1.4,0.64,1);
    box-shadow: 0 4px 16px rgba(0,0,0,0.07); 
    position:relative;
    animation: fadeUp 0.4s ease both;
}
.feat-card:hover { transform:translateY(-6px) scale(1.03); box-shadow: 0 16px 40px rgba(0,0,0,0.18); filter:brightness(1.04); }
.feat-icon-wrap {
    width:62px; height:62px; border-radius:18px; margin:0 auto 0.75rem;
    display:flex; align-items:center; justify-content:center;
    font-size:1.75rem; box-shadow: 0 6px 18px rgba(0,0,0,0.2);
    transition:transform 0.3s cubic-bezier(0.34,1.6,0.64,1); position:relative; z-index:1;
}
.feat-card:hover .feat-icon-wrap { transform:scale(1.15) rotate(-5deg); }
.feat-label { font-size:0.82rem; font-weight:700; position:relative; z-index:1; }

.dyk-card {
    border-radius:20px; padding:1.3rem 1.6rem;
    display:flex; align-items:center; gap:1.2rem;
    box-shadow: 0 4px 20px rgba(99,102,241,0.12);
    border:1.5px solid rgba(99,102,241,0.2);
    background:linear-gradient(135deg,#f5f3ff,#ede9fe);
    margin:0.5rem 0 1.2rem; animation:fadeUp 0.6s ease; transition:all 0.3s;
}
.dyk-card:hover { transform:scale(1.01); box-shadow: 0 8px 28px rgba(99,102,241,0.22); }
.dyk-icon { font-size:2rem; flex-shrink:0; }
.dyk-text { font-size:0.95rem; color:#3b0764 !important; font-weight:600; line-height:1.6; }

.tip-card {
    border-radius:20px; padding:1.5rem 1.8rem;
    box-shadow: 0 4px 20px rgba(16,185,129,0.1);
    border-left:5px solid #10b981; 
    background:linear-gradient(135deg,#ecfdf5,#d1fae5); 
    margin:0.5rem 0;
}
.tip-title { font-weight:800; color:#065f46 !important; font-size:1rem; margin-bottom:0.5rem; }
.tip-text { color:#065f46 !important; font-size:0.95rem; line-height:1.7; font-style:italic; }

.season-row { display:flex; gap:8px; margin:0.8rem 0 1.4rem; flex-wrap:wrap; }
.season-pill { padding:6px 16px; border-radius:20px; font-size:0.78rem; font-weight:700; border:2px solid transparent; transition:all 0.2s; cursor:default; }
.season-pill.active  { color:#ffffff !important; }
.season-pill.inactive{ background:white; color:#4b5563 !important; border-color:#e5e7eb; }

.chat-wrap { border-radius:0 0 20px 20px; border:2px solid; border-top:none; background:#ffffff; }
.chat-hdr  { border-radius:20px 20px 0 0; padding:1rem 1.4rem; display:flex; align-items:center; gap:12px; border:2px solid; border-bottom:none; }
.chat-hdr-icon { width:40px; height:40px; border-radius:12px; color:#ffffff !important; font-size:1.2rem; display:flex; align-items:center; justify-content:center; box-shadow:0 4px 12px rgba(0,0,0,0.2); }
.chat-hdr-name { font-weight:800; font-size:1rem; }
.chat-hdr-sub  { font-size:0.7rem; font-weight:600; text-transform:uppercase; letter-spacing:0.07em; color:#6b7280 !important; }
.msg-user-wrap { display:flex; justify-content:flex-end; margin:8px 0; animation:msgSlide 0.3s ease; }
.msg-bot-wrap  { display:flex; justify-content:flex-start; margin:8px 0; animation:msgSlide 0.3s ease; }
@keyframes msgSlide { from{opacity:0;transform:translateY(8px);} to{opacity:1;transform:translateY(0);} }
.msg-user { color:#ffffff !important; border-radius:18px 18px 4px 18px; padding:0.75rem 1.1rem; max-width:78%; font-size:0.9rem; line-height:1.6; box-shadow:0 4px 16px rgba(0,0,0,0.25); }
.msg-bot { background:#ffffff; color:#111827 !important; border-radius:18px 18px 18px 4px; padding:0.75rem 1.1rem; max-width:78%; font-size:0.9rem; line-height:1.6; box-shadow:0 4px 16px rgba(0,0,0,0.07); white-space:pre-wrap; }
.msg-time { font-size:0.65rem; color:#9ca3af !important; font-weight:700; margin-top:3px; }
.msg-avatar { width:32px; height:32px; border-radius:10px; flex-shrink:0; display:flex; align-items:center; justify-content:center; font-size:0.95rem; box-shadow:0 2px 8px rgba(0,0,0,0.15); background:linear-gradient(135deg,#6366f1,#8b5cf6); color:#ffffff !important; }
.typing-dot { display:inline-block; width:7px; height:7px; border-radius:50%; background:#94a3b8; margin:0 2px; animation:typingPulse 1.2s ease-in-out infinite; }
.typing-dot:nth-child(2){animation-delay:0.2s;} .typing-dot:nth-child(3){animation-delay:0.4s;}
@keyframes typingPulse { 0%,80%,100%{transform:scale(0.8);opacity:0.5;} 40%{transform:scale(1.2);opacity:1;} }

.prog-wrap { background:#e5e7eb; border-radius:6px; overflow:hidden; height:8px; margin:4px 0; }
.prog-bar  { height:100%; border-radius:6px; transition:width 1.2s cubic-bezier(0.4,0,0.2,1); }

.val-output {
    background:linear-gradient(135deg,#f8faff,#eff6ff); border-left:5px solid #3b82f6;
    border-radius:0 16px 16px 0; padding:1.2rem 1.4rem;
    white-space:pre-wrap; font-size:0.9rem; line-height:1.75; color:#1e3a8a !important;
    box-shadow:0 4px 16px rgba(59,130,246,0.1);
}

.stTextInput input, .stTextArea textarea {
    border-radius:14px !important; border:2px solid #e5e7eb !important;
    padding:0.7rem 1rem !important; background:#f9fafb !important;
    font-family:'Inter','Noto Sans Devanagari',sans-serif !important;
    font-size:0.95rem !important; color:#111827 !important; transition:all 0.2s !important;
}
.stTextInput input::placeholder, .stTextArea textarea::placeholder { color:#9ca3af !important; }
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color:#6366f1 !important; background:#ffffff !important;
    box-shadow:0 0 0 3px rgba(99,102,241,0.15) !important; color:#111827 !important;
}
.stTextInput label, .stTextArea label, .stSelectbox label, .stFileUploader label { color:#374151 !important; font-weight:600 !important; }
.stButton button {
    border-radius:12px !important; font-weight:700 !important;
    font-family:'Inter','Noto Sans Devanagari',sans-serif !important;
    transition:all 0.2s ease !important; color:#111827 !important;
    background:#f3f4f6 !important; border:2px solid #e5e7eb !important;
}
.stButton button:hover { transform:translateY(-2px) !important; background:#e5e7eb !important; }
.stButton button[kind="primary"] {
    background:linear-gradient(135deg,#6366f1,#8b5cf6) !important;
    color:#ffffff !important; border:none !important;
    box-shadow:0 4px 14px rgba(99,102,241,0.4) !important;
}
.stSelectbox > div > div { border-radius:12px !important; border:2px solid #e5e7eb !important; background:#f9fafb !important; color:#111827 !important; }
.stSelectbox [data-baseweb="select"] span { color:#111827 !important; }
[data-baseweb="popover"] li { color:#111827 !important; background:#ffffff !important; }
[data-baseweb="popover"] li:hover { background:#f0f4ff !important; color:#4f46e5 !important; }
.stFileUploader > div { border:2px dashed #c7d2fe !important; border-radius:16px !important; background:#f5f3ff !important; }
.stFileUploader label { color:#374151 !important; }
.stFileUploader span { color:#374151 !important; }
.stTabs [data-baseweb="tab-list"] { background:#ffffff; border-radius:14px; padding:4px; gap:4px; border:2px solid #e5e7eb; box-shadow:0 2px 8px rgba(0,0,0,0.04); }
.stTabs [data-baseweb="tab"] { border-radius:10px !important; font-weight:700 !important; padding:0.5rem 1rem !important; color:#374151 !important; }
.stTabs [aria-selected="true"] { background:linear-gradient(135deg,#6366f1,#8b5cf6) !important; color:#ffffff !important; }
.stTabs [aria-selected="false"] { color:#374151 !important; }
.stMetric { background:#ffffff; border-radius:16px; padding:1rem; border:2px solid #f3f4f6; box-shadow:0 2px 10px rgba(0,0,0,0.04); }
.stMetric label { color:#6b7280 !important; font-size:0.75rem !important; text-transform:uppercase; letter-spacing:0.06em; }
.stMetric [data-testid="stMetricValue"] { font-family:'Poppins',sans-serif; font-weight:900; font-size:1.7rem !important; color:#111827 !important; }
div[data-testid="stExpander"] { border:2px solid #e5e7eb !important; border-radius:16px !important; }
div[data-testid="stExpander"] summary { color:#374151 !important; font-weight:600 !important; }
.stAlert p { color:#111827 !important; }
.stMarkdown p, .stMarkdown li, .stMarkdown span { color:#111827 !important; }
</style>
""", unsafe_allow_html=True)

# ===================================================═══════════
#  SESSION STATE
# ===================================================═══════════
def init_state():
    defaults = {
        "logged_in": False, "user_name": "", "phone": "",
        "lang": "mr", "active_feature": None, "weather_data": None,
        "dyk_idx": 0,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v
    for feat in ["crop","pest","weather","soil","eco"]:
        if f"chat_{feat}" not in st.session_state:
            st.session_state[f"chat_{feat}"] = []

init_state()

# ===================================================═══════════
#  HELPERS
# ===================================================═══════════
def s(key): return UI[st.session_state.lang].get(key, key)

def get_api_key():
    try:   return st.secrets["GEMINI_API_KEY"]
    except: return st.session_state.get("_api_key","")

def make_model(api_key, temp=0.7):
    client = genai.Client(api_key=api_key)
    return client

def get_weather(api_key, lang):
    ln = {"en":"English","hi":"Hindi","mr":"Marathi"}[lang]
    try:
        client = genai.Client(api_key=api_key)
        prompt = (
            f"Simulate realistic current weather for Pune Maharashtra India. "
            f"Respond ONLY valid JSON with keys: temp (number), condition (string 2-3 words in {ln}), "
            f"humidity (number 0-100), rainfall_prob (number 0-100), tip (string one sentence farming advice in {ln}). No markdown."
        )
        r = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                max_output_tokens=200,
                temperature=0.3
            )
        )
        return json.loads(r.text.strip())
    except:
        return {"temp":29,"condition":"Partly Cloudy" if lang=="en" else ("आंशिक बादल" if lang=="hi" else "अंशतः ढगाळ"),
                "humidity":68,"rainfall_prob":35,"tip":"Good day for irrigation."}

MONTHS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
KHARIF  = {5,6,7,8,9,10}
RABI    = {10,11,0,1,2,3}

# ===================================================═══════════
#  SIDEBAR
# ===================================================═══════════
def render_sidebar():
    with st.sidebar:
        st.markdown(f"""
        <div style="text-align:center;padding:1.5rem 0 1rem;">
          <div style="font-size:2.5rem;margin-bottom:0.4rem;">🌾</div>
          <div style="font-family:'Poppins',sans-serif;font-size:1.1rem;font-weight:900;color:#e0e7ff;">{s('app_name')}</div>
          <div style="font-size:0.7rem;color:#a5b4fc;letter-spacing:0.1em;text-transform:uppercase;margin-top:2px;">{s('tagline')}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown(f"**{s('lang_label')}**")
        lang_options = {"🇮🇳 मराठी":"mr","🇮🇳 हिंदी":"hi","🌐 English":"en"}
        chosen = st.radio("", list(lang_options.keys()),
                          index=list(lang_options.values()).index(st.session_state.lang),
                          label_visibility="collapsed")
        nl = lang_options[chosen]
        if nl != st.session_state.lang:
            st.session_state.lang = nl
            st.session_state.weather_data = None
            st.rerun()

        st.markdown("---")
        st.markdown(f"**{s('api_label')}**")
        api_in = st.text_input("", type="password", placeholder="AIza...",
                               help=s("api_help"), label_visibility="collapsed", key="api_key_input")
        if api_in: st.session_state["_api_key"] = api_in

        if st.session_state.logged_in:
            st.markdown("---")
            st.markdown(f"""
            <div style="background:rgba(99,102,241,0.2);border-radius:14px;padding:0.8rem 1rem;margin-bottom:0.5rem;">
              <div style="font-size:0.7rem;color:#a5b4fc;text-transform:uppercase;letter-spacing:0.08em;">Logged in as</div>
              <div style="font-weight:800;font-size:1rem;color:#e0e7ff;margin-top:3px;">👤 {st.session_state.user_name}</div>
              <div style="font-size:0.78rem;color:#c7d2fe;margin-top:2px;">📱 {st.session_state.phone}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(s("logout"), key="logout_btn", use_container_width=True):
                for k in ["logged_in","user_name","phone","active_feature","weather_data"]:
                    st.session_state[k] = False if k=="logged_in" else None if k in ["active_feature","weather_data"] else ""
                for feat in ["crop","pest","weather","soil","eco"]:
                    st.session_state[f"chat_{feat}"] = []
                st.rerun()

        st.markdown("---")
        st.markdown("""
        <div style="font-size:0.72rem;color:#818cf8;line-height:1.7;">
          <div style="font-weight:800;color:#a5b4fc;margin-bottom:6px;">📌 About</div>
          FA-2 · Generative AI Course<br>
          Streamlit + Gemini 1.5 Flash<br>
          Marathi · Hindi · English<br>
          <br>
          <a href="https://aistudio.google.com" style="color:#818cf8;">Get Free API Key →</a>
        </div>
        """, unsafe_allow_html=True)

# ===================================================═══════════
#  ✨ NEW: CURSOR-REACTIVE ANIMATED LOGIN PAGE
# ===================================================═══════════
def render_login():
    lang = st.session_state.lang
    t = UI[lang]
    login_welcome = t['login_welcome']
    login_sub = t['login_sub']

    # ── 1. Animated background (fixed, z-index 0) ──
    bg_css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@700;900&display=swap');

    /* Hide Streamlit chrome on login page */
    [data-testid="stAppViewContainer"] { background: #0a0f1e !important; }
    [data-testid="stHeader"], #MainMenu, footer { display:none !important; }
    .block-container { padding: 0 !important; max-width: 100% !important; }

    /* Full-screen animated gradient background */
    .login-bg {
      position: fixed; inset: 0; z-index: 0; overflow: hidden;
      background: linear-gradient(135deg, #0a0f1e 0%, #0d1b2a 30%, #0f2b1e 65%, #091a2a 100%);
    }
    /* Gradient blobs -- animated by JS cursor tracking */
    .blob {
      position: absolute; border-radius: 50%;
      filter: blur(90px); opacity: 0.6;
      pointer-events: none; will-change: transform;
    }
    .blob-1 {
      width: 650px; height: 650px; top: -180px; left: -180px;
      background: radial-gradient(circle, rgba(16,185,129,0.75) 0%, rgba(5,150,105,0.3) 45%, transparent 70%);
    }
    .blob-2 {
      width: 580px; height: 580px; bottom: -140px; right: -140px;
      background: radial-gradient(circle, rgba(99,102,241,0.7) 0%, rgba(67,56,202,0.3) 45%, transparent 70%);
    }
    .blob-3 {
      width: 480px; height: 480px; top: 40%; left: 40%;
      transform: translate(-50%, -50%);
      background: radial-gradient(circle, rgba(245,158,11,0.5) 0%, rgba(217,119,6,0.2) 45%, transparent 70%);
    }
    /* Subtle grid overlay */
    .bg-grid {
      position: absolute; inset: 0; pointer-events: none;
      background-image:
        linear-gradient(rgba(16,185,129,0.035) 1px, transparent 1px),
        linear-gradient(90deg, rgba(16,185,129,0.035) 1px, transparent 1px);
      background-size: 55px 55px;
    }
    /* Floating emoji particles */
    .bg-float {
      position: absolute; pointer-events: none;
      opacity: 0.07; filter: blur(0.5px);
      animation: bgfloat linear infinite;
    }
    @keyframes bgfloat {
      0%,100% { transform: translateY(0) rotate(0deg); opacity:0.05; }
      50%      { transform: translateY(-28px) rotate(7deg); opacity:0.09; }
    }

    /* ── GLASSMORPHISM CARD ── */
    /* Target the Streamlit column that holds our login form */
    .login-card-col > div:first-child {
      background: rgba(255,255,255,0.06) !important;
      backdrop-filter: blur(30px) saturate(160%) !important;
      -webkit-backdrop-filter: blur(30px) saturate(160%) !important;
      border: 1px solid rgba(255,255,255,0.13) !important;
      border-radius: 28px !important;
      padding: 2.5rem 1.8rem 2rem !important;
      box-shadow: 0 32px 80px rgba(0,0,0,0.55),
                  0 0 60px rgba(16,185,129,0.08),
                  inset 0 1px 0 rgba(255,255,255,0.12) !important;
      position: relative !important;
      animation: cardIn 0.8s cubic-bezier(0.34,1.4,0.64,1) both !important;
    }
    @keyframes cardIn {
      from { opacity:0; transform: translateY(35px) scale(0.93); }
      to   { opacity:1; transform: translateY(0) scale(1); }
    }

    /* Animated rainbow top border on card */
    .login-card-col > div:first-child::before {
      content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
      border-radius: 28px 28px 0 0;
      background: linear-gradient(90deg, #10b981, #6366f1, #f59e0b, #ec4899, #10b981);
      background-size: 250% 100%;
      animation: borderFlow 4s linear infinite;
    }
    @keyframes borderFlow { 0% { background-position:0% 0%; } 100% { background-position:250% 0%; } }

    /* Logo */
    .login-logo {
      width: 68px; height: 68px;
      background: linear-gradient(135deg, #059669, #10b981);
      border-radius: 20px; margin: 0 auto 1rem; font-size: 2rem;
      display: flex; align-items: center; justify-content: center;
      box-shadow: 0 8px 28px rgba(16,185,129,0.45), 0 0 0 1px rgba(255,255,255,0.1);
      animation: logoFloat 3s ease-in-out infinite;
    }
    @keyframes logoFloat {
      0%,100% { transform:translateY(0); box-shadow:0 8px 28px rgba(16,185,129,0.45); }
      50%      { transform:translateY(-5px); box-shadow:0 14px 36px rgba(16,185,129,0.65); }
    }
    .login-title {
      font-family: 'Poppins', sans-serif; font-size: 1.55rem; font-weight: 900;
      color: #ffffff !important; text-align: center; margin: 0;
      text-shadow: 0 2px 18px rgba(16,185,129,0.35);
    }
    .login-sub {
      font-size: 0.8rem; color: rgba(255,255,255,0.5) !important;
      text-align: center; margin-top: 0.3rem; margin-bottom: 0;
    }
    .login-divider {
      height: 1px; margin: 1.1rem 0;
      background: linear-gradient(90deg, transparent, rgba(255,255,255,0.13), transparent);
    }

    /* Input field dark styling */
    .login-card-col .stTextInput input {
      background: rgba(255,255,255,0.07) !important;
      border: 1.5px solid rgba(255,255,255,0.14) !important;
      border-radius: 12px !important; color: #ffffff !important;
      font-size: 0.92rem !important; padding: 0.7rem 1rem !important;
    }
    .login-card-col .stTextInput input::placeholder { color: rgba(255,255,255,0.3) !important; }
    .login-card-col .stTextInput input:focus {
      border-color: rgba(16,185,129,0.65) !important;
      background: rgba(255,255,255,0.11) !important;
      box-shadow: 0 0 0 3px rgba(16,185,129,0.18) !important;
      color: #ffffff !important;
    }
    .login-card-col .stTextInput label {
      color: rgba(255,255,255,0.65) !important; font-size: 0.75rem !important;
      font-weight: 600 !important; letter-spacing: 0.07em !important;
      text-transform: uppercase !important;
    }

    /* Login button */
    .login-btn-wrap .stButton button {
      background: linear-gradient(135deg, #059669, #10b981) !important;
      color: #ffffff !important; border: none !important;
      border-radius: 13px !important; font-size: 0.98rem !important;
      font-weight: 800 !important; letter-spacing: 0.02em !important;
      box-shadow: 0 6px 22px rgba(16,185,129,0.42) !important;
      transition: all 0.25s cubic-bezier(0.34,1.4,0.64,1) !important;
    }
    .login-btn-wrap .stButton button:hover {
      transform: translateY(-3px) scale(1.02) !important;
      box-shadow: 0 12px 30px rgba(16,185,129,0.55) !important;
    }

    /* Language pills */
    .lang-pill-wrap .stButton button {
      background: rgba(255,255,255,0.06) !important;
      border: 1.5px solid rgba(255,255,255,0.14) !important;
      color: rgba(255,255,255,0.65) !important;
      border-radius: 20px !important; font-size: 0.77rem !important;
      font-weight: 700 !important; padding: 0.35rem 0.4rem !important;
      transition: all 0.2s !important;
    }
    .lang-pill-wrap .stButton button:hover {
      background: rgba(16,185,129,0.18) !important;
      border-color: rgba(16,185,129,0.5) !important;
      color: #ffffff !important; transform: translateY(-1px) !important;
    }

    /* Active language pill */
    .lang-active .stButton button {
      background: linear-gradient(135deg, #059669, #10b981) !important;
      border-color: #10b981 !important; color: #ffffff !important;
      box-shadow: 0 4px 14px rgba(16,185,129,0.38) !important;
    }

    /* Validation hints */
    .hint-ok  { font-size:0.74rem; color:#34d399; font-weight:700; margin:-8px 0 6px; }
    .hint-err { font-size:0.74rem; color:#f87171; font-weight:700; margin:-8px 0 6px; }

    /* Footer row */
    .login-footer { text-align:center; margin-top:0.9rem; }
    .login-forgot {
      font-size:0.76rem; color:rgba(255,255,255,0.35);
      cursor:pointer; display:inline-block; transition:color 0.2s;
    }
    .login-forgot:hover { color:rgba(255,255,255,0.7); text-decoration:underline; }
    .trust-row { display:flex; justify-content:center; gap:14px; flex-wrap:wrap; margin-top:0.7rem; }
    .trust-badge { font-size:0.66rem; color:rgba(255,255,255,0.28); font-weight:600; letter-spacing:0.04em; }

    /* Vertical centering helper */
    .login-spacer { min-height: 10vh; }
    </style>
    """
    st.markdown(bg_css, unsafe_allow_html=True)

    # ── 2. Animated background elements (blobs + floating emojis) ──
    bg_html = """
    <div class="login-bg">
      <div class="bg-grid"></div>
      <div class="blob blob-1" id="blob1"></div>
      <div class="blob blob-2" id="blob2"></div>
      <div class="blob blob-3" id="blob3"></div>
      <div class="bg-float" style="top:7%;left:5%;font-size:2.8rem;animation-duration:7s;">🌾</div>
      <div class="bg-float" style="top:16%;right:8%;font-size:2.1rem;animation-duration:9s;animation-delay:1.5s;">🌿</div>
      <div class="bg-float" style="top:52%;left:3%;font-size:1.9rem;animation-duration:11s;animation-delay:3s;">🌱</div>
      <div class="bg-float" style="bottom:7%;right:6%;font-size:3.2rem;animation-duration:8s;animation-delay:0.5s;">🚜</div>
      <div class="bg-float" style="bottom:20%;left:9%;font-size:2.3rem;animation-duration:10s;animation-delay:2s;">☀️</div>
      <div class="bg-float" style="top:37%;right:4%;font-size:2rem;animation-duration:7.5s;animation-delay:4s;">💧</div>
      <div class="bg-float" style="top:70%;left:48%;font-size:1.7rem;animation-duration:12s;animation-delay:1s;">🌻</div>
    </div>
    """
    st.markdown(bg_html, unsafe_allow_html=True)

    # ── 3. JS cursor tracking (plain string, no f-string) ──
    js = """
    <script>
    (function() {
      /* ===================================================
         CURSOR-REACTIVE BLOB ENGINE
         - Blobs re-fetched from DOM each frame (survives Streamlit re-renders)
         - window._krishiMove stored globally so listener is never duplicated
         - LERP=0.12 gives snappy-but-smooth response at 60fps
         
         CUSTOMIZE:
           LERP : 0.06=smooth, 0.12=default, 0.25=instant
           I1/I2/I3 : pixel range each blob travels
      =================================================== */
      var LERP=0.12, I1=300, I2=350, I3=220, AUTO=0.001;
      var mx=0.5, my=0.5, hasMouse=false, autoT=0;
      var b1x=0,b1y=0, b2x=0,b2y=0, b3x=0,b3y=0;

      function lerp(a,b,t){ return a+(b-a)*t; }
      function get(id){ return document.getElementById(id); }

      function onMove(e){
        hasMouse=true;
        mx=e.clientX/window.innerWidth;
        my=e.clientY/window.innerHeight;
      }
      function onTouch(e){
        if(e.touches.length>0){
          hasMouse=true;
          mx=e.touches[0].clientX/window.innerWidth;
          my=e.touches[0].clientY/window.innerHeight;
        }
      }

      /* Deduplicate listeners across Streamlit re-renders */
      if(window._km){ window.removeEventListener('mousemove',window._km); }
      if(window._kt){ window.removeEventListener('touchmove',window._kt); }
      window._km=onMove; window._kt=onTouch;
      window.addEventListener('mousemove',onMove,{passive:true});
      window.addEventListener('touchmove',onTouch,{passive:true});

      function frame(){
        /* Auto-wave when no mouse */
        if(!hasMouse){
          autoT+=AUTO;
          mx=0.5+0.35*Math.sin(autoT);
          my=0.5+0.28*Math.cos(autoT*0.65);
        }
        var tx,ty,el;

        /* Blob 1 - follows cursor */
        tx=(mx-0.5)*I1; ty=(my-0.5)*I1;
        b1x=lerp(b1x,tx,LERP); b1y=lerp(b1y,ty,LERP);
        el=get('blob1'); if(el) el.style.transform='translate('+b1x.toFixed(1)+'px,'+b1y.toFixed(1)+'px)';

        /* Blob 2 - opposite direction */
        tx=-(mx-0.5)*I2; ty=-(my-0.5)*I2;
        b2x=lerp(b2x,tx,LERP*0.75); b2y=lerp(b2y,ty,LERP*0.75);
        el=get('blob2'); if(el) el.style.transform='translate('+b2x.toFixed(1)+'px,'+b2y.toFixed(1)+'px)';

        /* Blob 3 - diagonal, fastest */
        tx=(mx-0.5)*I3*-0.7; ty=(my-0.5)*I3*1.1;
        b3x=lerp(b3x,tx,LERP*1.5); b3y=lerp(b3y,ty,LERP*1.5);
        el=get('blob3'); if(el) el.style.transform='translate('+b3x.toFixed(1)+'px,'+b3y.toFixed(1)+'px)';

        requestAnimationFrame(frame);
      }

      /* Single loop guard */
      if(!window._kloop){ window._kloop=true; requestAnimationFrame(frame); }
    })();
    </script>
    """
    st.markdown(js, unsafe_allow_html=True)

    # ── 4. Centered Streamlit form (this IS the glass card via CSS targeting) ──
    st.markdown("<div class='login-spacer'></div>", unsafe_allow_html=True)
    _, col, _ = st.columns([1, 1.4, 1])

    with col:
        # Mark this column so CSS can target it
        st.markdown("<div class='login-card-col'>", unsafe_allow_html=True)

        # Header (logo + title inside the card)
        st.markdown(f"""
        <div class="login-logo">🌾</div>
        <div class="login-title">{login_welcome}</div>
        <div class="login-sub">{login_sub}</div>
        <div class="login-divider"></div>
        """, unsafe_allow_html=True)

        # Language selector
        st.markdown("<div class='lang-pill-wrap'>", unsafe_allow_html=True)
        lmap = {"मराठी": "mr", "हिंदी": "hi", "English": "en"}
        lcols = st.columns(3)
        for col2, (label, code) in zip(lcols, lmap.items()):
            is_active = st.session_state.lang == code
            with col2:
                # Wrap active pill with extra class
                if is_active:
                    st.markdown("<div class='lang-active'>", unsafe_allow_html=True)
                if st.button(label, key=f"ll_{code}", use_container_width=True):
                    st.session_state.lang = code
                    st.rerun()
                if is_active:
                    st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

        # Name input
        name = st.text_input("👤  " + t['name_label'], placeholder=t["name_ph"], key="ln")
        if name:
            greet = {"en": "Hello", "hi": "नमस्ते", "mr": "नमस्कार"}[lang]
            st.markdown(f"<div class='hint-ok'>✓ {greet}, {name}!</div>", unsafe_allow_html=True)

        # Phone input
        phone = st.text_input("📱  " + t['phone_label'], placeholder=t["phone_ph"], key="lp", max_chars=10)
        if phone:
            ok = len(phone) == 10 and phone.isdigit()
            if ok:
                st.markdown("<div class='hint-ok'>✓ Valid number</div>", unsafe_allow_html=True)
            else:
                rem = 10 - len(phone)
                st.markdown(f"<div class='hint-err'>✗ {rem} digit{'s' if rem!=1 else ''} remaining</div>", unsafe_allow_html=True)

        st.markdown("<div style='height:0.3rem'></div>", unsafe_allow_html=True)

        # Login button
        st.markdown("<div class='login-btn-wrap'>", unsafe_allow_html=True)
        if st.button(t["login_btn"], key="lbtn", use_container_width=True):
            if not name.strip():
                errs = {"en": "Please enter your name.", "hi": "कृपया नाम दर्ज करें।", "mr": "कृपया नाव टाका."}
                st.error(errs[lang])
            elif len(phone) != 10 or not phone.isdigit():
                errs = {"en": "Please enter a valid 10-digit number.",
                        "hi": "कृपया 10 अंकों का सही नंबर दर्ज करें।",
                        "mr": "कृपया योग्य १० अंकी नंबर टाका."}
                st.error(errs[lang])
            else:
                st.session_state.logged_in = True
                st.session_state.user_name = name.strip()
                st.session_state.phone = phone.strip()
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

        # Footer
        st.markdown("""
        <div class="login-footer">
          <span class="login-forgot">Forgot password? Contact support &rarr;</span>
          <div class="trust-row">
            <span class="trust-badge">🔒 Secure</span>
            <span class="trust-badge">🤖 AI-Powered</span>
            <span class="trust-badge">🌾 50+ Crops</span>
            <span class="trust-badge">🇮🇳 Made in India</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)  # close login-card-col


def render_hero(api_key):
    t  = UI[st.session_state.lang]
    nm = st.session_state.user_name

    if st.session_state.weather_data is None and api_key:
        with st.spinner(""):
            st.session_state.weather_data = get_weather(api_key, st.session_state.lang)
    w = st.session_state.weather_data

    # Render hero banner
    st.markdown(f"""
    <div class="hero">
      <div class="hero-badge">📍 {t['location']}</div>
      <h2 class="hero-name">{t['greeting']}, {nm}! 👋</h2>
      <p class="hero-sub">{t['hero_sub']}</p>
    </div>
    """, unsafe_allow_html=True)

    # Render weather pill separately (avoids nested HTML variable issue)
    if w:
        hum_pct  = w["humidity"]
        rain_pct = w["rainfall_prob"]
        temp     = round(w["temp"])
        cond     = w["condition"]
        st.markdown(f"""
        <div class="weather-pill" style="margin-top:-1rem;margin-bottom:1rem;">
          <div class="w-temp">{temp}°<span style="font-size:1.1rem;opacity:0.55">C</span></div>
          <div style="width:1px;background:rgba(255,255,255,0.25);height:50px;"></div>
          <div class="w-info">
            <div style="font-weight:800;font-size:0.9rem;">☁️ {cond}</div>
            <div>💧 {t['humidity']}: {hum_pct}%
              <div class="w-bar-wrap"><div class="w-bar" style="width:{hum_pct}%;background:rgba(255,255,255,0.7);"></div></div>
            </div>
            <div>🌧 {t['rain']}: {rain_pct}%
              <div class="w-bar-wrap"><div class="w-bar" style="width:{rain_pct}%;background:rgba(147,197,253,0.9);"></div></div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

# ===================================================═══════════
#  STATS ROW
# ===================================================═══════════
def render_stats():
    t = UI[st.session_state.lang]
    colors = [
        ("linear-gradient(135deg,#ede9fe,#ddd6fe)","#6d28d9"),
        ("linear-gradient(135deg,#d1fae5,#a7f3d0)","#065f46"),
        ("linear-gradient(135deg,#fef3c7,#fde68a)","#92400e"),
        ("linear-gradient(135deg,#dbeafe,#bfdbfe)","#1e40af"),
    ]
    html = '<div class="stats-row">'
    for i,(lbl,val) in enumerate(zip(t["stats"],t["stat_vals"])):
        bg,col = colors[i]
        html += f"""<div class="stat-card" style="background:{bg};animation-delay:{i*0.1}s;">
          <div class="stat-val" style="color:{col};">{val}</div>
          <div class="stat-lbl" style="color:{col};">{lbl}</div>
        </div>"""
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

# ===================================================═══════════
#  SEASON TRACKER
# ===================================================═══════════
def render_season_tracker():
    t = UI[st.session_state.lang]
    now_m = datetime.datetime.now().month % 12
    kharif_lbl = {"en":"Kharif","hi":"खरीफ","mr":"खरीप"}[st.session_state.lang]
    rabi_lbl   = {"en":"Rabi","hi":"रबी","mr":"रब्बी"}[st.session_state.lang]
    st.markdown(f"<div style='font-weight:800;color:#374151;font-size:0.9rem;margin-top:1rem;'>{t['season_label']}</div>", unsafe_allow_html=True)
    pills_html = '<div class="season-row">'
    for i,m in enumerate(MONTHS):
        active = (i == now_m)
        is_k = i in KHARIF
        if active:
            color = "#16a34a" if is_k else "#2563eb"
            pills_html += f'<div class="season-pill active" style="background:{color};border-color:{color};">{m} ◀</div>'
        else:
            pills_html += f'<div class="season-pill inactive">{m}</div>'
    pills_html += '</div>'
    pills_html += f'<div style="font-size:0.75rem;font-weight:700;color:#6b7280;margin-top:-4px;">🟢 {kharif_lbl}  🔵 {rabi_lbl}</div>'
    st.markdown(pills_html, unsafe_allow_html=True)

# ===================================================═══════════
#  DID YOU KNOW
# ===================================================═══════════
def render_dyk():
    t = UI[st.session_state.lang]
    facts = t["did_you_know"]
    idx = st.session_state.dyk_idx % len(facts)
    c1, c2 = st.columns([5,1])
    with c1:
        st.markdown(f"""
        <div class="dyk-card">
          <div class="dyk-icon">💡</div>
          <div class="dyk-text">{facts[idx]}</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        if st.button("Next →", key="dyk_next"):
            st.session_state.dyk_idx += 1
            st.rerun()

# ===================================================═══════════
#  FEATURE CARDS
# ===================================================═══════════
def render_feature_cards():
    t = UI[st.session_state.lang]
    feats = list(zip(t["features"], t["feat_ids"]))
    cols  = st.columns(5)
    for i, (label, fid) in enumerate(feats):
        gf, gt, acc, bg, icon = FEAT_THEME[fid]
        with cols[i]:
            # Single styled button - no HTML div on top to block clicks
            st.markdown(f"""
            <style>
            div[data-testid="stButton"] button[kind="secondary"][id="feat_{fid}"] {{
                background:{bg} !important; border:2px solid {acc} !important;
            }}
            </style>
            <div style="background:{bg};border:2px solid {acc};border-radius:22px;
                 padding:1.2rem 0.5rem 0.6rem;text-align:center;margin-bottom:4px;
                 pointer-events:none;">
              <div style="width:58px;height:58px;border-radius:16px;margin:0 auto 0.6rem;
                   background:linear-gradient(135deg,{gf},{gt});display:flex;
                   align-items:center;justify-content:center;font-size:1.7rem;
                   box-shadow:0 5px 16px rgba(0,0,0,0.18);">{icon}</div>
              <div style="font-size:0.8rem;font-weight:700;color:{gf};">{label}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(t["open_chat"], key=f"feat_{fid}", use_container_width=True):
                st.session_state.active_feature = fid
                st.rerun()

# ===================================================═══════════
#  TIP CARD
# ===================================================═══════════
def render_tip():
    t = UI[st.session_state.lang]
    w = st.session_state.weather_data
    tip = (w.get("tip","") if w else "") or t["tip"]
    st.markdown(f"""
    <div class="tip-card">
      <div class="tip-title">{t['daily_tip']}</div>
      <div class="tip-text">"{tip}"</div>
    </div>
    """, unsafe_allow_html=True)

# ===================================================═══════════
#  CHAT
# ===================================================═══════════
def render_chat(feat_id, api_key):
    lang = st.session_state.lang
    t    = UI[lang]
    gf, gt, acc, bg, icon = FEAT_THEME[feat_id]
    feat_label = t["features"][t["feat_ids"].index(feat_id)]
    key      = f"chat_{feat_id}"
    chip_key = f"chip_sel_{feat_id}"
    inp_key  = f"inp_val_{feat_id}"

    # Initialise session keys
    if chip_key not in st.session_state:
        st.session_state[chip_key] = ""
    if inp_key not in st.session_state:
        st.session_state[inp_key] = ""
    if key not in st.session_state:
        st.session_state[key] = []

    msgs = st.session_state[key]

    # ── Chat header ──
    st.markdown(f"""
    <div class="chat-hdr" style="background:{bg};border-color:{acc};">
      <div class="chat-hdr-icon" style="background:linear-gradient(135deg,{gf},{gt});">{icon}</div>
      <div>
        <div class="chat-hdr-name" style="color:{gf};">{feat_label}</div>
        <div class="chat-hdr-sub">Gemini 1.5 Flash · AI Powered</div>
      </div>
      <div style="margin-left:auto;width:10px;height:10px;border-radius:50%;background:#22c55e;
           box-shadow:0 0 6px #22c55e;"></div>
    </div>
    """, unsafe_allow_html=True)

    # ── Message history ──
    # ── Message display ── (single st.markdown call avoids code-block rendering bug)
    import html as _html
    chat_parts = []
    chat_parts.append(f'<div class="chat-wrap" style="background:#fafafa;border-color:{acc};padding:1rem 1.2rem;min-height:220px;">')

    if not msgs:
        chat_parts.append(f'''
        <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;
             padding:2.5rem 1rem;text-align:center;opacity:0.6;">
          <div style="font-size:3rem;margin-bottom:0.7rem;">{icon}</div>
          <div style="font-weight:800;font-size:1rem;color:#111827;">{t["greeting_chat"]}</div>
          <div style="font-size:0.78rem;color:#9ca3af;margin-top:0.3rem;">AI Agricultural Expert</div>
        </div>''')
    else:
        import re as _re
        for m in msgs:
            ts = m.get("time","")
            if m["role"] == "user":
                safe_text = _html.escape(m["text"])
                img_note = f'<div style="font-size:0.75rem;opacity:0.7;margin-bottom:3px;">📷 {t["img_caption"]}</div>' if m.get("has_image") else ""
                chat_parts.append(
                    f'<div class="msg-user-wrap">' +
                    f'<div>{img_note}' +
                    f'<div class="msg-user" style="background:linear-gradient(135deg,{gf},{gt});">{safe_text}</div>' +
                    f'<div class="msg-time" style="text-align:right;">{ts}</div>' +
                    f'</div>' +
                    f'<div class="msg-avatar" style="margin-left:8px;background:linear-gradient(135deg,{gf},{gt});">👤</div>' +
                    f'</div>'
                )
            else:
                safe_text = _html.escape(m["text"])
                safe_text = _re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', safe_text)
                safe_text = _re.sub(r'\*(.*?)\*', r'<i>\1</i>', safe_text)
                safe_text = safe_text.replace("\n", "<br>")
                chat_parts.append(
                    f'<div class="msg-bot-wrap">' +
                    f'<div class="msg-avatar" style="margin-right:8px;">🤖</div>' +
                    f'<div style="max-width:78%;">' +
                    f'<div class="msg-bot" style="border:2px solid {acc};">{safe_text}</div>' +
                    f'<div class="msg-time">{ts}</div>' +
                    f'</div></div>'
                )

    chat_parts.append('</div>')
    st.markdown("".join(chat_parts), unsafe_allow_html=True)

    # ── Quick Prompt chips ──
    st.markdown("<div style='font-size:0.78rem;font-weight:700;color:#6b7280;margin:0.8rem 0 0.4rem;'>⚡ Quick Prompts</div>", unsafe_allow_html=True)
    qps = t["quick_prompts"]
    chip_cols = st.columns(len(qps))
    for i, qp in enumerate(qps):
        with chip_cols[i]:
            if st.button(qp, key=f"chip_{feat_id}_{i}", use_container_width=True):
                # Save chip text and clear old input value, then rerun
                st.session_state[chip_key] = qp
                st.session_state[inp_key]  = qp
                st.rerun()

    # ── Image upload ──
    with st.expander(t["upload_img"]):
        uploaded = st.file_uploader("", type=["jpg","jpeg","png","webp"],
                                    key=f"img_{feat_id}", label_visibility="collapsed")
        if uploaded:
            img_obj = Image.open(uploaded).convert("RGB")
            st.image(img_obj, width=180, caption=t["img_caption"])

    # ── Text input + Send button ──
    # Use on_change callback to keep inp_key in sync with what user types
    def _sync_input():
        st.session_state[inp_key] = st.session_state[f"inp_{feat_id}"]

    in_col, send_col = st.columns([5, 1])
    with in_col:
        user_input = st.text_input(
            "", placeholder=t["chat_ph"],
            key=f"inp_{feat_id}",
            value=st.session_state[inp_key],
            label_visibility="collapsed",
            on_change=_sync_input,
        )
    with send_col:
        send_clicked = st.button(t["send"], key=f"send_{feat_id}", use_container_width=True)

    if user_input:
        st.markdown(f"<div style='font-size:0.7rem;color:#9ca3af;text-align:right;margin-top:-8px;'>{len(user_input)} chars</div>", unsafe_allow_html=True)

    # ── Clear / Download ──
    c1, c2, _ = st.columns([1, 1, 3])
    with c1:
        if st.button(t["clear_chat"], key=f"clr_{feat_id}"):
            st.session_state[key]      = []
            st.session_state[chip_key] = ""
            st.session_state[inp_key]  = ""
            st.rerun()
    with c2:
        if msgs:
            txt = "\n\n".join(
                f"[{m['time']}] {'You' if m['role']=='user' else 'Krishi Sahayak'}: {m['text']}"
                for m in msgs
            )
            st.download_button(t["download_chat"], data=txt,
                               file_name=f"chat_{feat_id}.txt", mime="text/plain",
                               key=f"dl_{feat_id}")

    # ── Handle send ──
    final_text = st.session_state[inp_key].strip()
    if send_clicked and (final_text or uploaded is not None):
        if not api_key:
            st.error(t["api_missing"])
            return

        now      = datetime.datetime.now().strftime("%H:%M")
        has_img  = uploaded is not None
        utext    = final_text or ("📷 " + t["img_caption"])

        st.session_state[key].append({"role":"user","text":utext,"time":now,"has_image":has_img})

        feat_ctx    = FEATURE_PROMPTS[feat_id][lang]
        full_prompt = f"[Category: {feat_ctx}]\n\n{utext}"

        with st.spinner(t["thinking"]):
            try:
                client = make_model(api_key)
                if uploaded:
                    img_obj = Image.open(uploaded).convert("RGB")
                    buf = io.BytesIO()
                    img_obj.save(buf, format="JPEG")
                    img_b64 = base64.b64encode(buf.getvalue()).decode()
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=[
                            types.Part.from_text(text=full_prompt),
                            types.Part.from_bytes(data=base64.b64decode(img_b64), mime_type="image/jpeg")
                        ],
                        config=types.GenerateContentConfig(
                            system_instruction=SYSTEM_PROMPTS[st.session_state.lang],
                            temperature=0.7,
                            max_output_tokens=700
                        )
                    )
                else:
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=full_prompt,
                        config=types.GenerateContentConfig(
                            system_instruction=SYSTEM_PROMPTS[st.session_state.lang],
                            temperature=0.7,
                            max_output_tokens=700
                        )
                    )
                bot_text = response.text.strip()
            except Exception as e:
                bot_text = t["error_msg"] + f"\n(Error: {str(e)[:80]})"

        st.session_state[key].append({"role":"model","text":bot_text,"time":now})
        # Clear input after successful send
        st.session_state[chip_key] = ""
        st.session_state[inp_key]  = ""
        st.rerun()


# ===================================================═══════════
#  VALIDATION TAB
# ===================================================═══════════
def render_validation(api_key):
    t = UI[st.session_state.lang]
    st.markdown("""
    <div style="background:linear-gradient(135deg,#eff6ff,#dbeafe);border-radius:16px;
    padding:1rem 1.4rem;margin-bottom:1rem;border-left:4px solid #3b82f6;">
      <b style="color:#1d4ed8;">What is Model Validation?</b><br>
      <span style="font-size:0.85rem;color:#1e40af;">Test the AI with 6 diverse prompts from India, Canada & Ghana.
      Compare results and measure response quality automatically.</span>
    </div>
    """, unsafe_allow_html=True)

    test_prompts = [
        {"flag":"🇮🇳","region":"Rajasthan, India","season":"August","crop":"Millet","q":"What crops should I sow in August in Rajasthan?"},
        {"flag":"🇮🇳","region":"Punjab, India","season":"November","crop":"Wheat","q":"How do I manage rust disease in wheat during winter?"},
        {"flag":"🇨🇦","region":"Ontario, Canada","season":"May","crop":"Canola","q":"What is the best sowing time and spacing for canola in Ontario?"},
        {"flag":"🇨🇦","region":"Saskatchewan, Canada","season":"July","crop":"Barley","q":"How do I identify and treat barley yellow dwarf virus?"},
        {"flag":"🇬🇭","region":"Northern Ghana","season":"June","crop":"Maize","q":"How can I improve maize yield during the rainy season in northern Ghana?"},
        {"flag":"🇬🇭","region":"Ashanti, Ghana","season":"March","crop":"Cocoa","q":"What fertilizers and pest control work best for cocoa in Ashanti?"},
    ]

    idx = st.selectbox("", range(len(test_prompts)),
                       format_func=lambda i: f"{test_prompts[i]['flag']} Prompt {i+1}: {test_prompts[i]['region']} — {test_prompts[i]['q'][:50]}...",
                       key="val_sel", label_visibility="collapsed")
    tp = test_prompts[idx]

    c1,c2,c3,c4 = st.columns(4)
    c1.info(f"📍 {tp['region']}")
    c2.info(f"📅 {tp['season']}")
    c3.info(f"🌱 {tp['crop']}")
    c4.info(f"❓ Test {idx+1} / 6")
    st.markdown(f"<b>Question:</b> <i>{tp['q']}</i>", unsafe_allow_html=True)

    if st.button(t["run_test"], key="vrun"):
        if not api_key:
            st.error(t["api_missing"])
        else:
            prompt = f"""You are an expert agricultural AI for {tp['region']}.
Farmer grows {tp['crop']} in {tp['season']}.
Question: {tp['q']}
Provide 3-4 numbered recommendations with 'Why:' justifications. Be region-specific."""
            with st.spinner(t["thinking"]):
                try:
                    client2 = genai.Client(api_key=api_key)
                    r2 = client2.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=prompt,
                        config=types.GenerateContentConfig(temperature=0.5, max_output_tokens=600)
                    )
                    out = r2.text.strip()
                except Exception as e:
                    out = f"Error: {str(e)}"

            st.markdown("#### 📋 AI Response")
            st.markdown(f'<div class="val-output">{out}</div>', unsafe_allow_html=True)

            st.markdown("#### 🔍 Auto Quality Check")
            has_why     = "why" in out.lower() or "because" in out.lower()
            has_num     = any(f"{i}." in out for i in range(1,5))
            has_crop    = tp["crop"].lower() in out.lower()
            wc          = len(out.split())
            good_len    = 60 < wc < 500

            vm1,vm2,vm3,vm4 = st.columns(4)
            def colored_metric(col, label, val, good):
                bg = "#d1fae5" if good else "#fee2e2"
                col_c = "#065f46" if good else "#991b1b"
                col.markdown(f"""<div style="background:{bg};border-radius:12px;padding:0.8rem;text-align:center;">
                <div style="font-size:0.7rem;font-weight:700;text-transform:uppercase;color:{col_c};opacity:0.7;">{label}</div>
                <div style="font-size:1.2rem;font-weight:900;color:{col_c};">{val}</div>
                </div>""", unsafe_allow_html=True)

            colored_metric(vm1, "Crop-specific", "✅ Yes" if has_crop else "⚠️ Partial", has_crop)
            colored_metric(vm2, "Has Reasoning", "✅ Yes" if has_why  else "❌ No", has_why)
            colored_metric(vm3, "Numbered List", "✅ Yes" if has_num  else "❌ No", has_num)
            colored_metric(vm4, "Word Count",    f"{wc} words", good_len)

# ===================================================═══════════
#  FEEDBACK CHECKLIST TAB
# ===================================================═══════════
def render_checklist():
    import pandas as pd
    checks = [
        ("📍","Is the advice specific to the input region/location?"),
        ("🧠","Does the output provide valid and logical reasoning?"),
        ("🗣","Is the language simple enough for a layperson?"),
        ("🎯","Are outputs free from being too generic or technical?"),
        ("🛡","Does the model avoid misleading or unsafe advice?"),
        ("🔢","Are numbered recommendations clearly listed?"),
        ("❓","Is each recommendation followed by a 'Why' justification?"),
        ("🌦","Is the response relevant to the current season/crop stage?"),
        ("⚡","Would a farmer be able to act on this advice immediately?"),
        ("🔍","Is the response free of hallucinated or unverifiable facts?"),
    ]
    option_colors = {"✅ Yes":"#d1fae5","⚠️ Partial":"#fef3c7","❌ No":"#fee2e2"}
    scores = {}
    for i,(emoji,check) in enumerate(checks):
        c1, c2 = st.columns([5,1])
        with c1:
            st.markdown(f"""
            <div style="background:white;border:2px solid #f3f4f6;border-radius:12px;
            padding:0.7rem 1rem;margin-bottom:6px;display:flex;align-items:center;gap:10px;">
              <span style="font-size:1.2rem;">{emoji}</span>
              <span style="font-weight:600;font-size:0.88rem;color:#374151;">{check}</span>
            </div>""", unsafe_allow_html=True)
        with c2:
            scores[i] = st.selectbox("", list(option_colors.keys()),
                                     key=f"chk_{i}", label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("📊 Generate Score Report", key="gen_rep"):
        yes     = sum(1 for v in scores.values() if v=="✅ Yes")
        partial = sum(1 for v in scores.values() if v=="⚠️ Partial")
        no      = sum(1 for v in scores.values() if v=="❌ No")
        pct     = round((yes + 0.5*partial) / len(checks) * 100, 1)

        if pct >= 80:    ring_col,ring_bg,msg_fn = "#059669","#d1fae5", st.success
        elif pct >= 60:  ring_col,ring_bg,msg_fn = "#d97706","#fef3c7", st.warning
        else:            ring_col,ring_bg,msg_fn = "#dc2626","#fee2e2", st.error

        sc1,sc2,sc3,sc4,sc5 = st.columns(5)
        def score_box(col,label,val,bg,col_c):
            col.markdown(f"""<div style="background:{bg};border-radius:14px;padding:0.9rem;
            text-align:center;border:2px solid {col_c}22;">
            <div style="font-size:0.68rem;font-weight:700;text-transform:uppercase;color:{col_c};opacity:0.7;letter-spacing:0.06em;">{label}</div>
            <div style="font-size:1.7rem;font-weight:900;color:{col_c};">{val}</div>
            </div>""", unsafe_allow_html=True)

        score_box(sc1,"Score",f"{pct}%",ring_bg,ring_col)
        score_box(sc2,"✅ Passed",yes,"#d1fae5","#059669")
        score_box(sc3,"⚠️ Partial",partial,"#fef3c7","#d97706")
        score_box(sc4,"❌ Failed",no,"#fee2e2","#dc2626")
        score_box(sc5,"Total",len(checks),"#ede9fe","#7c3aed")

        st.markdown(f"""
        <div style="margin:1rem 0 0.5rem;font-size:0.8rem;font-weight:700;color:#374151;">Overall Score</div>
        <div class="prog-wrap" style="height:14px;border-radius:7px;">
          <div class="prog-bar" style="width:{pct}%;background:linear-gradient(90deg,{ring_col},{ring_col}88);"></div>
        </div>
        <div style="text-align:right;font-size:0.75rem;font-weight:700;color:{ring_col};margin-top:3px;">{pct}%</div>
        """, unsafe_allow_html=True)

        if pct >= 80:   msg_fn("🏆 Excellent! AI response meets high quality standards.")
        elif pct >= 60: msg_fn("⚠️ Good, but some improvements needed.")
        else:           msg_fn("❌ Low quality. Try refining prompts or lowering temperature.")

        failed = [(emoji,check) for i,(emoji,check) in enumerate(checks) if scores[i]=="❌ No"]
        if failed:
            st.markdown("**🔧 Suggestions to improve:**")
            for em,ch in failed:
                st.markdown(f"- {em} {ch}")

        df = pd.DataFrame([{"#":i+1,"Emoji":em,"Criteria":ch,"Rating":scores[i]}
                           for i,(em,ch) in enumerate(checks)])
        c1,c2 = st.columns(2)
        with c1:
            st.download_button("⬇ Download CSV", data=df.to_csv(index=False),
                               file_name="krishi_checklist.csv", mime="text/csv")
        with c2:
            st.markdown(f"<div style='background:{ring_bg};border-radius:10px;padding:0.6rem 1rem;text-align:center;font-weight:800;color:{ring_col};'>Final Grade: {'A 🏆' if pct>=80 else 'B ✅' if pct>=60 else 'C ⚠️'}</div>", unsafe_allow_html=True)

# ===================================================═══════════
#  MAIN DASHBOARD
# ===================================================═══════════
def render_dashboard():
    api_key = get_api_key()

    if st.session_state.active_feature:
        fid = st.session_state.active_feature
        t   = UI[st.session_state.lang]
        gf, gt, acc, bg, icon = FEAT_THEME[fid]

        back_col, title_col = st.columns([1,5])
        with back_col:
            if st.button(t["back"], key="back_btn"):
                st.session_state.active_feature = None
                st.rerun()
        with title_col:
            feat_label = t["features"][t["feat_ids"].index(fid)]
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:0.5rem;">
              <div style="width:36px;height:36px;border-radius:10px;background:linear-gradient(135deg,{gf},{gt});
              display:flex;align-items:center;justify-content:center;font-size:1.2rem;color:white;">{icon}</div>
              <div style="font-family:'Poppins',sans-serif;font-size:1.4rem;font-weight:900;color:{gf};">{feat_label}</div>
            </div>
            """, unsafe_allow_html=True)

        render_chat(fid, api_key)
        return

    render_hero(api_key)
    render_stats()

    t = UI[st.session_state.lang]
    st.markdown(f"""<div style="font-family:'Poppins',sans-serif;font-size:1.2rem;font-weight:900;
    color:#1e1b4b;border-bottom:3px solid;border-image:linear-gradient(90deg,#6366f1,#10b981,#f59e0b) 1;
    padding-bottom:8px;margin:1.5rem 0 1rem;">🚜 {t['tagline']}</div>""", unsafe_allow_html=True)

    render_feature_cards()
    render_season_tracker()
    render_tip()
    render_dyk()

    st.markdown("<br>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs([f"🔬 {t['validation_title']}", f"📊 {t['checklist_title']}"])
    with tab1:
        render_validation(api_key)
    with tab2:
        render_checklist()

# ===================================================═══════════
#  ENTRY POINT
# ===================================================═══════════
inject_css()
render_sidebar()

if not st.session_state.logged_in:
    render_login()
else:
    render_dashboard()