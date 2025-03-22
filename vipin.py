from flask import Flask, request, jsonify, send_from_directory
import yt_dlp
import os

app = Flask(__name__)

# Download Folder (Public Access)
DOWNLOAD_FOLDER = "downloads"
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# Cookies file (Agar required ho)
COOKIES_FILE = "cookies.txt"

@app.route('/download', methods=['GET'])
def download_video():
    url = request.args.get('url')

    if not url:
        return jsonify({"error": "Please provide a YouTube URL"}), 400

    try:
        ydl_opts = {
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
            'format': 'bestvideo+bestaudio/best',
            'cookiefile': COOKIES_FILE if os.path.exists(COOKIES_FILE) else None
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        return jsonify({
            "message": "Download successful",
            "title": info.get('title', 'Unknown'),
            "filename": os.path.basename(filename),
            "download_url": f"https://your-api-url.com/downloads/{os.path.basename(filename)}"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Serve Downloaded Files
@app.route('/downloads/<filename>', methods=['GET'])
def serve_file(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
