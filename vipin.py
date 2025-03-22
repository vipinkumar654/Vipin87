from flask import Flask, request, jsonify
from pytube import YouTube

app = Flask(__name__)

# 📌 Yaha cookies file ka path define karein
COOKIES_FILE = "youtube_cookies.txt"

@app.route('/download', methods=['GET'])
def download_video():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        # ✅ YouTube object me cookies load karein
        yt = YouTube(video_url, use_oauth=True, allow_oauth_cache=True)
        yt.cookies.load(COOKIES_FILE)

        # ✅ Best quality stream select karein
        stream = yt.streams.get_highest_resolution()

        return jsonify({
            "title": yt.title,
            "download_url": stream.url,  # ✅ Sahi download link
            "filename": f"{yt.title}.mp4",
            "message": "Download successful"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
