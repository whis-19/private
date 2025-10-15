import streamlit as st
import time
import base64
import streamlit.components.v1 as components

# --- Page Setup ---
st.set_page_config(page_title="Morning Aimen 💖", page_icon="☀️", layout="centered")

# --- Custom CSS ---
st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #ffe6eb, #ffd1dc);
        font-family: 'Poppins', sans-serif;
        color: #6a1b9a;
        text-align: center;
    }
    .title {
        font-size: 40px;
        font-weight: 700;
        color: #ad1457;
        text-shadow: 1px 1px 3px #fff;
    }
    .lyrics {
        font-size: 24px;
        color: #6a1b9a;
        margin-top: 30px;
        text-shadow: 1px 1px 3px #fff;
        transition: opacity 1s ease-in-out;
    }
    audio {
        display: none; /* Hide player controls */
    }
    </style>
""", unsafe_allow_html=True)

# --- UI ---
st.markdown("<div class='title'>☀️ Good Morning, Beautiful ladiez 💕</div>", unsafe_allow_html=True)
st.write("Click the button to start from your favorite part 🎶")

# --- Lyrics synced with 2:26 → 2:44 (18s window) ---
lyrics = [
    ("Maybe it's 6:45 🌅", 3),
    ("Maybe I'm barely alive 💭", 2),
    ("Maybe you've taken my heart for the last time, yeah 💘", 3),
    ("Maybe I know that I'm yours 💫", 3),
    ("Maybe I know you're the one 💎", 2),
    ("Maybe you're thinking it's better if we drive 🚗💨", 3),
    ("Oh, 'cause girls like you 💕", 2),
    ("Make the world so much brighter 🌍✨", 6),
    ("I need a girl like you, yeah 💞", 5)
]

# --- Button ---
if st.button("💖 Click to Make Your Day Beautiful 💖"):
    # --- Load and Encode Music ---
    with open("song.mp3", "rb") as f:
        audio_bytes = f.read()
        b64 = base64.b64encode(audio_bytes).decode()

    # --- HTML/JS Component (with fade-out logic) ---
    audio_html = f"""
        <audio id="loveAudio" autoplay>
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
        <script>
            const audio = document.getElementById('loveAudio');
            audio.volume = 1.0;
            const fadeStart = 162;  // start fade at 2:42 (3s before stop)
            const stopTime = 165;   // stop at 2:45

            audio.addEventListener('loadedmetadata', () => {{
                audio.currentTime = 146; // Start at 2:26
                audio.play();
            }});

            const checkInterval = setInterval(() => {{
                if (audio.currentTime >= fadeStart && audio.currentTime < stopTime) {{
                    // Gradually lower volume
                    const remaining = stopTime - audio.currentTime;
                    audio.volume = Math.max(0, remaining / 3);
                }}
                if (audio.currentTime >= stopTime) {{
                    audio.pause();
                    audio.currentTime = stopTime;
                    audio.volume = 1.0;
                    clearInterval(checkInterval);
                }}
            }}, 200);
        </script>
    """
    components.html(audio_html, height=0)

    # --- Show Synced Lyrics ---
    placeholder = st.empty()
    time.sleep(1.5)  # Small delay for music start

    for line, delay in lyrics:
        placeholder.markdown(f"<div class='lyrics'>{line}</div>", unsafe_allow_html=True)
        time.sleep(delay)

    st.success("💐 Hope your day starts with a smile 💐")

