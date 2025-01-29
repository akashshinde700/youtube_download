# youtube_download
This is a web-based YouTube downloader application built using Python's Flask framework and the powerful yt-dlp library. The tool allows users to download individual YouTube videos or entire playlists. It provides a simple user interface for video/playlist URL submission and download quality selection, and supports downloading content in various formats

**Features:**
Download Single Video: Input the URL of a single video, and the tool will download it in the desired quality.
Download Playlists: Enter a playlist URL to fetch and download the entire playlist or select specific videos.
User-friendly Web Interface: A basic web page allows easy interaction with the tool.
Quality Selection: Choose video quality (e.g., best quality or specific formats).
Custom Download Path: Optionally specify a custom download location.
yt-dlp Backend: Uses yt-dlp, a powerful tool for downloading videos from YouTube and other sites.

**Requirements:**
Python 3.x
Flask - Install with: pip install Flask
yt-dlp - Install with: pip install yt-dlp

**Run the Flask server:** 
Navigate to the project directory and start the server:
**python server.py**

Access the Web Interface: Open your browser and go to **http://127.0.0.1:5000**. The web interface will allow you to:

Input the YouTube video or playlist URL.
Choose the download quality and specify a custom download path if needed.
Start the download by clicking the appropriate button.

**Download Process:**

The server will fetch the video or playlist information.
It will then download the selected content in the best available quality or the specified format.
Downloaded files will be saved to the specified location.


**License:**
This project is open-source and can be modified and used freely. Make sure to adhere to YouTube's Terms of Service when downloading content.
