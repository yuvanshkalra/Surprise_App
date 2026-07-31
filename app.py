import streamlit as st
import base64
import os

# --- Helper Function for Images ---
def get_image_src(path):
    """Converts local images to base64 so they can render in custom HTML, or returns the URL."""
    if path.startswith("http://") or path.startswith("https://"):
        return path
    try:
        with open(path, "rb") as img_file:
            return f"data:image/jpeg;base64,{base64.b64encode(img_file.read()).decode()}"
    except Exception as e:
        return "" 

# --- Helper Function for Audio ---
def get_audio_base64(path):
    """Converts local audio to base64 so it can play in the custom HTML player."""
    try:
        with open(path, "rb") as audio_file:
            return f"data:audio/mp3;base64,{base64.b64encode(audio_file.read()).decode()}"
    except Exception as e:
        return ""

# 1. Configure the page 
st.set_page_config(page_title="For You", page_icon="❤️", layout="wide")

# 2. Define structured floating stickers
stickers_data = [
    ("💖", "5%", "0s", "9s"), ("✨", "15%", "2s", "11s"), ("🧸", "25%", "4s", "8s"),
    ("💌", "35%", "1s", "10s"), ("🌸", "45%", "5s", "12s"), ("🎀", "55%", "3s", "9s"),
    ("💕", "65%", "0.5s", "11s"), ("🦋", "75%", "2.5s", "8s"), ("🌷", "85%", "4.5s", "10s"),
    ("🍓", "95%", "1.5s", "12s"), ("💘", "10%", "6s", "9s"), ("🌻", "30%", "7s", "10s"),
    ("💝", "50%", "6.5s", "8s"), ("🎂", "70%", "7.5s", "11s"), ("💗", "90%", "5.5s", "9s"),
]

html_stickers = ""
for i, (emoji, left_pos, delay, duration) in enumerate(stickers_data):
    html_stickers += f'<div class="floating-sticker" style="left: {left_pos}; animation-delay: {delay}; animation-duration: {duration};">{emoji}</div>\n'

# 3. Inject GLOBAL Custom CSS (Applies everywhere)
page_style = f"""
<style>
.block-container {{
    padding-top: 2rem !important;
    padding-bottom: 1rem !important;
}}
[data-testid="stAppViewContainer"] {{
    background-image: url("https://images.unsplash.com/photo-1518199266791-5375a83190b7?q=80&w=2000&auto=format&fit=crop");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}}
[data-testid="stHeader"] {{
    background: rgba(0,0,0,0);
}}
.stApp {{
    background-color: rgba(0, 0, 0, 0.45); 
}}
h1, h2, h3, p, .stMarkdown, label {{
    color: white !important; 
}}
h1, h2, label, .center-text {{
    text-align: center !important;
}}
.stButton {{
    display: flex !important;
    justify-content: center !important;
    width: 100% !important;
    margin-top: 15px !important;
}}
.stButton > button {{
    background-color: #FF69B4 !important; 
    color: white !important;
    border-radius: 20px;
    border: none;
    padding: 10px 24px;
    font-weight: bold;
    font-size: 1rem;
    box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    transition: all 0.3s ease;
    display: block;
    margin: 0 auto;
}}
.stButton > button:hover {{
    background-color: #ff4d94 !important;
    transform: translateY(-2px);
}}
.floating-sticker {{
    position: fixed;
    font-size: 4rem; 
    z-index: 0; 
    pointer-events: none; 
    animation-name: floatUp;
    animation-iteration-count: infinite;
    animation-timing-function: ease-in-out;
    bottom: -15vh;
}}
@keyframes floatUp {{
    0% {{ transform: translateY(0) rotate(0deg); opacity: 0; }}
    15% {{ opacity: 0.9; }}
    85% {{ opacity: 0.9; }}
    100% {{ transform: translateY(-115vh) rotate(360deg); opacity: 0; }}
}}
</style>
{html_stickers}
"""
st.markdown(page_style, unsafe_allow_html=True)

# 4. Secret Password Configuration 
SECRET_PASSWORD = "26march2026"

if 'unlocked' not in st.session_state:
    st.session_state.unlocked = False

def check_password():
    if st.session_state.pwd_input.strip().lower() == SECRET_PASSWORD.lower():
        st.session_state.unlocked = True
    else:
        st.error("Write the complete Date without spaces. 😉")

# 5. Application Logic
if not st.session_state.unlocked:
    # --- LOCK SCREEN CSS (Only active when locked) ---
    lock_screen_css = """
    <style>
    /* Force the main container to push down and center vertically & horizontally */
    .block-container {
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        align-items: center !important;
        min-height: 95vh !important;
        padding-top: 4rem !important; 
    }

    /* Target the center column card */
    div[data-testid="stColumn"]:nth-of-type(2) {
        background-image: url("https://images.unsplash.com/photo-1518381533037-12fb189670f3?q=80&w=800&auto=format&fit=crop"); 
        background-size: cover;
        background-position: center;
        padding: 50px 40px;
        border-radius: 20px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.6);
        border: 4px double #FF69B4; 
        position: relative;
        overflow: hidden;
    }

    /* Add a dark tint inside the card */
    div[data-testid="stColumn"]:nth-of-type(2)::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: rgba(0, 0, 0, 0.4); 
        border-radius: 15px; 
        z-index: 0;
    }

    /* Ensure the text and inputs float above the dark tint */
    div[data-testid="stColumn"]:nth-of-type(2) > div {
        position: relative;
        z-index: 1;
    }
    
    /* Input field styling */
    div[data-baseweb="input"] {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px;
    }
    input {
        color: white !important;
    }
    </style>
    """
    st.markdown(lock_screen_css, unsafe_allow_html=True)
    
    # --- LOCK SCREEN LAYOUT ---
    col1, col2, col3 = st.columns([1, 1.2, 1])
    
    with col2:
        st.markdown("<h1>A Secret Gateway</h1>", unsafe_allow_html=True)
        st.write("<p class='center-text'>Enter the password to unlock the Girlfriend's Day Surprise.</p>", unsafe_allow_html=True)
        
        st.text_input("The Day we made it Official", key="pwd_input", type="password", on_change=check_password)
        st.button("Unlock", on_click=check_password)

else:
    # --- UNLOCKED LANDING PAGE CSS ---
    landing_page_css = """
    <style>
    /* Turn both columns into beautifully framed cards */
    div[data-testid="stColumn"] {
        background-image: url("https://images.unsplash.com/photo-1518381533037-12fb189670f3?q=80&w=800&auto=format&fit=crop"); 
        background-size: cover;
        background-position: center;
        padding: 40px 30px;
        border-radius: 20px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.6);
        border: 4px double #FF69B4; 
        position: relative;
        overflow: hidden;
    }

    /* Add the dark tint inside the columns */
    div[data-testid="stColumn"]::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: rgba(0, 0, 0, 0.4); 
        border-radius: 15px; 
        z-index: 0;
    }

    /* Ensure the text and content float above the dark tint */
    div[data-testid="stColumn"] > div {
        position: relative;
        z-index: 1;
    }
    
    /* Neon LED Glow Effect for the Main Header */
    .neon-glow {
        color: #ff3333 !important; 
        text-shadow: 
            0 0 5px #ff0000, 
            0 0 10px #ff0000, 
            0 0 20px #ff0000, 
            0 0 40px #ff0000, 
            0 0 80px #ff0000;
        text-align: center;
        font-weight: bold;
    }
    </style>
    """
    st.markdown(landing_page_css, unsafe_allow_html=True)

    # --- UNLOCKED LANDING PAGE ---
    st.balloons()
    
    # Background Music Player (Hidden and Autoplaying from local file)
    audio_path = "audio.mp3"
    audio_src = get_audio_base64(audio_path)
    
    if audio_src:
        audio_html = f"""
        <audio autoplay loop style="display:none;">
            <source src="{audio_src}" type="audio/mp3">
        </audio>
        """
        st.markdown(audio_html, unsafe_allow_html=True)
    
    st.markdown("<h1 class='neon-glow'>Happy Girlfriend's Day! ❤️</h1>", unsafe_allow_html=True)
    st.write("<br>", unsafe_allow_html=True) 
    
    col_left, col_right = st.columns([1.2, 1], gap="large")
    
    with col_left:
        st.markdown("""
        ### You crack the code to my heart.

        Mansi, Mansi, Mansi, My love....... 
        
        I wanted to take a moment today to tell you just how incredibly special you are to me. From the very beginning, I was completely captivated by you. You are absolutely stunning, inside and out, but I could honestly get lost in your eyes forever. Just looking at you makes my heart race, and I still can't believe how lucky I am to have someone as beautiful as you by my side.
        
        But it is not just your beauty that leaves me in awe; it is your incredible drive. Your ambition is so inspiring to watch. Seeing how passionate and determined you are to reach your goals motivates me every single day. You push me to be a better version of myself, to work harder on my own dreams, and to aim higher. I appreciate that about you more than words can say.

        I would have never thought that I'll be dating someone like you ever in my life. I decided a long time ago that I am unworthy of love but you crashed into my life like a meteor and caused a chaos in my life which I adore every single day of my life. I am genuinely lucky to have a beautiful, caring, smart, intelligent and ambitious girl in my life and I hope to spend my life with you love.
        
        What I cherish most of all, though, is the way you love me. The care and affection you pour into our relationship makes me feel so incredibly safe. You have this amazing ability to make me feel deeply wanted and unconditionally loved, and that is a feeling I will never take for granted. Knowing that I have your love and support means everything to me.
        
        I love you so much. Thank you for being the most amazing girlfriend, for taking care of me, and for just being you. I can't wait to see what the future holds for us.
        
        Forever yours,  
        Yuvansh
        """)
        
    with col_right:
        st.markdown("<h3 style='text-align: center;'> Our Memories</h3>", unsafe_allow_html=True)
        
        # --- AUTO-SCROLLING MEMORY GALLERY ---
        image_list = []
        folder_path = "Images" 
        
        # Check if the folder exists and grab all the images dynamically
        if os.path.exists(folder_path):
            valid_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.webp')
            for filename in os.listdir(folder_path):
                if filename.lower().endswith(valid_extensions):
                    image_list.append(os.path.join(folder_path, filename))
        
        # Fallback just in case the folder is empty or missing
        if not image_list:
            image_list = [
                "https://images.unsplash.com/photo-1516589178581-6cd7833ae3b2?q=80&w=800&auto=format&fit=crop",
                "https://images.unsplash.com/photo-1522673607200-164d1b6ce486?q=80&w=800&auto=format&fit=crop"
            ]
        
        img_tags = ""
        for img_path in image_list:
            src = get_image_src(img_path)
            if src:
                img_tags += f'<img src="{src}" style="width:100%; border-radius:15px; margin-bottom: 20px; box-shadow: 0 4px 8px rgba(0,0,0,0.4);">'
        
        # Slower scrolling animation (60s)
        scroll_html = f"""
        <div style="height: 500px; overflow: hidden; position: relative; border-radius: 15px; padding: 10px;">
            <div style="animation: scrollUp 60s linear infinite; display: flex; flex-direction: column;">
                {img_tags}
                {img_tags}
            </div>
        </div>
        <style>
        @keyframes scrollUp {{
            0% {{ transform: translateY(0); }}
            100% {{ transform: translateY(-50%); }} 
        }}
        </style>
        """
        st.markdown(scroll_html, unsafe_allow_html=True)
