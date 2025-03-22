from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp
import re

app = Flask(__name__)
CORS(app)

# ✅ Function to Convert Short URL to Long URL
def clean_youtube_url(url):
    match = re.match(r"https://youtu\.be/([a-zA-Z0-9_-]+)", url)
    if match:
        video_id = match.group(1)
        return f"https://www.youtube.com/watch?v={video_id}"
    return url

@app.route('/download', methods=['GET'])
def download():
    video_url = request.args.get('url')

    if not video_url:
        return jsonify({"error": "YouTube URL required!"}), 400
    
    # ✅ Convert Short URL to Full URL
    video_url = clean_youtube_url(video_url)

    # ✅ yt-dlp Options for MP4 & MP3
    ydl_opts_video = {
        'format': 'best[ext=mp4]',  # High-quality MP4
        'quiet': True,
        'noplaylist': True
    }
    ydl_opts_audio = {
        'format': 'bestaudio/best',  # High-quality MP3
        'quiet': True,
        'noplaylist': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }]
    }

    # ✅ Download URL Fetching
    with yt_dlp.YoutubeDL(ydl_opts_video) as ydl:
        video_info = ydl.extract_info(video_url, download=False)
        video_link = video_info['url']
    
    with yt_dlp.YoutubeDL(ydl_opts_audio) as ydl:
        audio_info = ydl.extract_info(video_url, download=False)
        audio_link = audio_info['url']

    return jsonify({
        "title": video_info['title'],
        "thumbnail": video_info['thumbnail'],
        "mp4": video_link,
        "mp3": audio_link
    })

if __name__ == '__main__':
    app.run(debug=True)
