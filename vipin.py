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

    # Format select karein
    if download_type == "audio":
        format_option = "bestaudio/best"
    else:
        format_option = "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]"

    try:
        ydl_opts = {
            'format': format_option,
            'cookiefile': COOKIES_FILE,
            'merge_output_format': 'mp4',
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4'
            }]
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)

            # Video link extract karein
            formats = info.get("formats", [])
            video_url = None
            for f in formats:
                if f.get("ext") == "mp4" and f.get("vcodec") != "none":  # Ensure it's video
                    video_url = f.get("url")
                    break  # First matching video URL ko use karein

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
