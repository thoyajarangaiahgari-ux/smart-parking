import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np
import io
from gtts import gTTS
import base64

# ==========================================
# 1. PAGE CONFIGURATION & PREMIUM THEMING
# ==========================================
st.set_page_config(
    page_title="ParkSmart | Premium Smart Parking",
    page_icon="🅿️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Premium CSS injecting futuristic glowing themes, broken title lines, and floating animations
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght=500;700;900&family=Inter:wght=300;400;600&display=swap');
    
    /* Main Theme Overrides with Background Layer Support */
    .stApp {
        background: radial-gradient(circle at 50% 50%, rgba(6, 9, 19, 0.98) 0%, rgba(1, 2, 6, 1) 100%) !important;
        color: #f8fafc;
        font-family: 'Inter', sans-serif;
        overflow-x: hidden;
    }
    
    /* Hide Default Header, Footers and Sidebars Decorators */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Premium Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #010206 !important;
        border-right: 2px solid #3b82f6 !important;
        box-shadow: 5px 0 35px rgba(59, 130, 246, 0.2);
    }
    
    /* Logo Container: PARK and SMART in separate lines */
    .logo-container {
        text-align: center;
        padding: 20px 10px;
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.4) 0%, rgba(15, 23, 42, 0.8) 100%);
        border-radius: 20px;
        border: 2px solid rgba(59, 130, 246, 0.4);
        box-shadow: 0 0 30px rgba(59, 130, 246, 0.25);
        margin-bottom: 30px;
    }
    .brand-title-line1 {
        font-family: 'Orbitron', sans-serif;
        font-size: 2.2rem;
        font-weight: 900;
        background: linear-gradient(45deg, #3b82f6, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-transform: uppercase;
        letter-spacing: 3px;
        margin-bottom: 0px;
    }
    .brand-title-line2 {
        font-family: 'Orbitron', sans-serif;
        font-size: 2.2rem;
        font-weight: 900;
        background: linear-gradient(45deg, #8b5cf6, #ec4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-transform: uppercase;
        letter-spacing: 3px;
        margin-top: -5px;
        margin-bottom: 5px;
    }
    .brand-subtitle {
        font-size: 0.8rem;
        color: #94a3b8;
        letter-spacing: 3px;
        text-transform: uppercase;
        font-weight: 600;
    }
    
    /* Inference Results Layout Blocks */
    .result-card-available {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.08) 0%, rgba(5, 150, 105, 0.25) 100%);
        border: 2px solid #10b981;
        padding: 35px;
        border-radius: 24px;
        box-shadow: 0 0 45px rgba(16, 185, 129, 0.35);
        text-align: center;
    }
    .result-card-full {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.08) 0%, rgba(220, 38, 38, 0.25) 100%);
        border: 2px solid #ef4444;
        padding: 35px;
        border-radius: 24px;
        box-shadow: 0 0 45px rgba(239, 68, 68, 0.35);
        text-align: center;
    }
    .result-text-main {
        font-family: 'Orbitron', sans-serif;
        font-size: 2.6rem;
        font-weight: 900;
        margin-bottom: 15px;
        letter-spacing: 1px;
    }
    .result-text-sub {
        font-size: 1.4rem;
        color: #f1f5f9;
        line-height: 1.6;
    }
    /* Premium Title Gradient Box Header Container */
    .gradient-header-box {
        background: linear-gradient(90deg, #1e40af 0%, #6b21a8 50%, #9d174d 100%) !important;
        color: #ffffff !important; /* <--- ADD THIS LINE HERE */
        padding: 24px !important;
        border-radius: 16px !important;
        box-shadow: 0 10px 30px rgba(139, 92, 246, 0.3) !important;
        text-align: center !important;
        margin-bottom: 35px !important;
        width: 100% !important;
    }
    /* Metrics panels */
    .metric-card {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(59, 130, 246, 0.25);
        border-radius: 16px;
        padding: 22px;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
    }
    .metric-lbl { font-size: 0.85rem; font-weight: 600; letter-spacing: 1.5px; text-transform: uppercase; }
    .metric-val { font-family: 'Orbitron', sans-serif; font-size: 2.2rem; font-weight: 700; margin-top: 8px; }

    /* Custom Centered File Uploader styling */
    [data-testid="stFileUploader"] {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.7) 0%, rgba(3, 7, 18, 0.9) 100%) !important;
        border: 2px dashed rgba(59, 130, 246, 0.4) !important;
        border-radius: 20px !important;
        padding: 30px !important;
        box-shadow: 0 0 40px rgba(59, 130, 246, 0.15) !important;
    }
    /* Custom Centered File Uploader styling with Forced High-Contrast visibility */
    [data-testid="stFileUploader"] {
        background: linear-gradient(135deg, #0f172a 0%, #020617 100%) !important;
        border: 2px dashed #3b82f6 !important;
        border-radius: 20px !important;
        padding: 30px !important;
        box-shadow: 0 0 40px rgba(59, 130, 246, 0.25) !important;
    }
    
    /* Forces all subtext, limitations, and prompt labels inside the uploader to be bright and clear */
    [data-testid="stFileUploader"] text, 
    [data-testid="stFileUploader"] span, 
    [data-testid="stFileUploader"] div, 
    [data-testid="stFileUploader"] label {
        color: #94a3b8 !important;
    }
    
    /* Fixes the 'Browse files' internal button text so it stands out sharply */
    [data-testid="stFileUploader"] button {
        background-color: #1e293b !important;
        color: #3b82f6 !important;
        border: 1px solid #3b82f6 !important;
    }
    
    /* POWERFUL STYLE FIX FOR ALL LOWER BUTTONS TO REMOVE THE WHITE COVER COLOR */
    div.stButton > button {
        background-color: #0b0f19 !important;
        color: #3b82f6 !important;
        border: 2px solid #3b82f6 !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        padding: 12px 20px !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.2) !important;
        transition: all 0.2s ease-in-out;
        width: 100% !important;
    }
    div.stButton > button:hover {
        background-color: #3b82f6 !important;
        color: #ffffff !important;
        box-shadow: 0 0 25px rgba(59, 130, 246, 0.6) !important;
        border-color: transparent !important;
    }
    
    /* Hardware-Accelerated Floating Background Layer */
    .skyway-viewport {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        pointer-events: none;
        z-index: -1;
        overflow: hidden;
    }
    .floater {
        position: absolute;
        font-size: 4rem;
        user-select: none;
        animation-fill-mode: both;
    }
    .f-car1 { top: 15%; animation: driftRight 22s linear infinite; }
    .f-bike1 { top: 40%; animation: driftLeft 18s linear infinite; }
    .f-car2 { top: 65%; animation: driftRight 26s linear infinite; }
    .f-bike2 { top: 80%; animation: driftLeft 21s linear infinite; }

    @keyframes driftRight {
        0% { left: -100px; opacity: 0; transform: scale(0.8) translateY(0px); }
        10% { opacity: 0.15; }
        90% { opacity: 0.15; }
        100% { left: 105vw; opacity: 0; transform: scale(0.8) translateY(-20px); }
    }
    @keyframes driftLeft {
        0% { right: -100px; opacity: 0; transform: scaleX(-1) scale(0.8) translateY(0px); }
        10% { opacity: 0.15; }
        90% { opacity: 0.15; }
        100% { right: 105vw; opacity: 0; transform: scaleX(-1) scale(0.8) translateY(20px); }
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. ACTIVE FLOATING BACKGROUND CONTAINER
# ==========================================
floating_bg_html = """
<div class="skyway-viewport">
    <div class="floater f-car1">🚗</div>
    <div class="floater f-bike1">🏍️</div>
    <div class="floater f-car2">🚙</div>
    <div class="floater f-bike2">🏍️</div>
</div>
"""
st.markdown(floating_bg_html, unsafe_allow_html=True)

# ==========================================
# 3. LOCALIZATION DICTIONARIES
# ==========================================
translations = {
    'English': {
        'greeting': 'Hi user, hope you are doing good! 🌟',
        'welcome': 'Welcome to ParkSmart Logistics Core.',
        'description': 'Leveraging state-of-the-art Deep Learning Neural Networks to optimize space utilization, slash transit emission times, and streamline city mobility infrastructure seamlessly.',
        'sidebar_lang_lbl': 'Choose UI & Speech Language',
        'sidebar_model_title': '📦 MODEL INTEGRITY',
        'metric_capacity': 'TOTAL SYSTEM CAPACITY',
        'metric_occupied': 'ACTIVE OCCUPIED',
        'metric_available': 'AVAILABLE LOTS',
        'metric_integrity': 'SYSTEM INTEGRITY',
        'metric_slots': 'Slots',
        'metric_online': 'ONLINE',
        'radar_title': 'VEHICLE GRID RADAR LIVE AUDIT',
        'predict_header': '🔮 Here are your prediction results',
        'upload_prompt': '🔬 Upload Parking Slot Image to Start Real-Time AI Inference Scanning',
        'btn_read': '🔊 Read Aloud Announcement',
        'grid_matrix_caption': 'Uploaded Parking Lot Stream',
        'ai_output_header': 'Artificial Intelligence Diagnostic',
        'decoding_spinner': 'Analyzing parking grid matrices...',
        'available_msg': 'Good news, parking is available! Have a good day.',
        'full_msg': 'Sorry for the inconvenience, but the parking is full. Please search for a nearby place.',
        'back_home': '⬅️ Return to Cockpit Panel',
        'lang_code': 'en'
    },
    'Telugu': {
        'greeting': 'హాయ్ యూజర్, మీరు బాగున్నారని ఆశిస్తున్నాము! 🌟',
        'welcome': 'పార్క్ స్మార్ట్ లాజిస్టిక్స్ కోర్‌కు స్వాగతం.',
        'description': 'పార్कीంగ్ స్థల వినియోగాన్ని ఆప్టిమైజ్ చేయడానికి, వాహన ఉద్గారాల సమయాన్ని తగ్గించడానికి మరియు నగర రవాణా మౌలిక సదుపాయాలను సజావుగా క్రమబద్ధీకరించడానికి స్టేట్-ఆఫ్-ది-ఆర్ట్ డీప్ లెర్నింగ్ న్యూరల్ నెట్‌వర్క్‌లను ఉపయోగించడం.',
        'sidebar_lang_lbl': 'యూజర్ ఇంటర్ఫేస్ & స్పీచ్ భాషను ఎంచుకోండి',
        'sidebar_model_title': '📦 మోడల్ సమగ్రత',
        'metric_capacity': 'మొత్తం సిస్టమ్ సామర్థ్యం',
        'metric_occupied': 'యాక్టివ్ ఆక్యుపైడ్',
        'metric_available': 'అందుబాటులో ఉన్న పార్కింగ్',
        'metric_integrity': 'సిస్టమ్ సమగ్రత',
        'metric_slots': 'స్లాట్లు',
        'metric_online': 'ఆన్‌లైన్',
        'radar_title': 'వాహన గ్రిడ్ రాడార్ లైవ్ ఆడిట్',
        'predict_header': '🔮 ఇక్కడ మీ ప్రిడిక్షన్ ఫలితాలు ఉన్నాయి',
        'upload_prompt': '🔬 నిజ-సమయ AI స్కానింగ్‌ను ప్రారంభించడానికి... ',
        'btn_read': '🔊 బిగ్గరగా చదవండి',
        'grid_matrix_caption': 'అప్‌లోడ్ చేయబడిన పార్కింగ్ లాట్ స్ట్రీమ్',
        'ai_output_header': 'కృత్రిమ మేధస్సు విశ్లేషణ',
        'decoding_spinner': 'పార్కింగ్ గ్రిడ్ మాతృకలను విశ్లేషిస్తోంది...',
        'available_msg': 'శుభవార్త, parking అందుబాటులో ఉంది! మంచి రోజు అవుగాక.',
        'full_msg': 'అసౌకర్యానికి క్షమించండి, పార్కింగ్ నిండిపోయింది. దయచేసి సమీపంలోని స్థలాన్ని వెతకండి.',
        'back_home': '⬅️ కాక్‌పిట్ ప్యానెల్‌కు తిరిగి వెళ్లండి',
        'lang_code': 'te'
    },
    'Tamil': {
        'greeting': 'ஹாய் பயனர், நீங்கள் நலமாக இருக்கிறீர்கள் என்று நம்புகிறேன்! 🌟',
        'welcome': 'பார்க்ஸ்மார்ட் லாஜிஸ்டிக்ஸ் மையத்திற்கு வரவேற்கிறோம்.',
        'description': 'பார்க்கிங் இட பயன்பாட்டை மேம்படுத்தவும், வாகன உமிழ்வு நேரத்தைக் குறைக்கவும் மற்றும் நகர போக்குவரத்து உள்கட்டமைப்பை தடையின்றி சீரமைக்கவும் அதிநவீன ஆழ்ந்த கற்றல் நரம்பியல் நெட்களைப் பயன்படுத்துதல்.',
        'sidebar_lang_lbl': 'UI மற்றும் பேச்சு மொழியைத் தேர்ந்தெடுக்கவும்',
        'sidebar_model_title': '📦 மாதிரி ஒருமைப்பாடு',
        'metric_capacity': 'மொத்த கணினி திறன்',
        'metric_occupied': 'செயலில் உள்ள ஆக்கிரமிப்பு',
        'metric_available': 'கிடைக்கும் இடங்கள்',
        'metric_integrity': 'கணினி ஒருமைப்பாடு',
        'metric_slots': 'இடங்கள்',
        'metric_online': 'ஆன்лайн',
        'radar_title': 'வாகன கிரிட் ரேடார் நேரடி தணிக்கை',
        'predict_header': '🔮 இதோ உங்களுடைய கணிப்பு முடிவுகள்',
        'upload_prompt': '🔬 நிகழ்நேர AI ஸ்கேனிங்கைத் தொடங்க பார்க்கிங் ஸ்லாட் படத்தை இங்கே பதிவேற்றவும்',
        'btn_read': '🔊 சத்தமாக வாசிக்கவும்',
        'grid_matrix_caption': 'பதிவேற்றப்பட்ட பார்க்கிங் பகுதி',
        'ai_output_header': 'செயற்கை நுண்ணறிவு கண்டறிதல்',
        'decoding_spinner': 'பார்க்கிங் கட்டத்தை பகுப்பாய்வு செய்கிறது...',
        'available_msg': 'நல்ல செய்தி, பார்க்கிங் வசதி உள்ளது! இந்த நாள் இனிய நாளாக அமையட்டும்.',
        'full_msg': 'அசவுகரியத்திற்கு மன்னிக்கவும், பார்க்கிங் நிரம்பியுள்ளது. அருகில் உள்ள இடத்தை தேடவும்.',
        'back_home': '⬅️ பிரதான பேனலுக்குத் திரும்பு',
        'lang_code': 'ta'
    },
    'Malayalam': {
        'greeting': 'ഹായ് ഉപയോക്താവേ, സുഖമായിരിക്കുന്നു എന്ന് കരുതുന്നു! 🌟',
        'welcome': 'പാർക്ക്സ്മാർട്ട് ലോജിസ്റ്റിക്സ് കോറിലേക്ക് സ്വാഗതം.',
        'description': 'പാർക്കിംഗ് സ്ഥല വിനിയോഗം ഒപ്റ്റിമൈസ് ചെയ്യുന്നതിനും നഗര ഗതാഗത അടിസ്ഥാന സൗകര്യങ്ങൾ സുഗമമാക്കുന്നതിനും അത്യാധുനിക ഡീപ് ലേണിംഗ് ന്യൂറൽ നെറ്റ്‌വർക്കുകൾ പ്രയോജനപ്പെടുത്തുന്നു.',
        'sidebar_lang_lbl': 'UI-യും സംസാര ഭാഷയും തിരഞ്ഞെടുക്കുക',
        'sidebar_model_title': '📦 മോഡൽ ഇൻ്റഗ്രിറ്റി',
        'metric_capacity': 'ആകെ സിസ്റ്റം കപ്പാസിറ്റി',
        'metric_occupied': 'സജീവമായി ഉപയോഗിക്കുന്നത്',
        'metric_available': 'ലഭ്യമായ പാർക്കിംഗ്',
        'metric_integrity': 'സിസ്റ്റം ഇൻ്റഗ്രിറ്റി',
        'metric_slots': 'സ്ലോട്ടുകൾ',
        'metric_online': 'ഓൺലൈൻ',
        'radar_title': 'വെഹിക്കിൾ ഗ്രിഡ് റഡാർ ലൈവ് ഓഡിറ്റ്',
        'predict_header': '🔮 നിങ്ങളുടെ പ്രവചന ഫലങ്ങൾ ഇതാ',
        'upload_prompt': '🔬 തത്സമയ AI സ്കാനിംഗ് ആരംഭിക്കുന്നതിന് പാർക്കിംഗ് ചിത്രം അപ്‌ലോഡ് ചെയ്യുക',
        'btn_read': '🔊 ഉറക്കെ വായിക്കുക',
        'grid_matrix_caption': 'അപ്‌ലോഡ് ചെയ്‌ത പാർക്കിംഗ് ചിത്രം',
        'ai_output_header': 'ആർട്ടിഫിഷ്യൽ ഇൻ്റലിജൻസ് ഡയഗ്നോസ്റ്റിക്',
        'decoding_spinner': 'പാർക്കിംഗ് ഗ്രിഡ് വിശകലനം ചെയ്യുന്നു...',
        'available_msg': 'നല്ല വാർത്ത,amp; പാർക്കിംഗ് ലഭ്യമാണ്! ഒരു നല്ല ദിവസം ആശംസിക്കുന്നു.',
        'full_msg': 'അസൗകര്യത്തിൽ ഖേദിക്കുന്നു, പാർക്കിംഗ് ഫുൾ ആണ്. ദയവായി അടുത്തുള്ള സ്ഥലം തിരയുക.',
        'back_home': '⬅️ പ്രധാന പാനലിലേക്ക് മടങ്ങുക',
        'lang_code': 'ml'
    },
    'Hindi': {
        'greeting': 'हाय यूजर, आशा है कि आप अच्छे होंगे! 🌟',
        'welcome': 'पार्कस्मार्ट लॉजिस्टिक्स कोर में आपका स्वागत है।',
        'description': 'पार्किंग स्थान के उपयोग को अनुकूलित करने, वाहन उत्सर्जन समय को कम करने और शहर के परिवहन बुनियादी ढांचे को सुचारू रूप से सुव्यवस्थित करने के लिए अत्याधुनिक डीप लर्निंग न्यूरल नेटवर्क का उपयोग करना।',
        'sidebar_lang_lbl': 'यूजर इंटरफेस और भाषण भाषा चुनें',
        'sidebar_model_title': '📦 MODEL INTEGRITY',
        'metric_capacity': 'कुल सिस्टम क्षमता',
        'metric_occupied': 'सक्रिय कब्जे वाले स्लॉट',
        'metric_available': 'उपलब्ध पार्किंग स्लॉट',
        'metric_integrity': 'सिस्टम सत्यता',
        'metric_slots': 'स्लॉट',
        'metric_online': 'ONLINE',
        'radar_title': 'वाहन ग्रिड रडार लाइव ऑडिट',
        'predict_header': '🔮 यहाँ आपके परिणाम दिए गए हैं',
        'upload_prompt': '🔬 रीयल-टाइम AI स्कैन शुरू करने के लिए पार्किंग स्लॉट छवि अपलोड करें',
        'btn_read': '🔊 बोलकर सुनाएं',
        'grid_matrix_caption': 'अपलोड की गई पार्किंग लॉट स्ट्रीम',
        'ai_output_header': 'कृत्रिम बुद्धिमत्ता निदान',
        'decoding_spinner': 'पार्किंग ग्रिड मैट्रिसेस का विश्लेषण किया जा रहा है...',
        'available_msg': 'अच्छी खबर है, पार्किंग उपलब्ध है! आपका दिन शुभ हो।',
        'full_msg': 'असुविधा के लिए खेद है, लेकिन पार्किंग भरी हुई है। कृपया पास की किसी जगह पर तलाश करें।',
        'back_home': '⬅️ कॉकपिट पैनल पर वापस जाएं',
        'lang_code': 'hi'
    }
}

# ==========================================
# 4. INTERACTIVE SPEECH AUDIO UTILITIES
# ==========================================
def text_to_speech_autoplay(text, lang_code):
    try:
        tts = gTTS(text=text, lang=lang_code, slow=False)
        b64_buffer = io.BytesIO()
        tts.write_to_fp(b64_buffer)
        b64_buffer.seek(0)
        b64 = base64.b64encode(b64_buffer.read()).decode()
        md = f'<audio autoplay><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>'
        st.markdown(md, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Audio Feedback Error: {e}")

@st.cache_resource
def load_parking_model():
    try:
        return tf.keras.models.load_model("new_smart_parking_cnn.h5")
    except Exception as e:
        st.error(f"Model Error: {e}")
        return None

# ==========================================
# 5. SIDEBAR BRAND ASSEMBLY
# ==========================================
with st.sidebar:
    st.markdown("""
        <div class="logo-container">
            <div class="brand-title-line1">PARK</div>
            <div class="brand-title-line2">SMART</div>
            <div class="brand-subtitle">INTELLIGENT EDGE</div>
        </div>
    """, unsafe_allow_html=True)
    
    selected_lang = st.selectbox(translations['English']['sidebar_lang_lbl'], list(translations.keys()))
    t = translations[selected_lang]
    st.markdown("---")
    st.markdown(f"### {t['sidebar_model_title']}")
    st.markdown('<div class="file-badge" style="background: rgba(59, 130, 246, 0.2); padding: 8px; border-radius: 8px; text-align: center; border: 1px solid #3b82f6;">new_smart_parking_cnn.h5</div>', unsafe_allow_html=True)

# ==========================================
# 6. FILE INTERACTION SCHEDULER
# ==========================================
uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"], key="master_uploader", label_visibility="collapsed")

if uploaded_file is not None:
    # --------------------------------------
    # IMMEDIATE PREDICTION RESULT STAGE
    # Clean styled text on screen, without the layout box bounding frames
    # --------------------------------------
    # High-visibility simple title text replacement
    st.markdown(f"<h2 style='text-align: center; font-family: \"Orbitron\", sans-serif; font-weight: 900; background: linear-gradient(45deg, #3b82f6, #ec4899); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 30px;'>{t['predict_header']}</h2>", unsafe_allow_html=True)
    
    img_col, pred_col = st.columns([1, 1])
    
    
    with img_col:
        image = Image.open(uploaded_file)
        st.image(image, use_container_width=True, caption=t['grid_matrix_caption'])
        
    with pred_col:
        st.markdown(f"### {t['ai_output_header']}")
        
        with st.spinner(t['decoding_spinner']):
            model = load_parking_model()
            if model is not None:
                try:
                    input_shape = model.input_shape
                    img_height = input_shape[1] if (len(input_shape) == 4 and input_shape[1] is not None) else 150
                    img_width = input_shape[2] if (len(input_shape) == 4 and input_shape[2] is not None) else 150
                except:
                    img_height, img_width = 150, 150
                    
                image = image.convert('RGB')
                img_resized = image.resize((img_width, img_height))
                img_array = np.asarray(img_resized, dtype=np.float32)
                
                # Image normalization
                img_array = img_array / 255.0
                img_array = np.expand_dims(img_array, axis=0)
                
                prediction = model.predict(img_array, verbose=0)
                prediction_value = float(prediction[0][0])
                
                # Dynamic model threshold classification logic
                is_available = prediction_value > 0.5
                
                if is_available:
                    st.markdown(f"""
                        <div class="result-card-available">
                            <div class="result-text-main" style="color: #34d399;">✅ SPACES AVAILABLE</div>
                            <div class="result-text-sub">{t['available_msg']}</div>
                        </div>
                    """, unsafe_allow_html=True)
                    speech_text = t['available_msg']
                else:
                    st.markdown(f"""
                        <div class="result-card-full">
                            <div class="result-text-main" style="color: #f87171;">⚠️ PARKING FULL</div>
                            <div class="result-text-sub">{t['full_msg']}</div>
                        </div>
                    """, unsafe_allow_html=True)
                    speech_text = t['full_msg']
                
                st.markdown("<br>", unsafe_allow_html=True)
                
               # Action Execution Row: both items fully visible and side-by-side
                btn_col1, btn_col2 = st.columns([1, 1])
                with btn_col1:
                    if st.button(t['btn_read'], use_container_width=True):
                        text_to_speech_autoplay(speech_text, t['lang_code'])
                with btn_col2:
                    if st.button(t['back_home'], use_container_width=True):
                        st.rerun()

else:
    # --------------------------------------
    # DEFAULT LANDING SCREEN COCKPIT VIEW
    # --------------------------------------
    st.markdown(f"""
        <div style="margin-bottom: 25px; text-align: center;">
            <h1 style="font-family: 'Orbitron', sans-serif; font-weight: 900; background: linear-gradient(45deg, #3b82f6, #a78bfa, #f472b6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 3.2rem;">
                PARKSMART CONTROL SYSTEMS
            </h1>
            <p style="color: #94a3b8; font-size: 1.2rem; max-width: 800px; margin: 0 auto 35px auto;">
                {t['description']}
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Grid Status Board Indicators
    m_col1, m_col2, m_col3 = st.columns(3)
    with m_col1:
        st.markdown(f"""
            <div class="metric-card" style="border-top: 4px solid #3b82f6;">
                <div class="metric-lbl" style="color: #3b82f6;">{t['metric_capacity']}</div>
                <div class="metric-val">150 <span style="font-size:1.2rem; color:#64748b;">{t['metric_slots']}</span></div>
            </div>
        """, unsafe_allow_html=True)
    with m_col2:
        st.markdown(f"""
            <div class="metric-card" style="border-top: 4px solid #ec4899;">
                <div class="metric-lbl" style="color: #ec4899;">{t['metric_integrity']}</div>
                <div class="metric-val">99.4% <span style="font-size:1.2rem; color:#64748b;">{t['metric_online']}</span></div>
            </div>
        """, unsafe_allow_html=True)
    with m_col3:
        st.markdown(f"""
            <div class="metric-card" style="border-top: 4px solid #10b981;">
                <div class="metric-lbl" style="color: #10b981;">{t['radar_title']}</div>
                <div class="metric-val" style="color: #10b981; font-size: 1.5rem; padding: 12px 0;">● ACTIVE SCANNING</div>
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align:center; font-family:\"Orbitron\", sans-serif; letter-spacing:2px; font-size:1.1rem; color:#3b82f6; margin-bottom:15px;'>{t['upload_prompt']}</h3>", unsafe_allow_html=True)