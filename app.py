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
    /* Try to load a decorative 'Venter' font (if available) via Google Fonts; if not, fall back */
    @import url('https://fonts.googleapis.com/css2?family=Varela+Round&display=swap');

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
        /* Use 'Venter' if installed; otherwise use a decorative fallback from Google Fonts */
        font-family: 'Venter', 'Varela Round', 'Poppins', sans-serif;
        font-size: 32px;
        font-style: italic;
        color: #6a1b9a;
        margin: 0;
        text-shadow: 1px 1px 6px #fff;
        transition: opacity 0.5s ease-in-out;
        line-height: 1.2;
        font-weight: 600;
        letter-spacing: 0.5px;
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
    # Pass the lyrics array into the client-side script so the lyrics only start
    # when the audio actually begins playing (handles autoplay-blocked cases).
    # The lyrics will be displayed inside the same HTML container.
    js_lyrics = '[' + ','.join([f'{{text: "{line}", delay: {delay}}}' for line, delay in lyrics]) + ']'

    audio_html = f"""
        <div id="lyricsContainer" style="height:300px; display:flex; align-items:center; justify-content:center; margin-top:20px;">
            <div style="text-align:center; width:100%;">
                <div id="lyrics" class="lyrics" style="opacity:0; transform:translateY(0);"></div>
                <div id="finishedMessage" style="margin-top:12px; font-size:20px; color:#4a148c;"></div>
            </div>
        </div>
        <audio id="loveAudio" preload="auto">
            <source src="{audio_source}" type="audio/mp3">
        </audio>
        <script>
            const audio = document.getElementById('loveAudio');
            const lyricsEl = document.getElementById('lyrics');
            const finishedEl = document.getElementById('finishedMessage');
            audio.volume = 1.0;
            const fadeStart = 162;  // start fade at 2:42
            const stopTime = 165;   // stop at 2:45
            const startAt = 146;    // start at 2:26
            const lyrics = {js_lyrics};

            // Reset UI
            lyricsEl.innerHTML = '';
            lyricsEl.style.opacity = 0;
            finishedEl.innerHTML = '';

            audio.addEventListener('loadedmetadata', () => {{
                try {{ audio.currentTime = startAt; }} catch(e) {{ /* ignore */ }}
            }});

            // Only start the lyric timeline once the audio is actually playing.
            audio.addEventListener('playing', async () => {{
                // small delay to match previous behavior
                await new Promise(r => setTimeout(r, 1500));

                for (const item of lyrics) {{
                    lyricsEl.innerHTML = item.text;
                    lyricsEl.style.opacity = 1;
                    await new Promise(r => setTimeout(r, item.delay * 1000));
                }}

                finishedEl.innerHTML = '💐 Hope your day starts with a smile 💐';
            }});

            // Fade out and stop near the end (same logic as before)
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

            // Try to play immediately; if browser blocks autoplay, lyrics won't start
            // because the 'playing' event never fires until user interaction.
            audio.play().catch(() => {{ /* autoplay blocked; waiting for user interaction */ }});
        </script>
    """
    # Clear the given container and render the HTML inside it. Using a
    # placeholder (returned by container.empty()) and a with-block ensures
    # the component is inserted into the same location and replaces any
    # previous audio element, avoiding overlaps.
    placeholder = container.empty()
    with placeholder:
        components.html(audio_html, height=150, scrolling=False)

def play_sequence():
    # increment so replay is allowed after first play
    st.session_state['play_count'] += 1
    # render (or replace) the audio iframe
    render_audio(audio_container)
    # Clear any previous server-side lyrics UI (client-side will handle lyrics)
    lyrics_placeholder.empty()

# Two-button UI: Play and Replay. Replay restarts the audio and lyrics by
# reusing the same audio container (so previous audio iframe is removed).
col1, col2 = st.columns(2)
play_clicked = col1.button("💖 Click to Make Your Day Beautiful 💖")
# separate plain-text Replay button as requested
replay_clicked = col2.button("Replay")

if play_clicked:
    play_sequence()
elif replay_clicked:
    if st.session_state.get('play_count', 0) > 0:
        play_sequence()
    else:
        st.info("Press the Play button first to start the song, then use Replay.")
