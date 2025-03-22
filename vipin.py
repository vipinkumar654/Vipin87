from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

# Download Folder
DOWNLOAD_FOLDER = "downloads"
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# Cookies file ka path
COOKIES_FILE = "cookies.txt"  # Is file ko apne browser se export karein

@app.route('/download', methods=['GET'])
def download_video():
    url = request.args.get('url')

    if not url:
        return jsonify({"error": "Please provide a YouTube URL"}), 400

    try:
        ydl_opts = {
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
            'format': 'bestvideo+bestaudio/best',
            'cookiefile': COOKIES_FILE  # Cookies ka support add kiya
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        return jsonify({
            "message": "Download successful",
            "title": info.get('title', 'Unknown'),
            "filename": os.path.basename(filename)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0')
