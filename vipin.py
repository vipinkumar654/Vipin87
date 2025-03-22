from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

COOKIES_FILE = "cookies.txt"

@app.route('/download', methods=['GET'])
def download():
    video_url = request.args.get('url')
    download_type = request.args.get('type', 'video')  # Default: Video

    if not video_url:
        return jsonify({"error": "YouTube URL required!"}), 400

    # Format select karein (MP4 ya MP3)
    if download_type == "audio":
        format_option = "bestaudio/best"
    else:
        format_option = "bestvideo+bestaudio/best"

    try:
        ydl_opts = {
            'format': format_option,
            'cookiefile': COOKIES_FILE
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            download_url = info.get("url", None)

            if not download_url:
                return jsonify({"error": "Failed to extract download link"}), 500

            return jsonify({
                "title": info.get("title", "Unknown Title"),
                "thumbnail": info.get("thumbnail", ""),
                "duration": info.get("duration", 0),
                "download_url": download_url
            })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
