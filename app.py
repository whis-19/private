import streamlit as st
import time
import requests
import base64
import streamlit.components.v1 as components

# --- Page Setup ---
st.set_page_config(
    page_title="Morning Aimen 💖",
    page_icon="☀️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- Light Theme + Aesthetic CSS ---
st.markdown("""
    <style>
    :root {
        color-scheme: only light;
    }
    html, body, [class*="css"] {
        background: linear-gradient(135deg, #ffe6eb, #ffd1dc) !important;
        font-family: 'Poppins', sans-serif !important;
        color: #6a1b9a !important;
        text-align: center !important;
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

# --- Step 1: Fetch and Buffer the Song ---
github_audio_url = "https://raw.githubusercontent.com/whis-19/private/main/song.mp3"

with st.spinner("🎵 Loading your favorite part... please wait 💖"):
    try:
        response = requests.get(github_audio_url)
        if response.status_code == 200:
            audio_bytes = response.content
            b64 = base64.b64encode(audio_bytes).decode()
            audio_source = f"data:audio/mp3;base64,{b64}"
            time.sleep(1)  # small wait for effect
        else:
            st.error("❌ Could not load the song from GitHub.")
            st.stop()
    except Exception as e:
        st.error(f"⚠️ Error loading song: {e}")
        st.stop()

# --- Step 2: Show the Main Page After Buffering ---
st.markdown("<div class='title'>☀️ Good Morning, Beautiful ladiez 💕</div>", unsafe_allow_html=True)
st.write("Click the button to start from your favorite part 🎶")

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

# --- Step 3: Play Music and Show Lyrics ---

# Containers so we can replace the audio iframe and lyrics display without
# leaving multiple audio elements playing at once.
audio_container = st.empty()
lyrics_placeholder = st.empty()

# Track play count so "Replay" knows whether there's something to restart.
if 'play_count' not in st.session_state:
    st.session_state['play_count'] = 0

def render_audio(container):
    """Embed the hidden audio player into the given Streamlit container.
    Replacing the content of the same container stops any previous audio iframe.
    """
    audio_html = f"""
        <audio id="loveAudio" autoplay>
            <source src="{audio_source}" type="audio/mp3">
        </audio>
        <script>
            const audio = document.getElementById('loveAudio');
            audio.volume = 1.0;
            const fadeStart = 162;  // start fade at 2:42
            const stopTime = 165;   // stop at 2:45

            audio.addEventListener('loadedmetadata', () => {{
                audio.currentTime = 146; // Start at 2:26
                audio.play();
            }});

            const checkInterval = setInterval(() => {{
                if (audio.currentTime >= fadeStart && audio.currentTime < stopTime) {{
                    const remaining = stopTime - audio.currentTime;
                    audio.volume = Math.max(0, remaining / 3);
                }}
                if (audio.currentTime >= stopTime) {{
                    audio.pause();
                    clearInterval(checkInterval);
                }}
            }}, 200);
        </script>
    """
    container.html(audio_html, height=0)

def play_sequence():
    # increment so replay is allowed after first play
    st.session_state['play_count'] += 1
    # render (or replace) the audio iframe
    render_audio(audio_container)

    # --- Display Lyrics Synced ---
    lyrics_placeholder.empty()
    time.sleep(1.5)  # Give song time to start

    for line, delay in lyrics:
        lyrics_placeholder.markdown(f"<div class='lyrics'>{line}</div>", unsafe_allow_html=True)
        time.sleep(delay)

    st.success("💐 Hope your day starts with a smile 💐")

# Two-button UI: Play and Replay. Replay restarts the audio and lyrics by
# reusing the same audio container (so previous audio iframe is removed).
col1, col2 = st.columns(2)
play_clicked = col1.button("💖 Click to Make Your Day Beautiful 💖")
replay_clicked = col2.button("🔁 Replay")

if play_clicked:
    play_sequence()
elif replay_clicked:
    if st.session_state.get('play_count', 0) > 0:
        play_sequence()
    else:
        st.info("Press the Play button first to start the song, then use Replay.")
