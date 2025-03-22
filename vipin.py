from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp
import os

app = Flask(__name__)
CORS(app)  # Fix CORS Error

COOKIES_FILE = "cookies.txt"

@app.route('/download', methods=['GET'])
def download():
    video_url = request.args.get('url')
    download_type = request.args.get('type', 'video')  # Default: Video

    if not video_url:
        return jsonify({"error": "YouTube URL required!"}), 400

    format_option = "bestaudio/best" if download_type == "audio" else "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]"

    try:
        ydl_opts = {
            'format': format_option,
            'cookiefile': COOKIES_FILE,
            'merge_output_format': 'mp4',
            'postprocessors': [{'key': 'FFmpegVideoConvertor', 'preferedformat': 'mp4'}]
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            formats = info.get("formats", [])
            video_url = next((f.get("url") for f in formats if f.get("ext") == "mp4" and f.get("vcodec") != "none"), None)

            if not video_url:
                return jsonify({"error": "Failed to extract video link"}), 500

            return jsonify({
                "title": info.get("title", "Unknown Title"),
                "thumbnail": info.get("thumbnail", ""),
                "duration": info.get("duration", 0),
                "download_url": video_url
            })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ⚡ Correct Port Handling for Deployment
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))  # Render/Heroku ke liye port 8080
    app.run(host='0.0.0.0', port=port)
