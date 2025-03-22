from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp
import os
import threading
import time

app = Flask(__name__)
CORS(app)

COOKIES_FILE = "youtube.com_cookies.txt"

# ✅ Auto-Update YouTube Cookies Every 12 Hours
def update_cookies():
    while True:
        print("Updating YouTube cookies...")
        os.system('yt-dlp --cookies-from-browser chrome -o "youtube.com_cookies.txt"')
        print("Cookies updated successfully!")
        time.sleep(43200)  # 12 hours = 43200 seconds

# Run cookies updater in the background
threading.Thread(target=update_cookies, daemon=True).start()

@app.route('/download', methods=['GET'])
def download():
    video_url = request.args.get('url')

    # ✅ Check if URL is provided
    if not video_url:
        return jsonify({"error": "YouTube URL required!"}), 400
    
    print(f"Downloading video from: {video_url}")  # Debugging ke liye

    # ✅ High-Quality MP4 (1080p ya best available)
    ydl_opts_video = {
        'format': 'bestvideo[height<=1080]+bestaudio/best',
        'quiet': False,
        'noplaylist': True,
        'cookiefile': COOKIES_FILE
    }
    
    # ✅ High-Quality MP3 (Best Audio Available)
    ydl_opts_audio = {
        'format': 'bestaudio[ext=m4a]/bestaudio',
        'quiet': False,
        'noplaylist': True,
        'cookiefile': COOKIES_FILE,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }]
    }

    try:
        # 🎥 MP4 Link Fetch Karega
        with yt_dlp.YoutubeDL(ydl_opts_video) as ydl:
            info_video = ydl.extract_info(video_url, download=False)
            video_link = info_video.get('url')

        # 🎵 MP3 Link Fetch Karega
        with yt_dlp.YoutubeDL(ydl_opts_audio) as ydl:
            info_audio = ydl.extract_info(video_url, download=False)
            audio_link = info_audio.get('url')
        
        return jsonify({
            "title": info_video.get("title"),
            "thumbnail": info_video.get("thumbnail"),
            "mp4": video_link,  # 🎥 High-Quality Video
            "mp3": audio_link   # 🎵 High-Quality Audio
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
