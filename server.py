from flask import Flask, request, send_file, jsonify, render_template
import yt_dlp
import os
import logging
import json
import csv

app = Flask(__name__)

# Set up the path to store downloaded files
DOWNLOAD_PATH = "C:/Users/Mulsan IT/Downloads/pro/downloads"
if not os.path.exists(DOWNLOAD_PATH):
    os.makedirs(DOWNLOAD_PATH)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Helper function to download the video using yt-dlp
def download_video_yt_dlp(video_url, quality, download_path):
    try:
        ydl_opts = {
            'format': f'{quality}+bestaudio/best',
            'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
            'headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
            },
            'nocheckcertificate': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(video_url, download=True)
        
        if 'entries' in result:
            # It's a playlist
            return [entry['title'] + '.' + entry['ext'] for entry in result['entries']]
        else:
            # It's a single video
            return [result['title'] + '.' + result['ext']]
    except yt_dlp.utils.DownloadError as e:
        logging.error(f"Error downloading video with yt-dlp: {e}")
        return None

# Helper function to fetch playlist details using yt-dlp
def fetch_playlist_details_yt_dlp(playlist_url):
    try:
        ydl_opts = {
            'extract_flat': True,  # Only fetch the playlist info
            'headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
            },
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(playlist_url, download=False)

        playlist_info = {
            "title": result.get("title"),
            "video_count": len(result["entries"]),
            "duration": result.get("duration"),
            "videos": [{"title": video["title"], "url": video["url"], "duration": video["duration"]} for video in result["entries"]],
        }

        return playlist_info
    except Exception as e:
        logging.error(f"Error fetching playlist with yt-dlp: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch_playlist', methods=['POST'])
def fetch_playlist():
    try:
        data = request.get_json()
        playlist_url = data.get("url")
        source = data.get("source", "yt-dlp")  # Default is 'yt-dlp'

        if not playlist_url:
            return jsonify({"error": "Playlist URL is required"}), 400

        # Fetch playlist details using yt-dlp
        if source == "yt-dlp":
            playlist_info = fetch_playlist_details_yt_dlp(playlist_url)

        if playlist_info:
            return jsonify(playlist_info)
        else:
            return jsonify({"error": "Failed to fetch playlist details"}), 400

    except Exception as e:
        logging.error(f"Error in fetch_playlist route: {e}")
        return jsonify({"error": f"Failed to fetch playlist details: {str(e)}"}), 500

@app.route('/fetch_video', methods=['POST'])
def fetch_video():
    try:
        data = request.get_json()
        video_url = data.get("url")

        if not video_url:
            return jsonify({"error": "Video URL is required"}), 400

        ydl_opts = {
            'extract_flat': True,
            'headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
            },
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(video_url, download=False)

        video_info = {
            "title": result.get("title"),
            "duration": result.get("duration"),
            "videos": [{
                "title": result.get("title"),
                "url": video_url,
                "duration": result.get("duration")
            }]
        }

        return jsonify(video_info)

    except Exception as e:
        logging.error(f"Error in fetch_video route: {e}")
        return jsonify({"error": f"Failed to fetch video details: {str(e)}"}), 500

@app.route('/download_video', methods=['POST'])
def download_video_route():
    try:
        data = request.get_json()
        video_url = data.get("url")
        quality = data.get("quality", "best")
        selected_files = data.get("selected_files", [])
        is_playlist = data.get("is_playlist", False)
        custom_path = data.get("custom_path", "")

        if not video_url:
            return jsonify({"error": "Video URL is required"}), 400

        download_path = os.path.join(DOWNLOAD_PATH, custom_path) if custom_path else DOWNLOAD_PATH
        if not os.path.exists(download_path):
            os.makedirs(download_path)

        filenames = download_video_yt_dlp(video_url, quality, download_path)

        if filenames:
            if is_playlist:
                selected_filenames = [f for f in filenames if f in selected_files]
                return jsonify({"message": f"Downloaded {len(selected_filenames)} files", "files": selected_filenames})
            else:
                return send_file(os.path.join(download_path, filenames[0]), as_attachment=True)

        return jsonify({"error": "Failed to download video"}), 500

    except Exception as e:
        logging.error(f"Error in download_video route: {e}")
        return jsonify({"error": f"Failed to download video: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
