from flask import Flask, render_template, request, flash, redirect, send_file, Response, stream_with_context
import requests
from util import get_thumbnail_url, is_valid_youtube_url, seconds_to_duration
from pytube import YouTube, Stream
from pytube.exceptions import VideoUnavailable
from waitress import serve

app = Flask(__name__)
app.secret_key = "salmank138"

@app.route('/')
def index():
    link = request.args.get("link")
    return render_template('index.html', link =  link)

@app.route('/video')
def video():
    link = request.args.get("link")
    isValidLink = is_valid_youtube_url(str(link))
    print(f"<{link}> is {isValidLink}") # debug print statement
    if isValidLink == True:
        video = YouTube(link)
        thumbNail_src = video.thumbnail_url
        info = { "title" : video.title, "duration" : seconds_to_duration(video.length), "thumbnailSrc": thumbNail_src, "embed_url": video.embed_url }
        return render_template('dl.html', imgSrc = thumbNail_src, info = info, link = link)
    else:
        flash("Invalid URL! Please enter a valid youtube video URL", "error")
        return redirect("/")

@app.route('/streams', methods=["GET", "POST"])
def get_streams():
    link = request.args.get("link")
    video = YouTube(link)
    streamQuery = video.streams.filter(file_extension='mp4', only_audio=False, type="video", progressive=True)
    if request.method == "GET":
        streams = [ { "res" : stream.resolution, "dl_link" : stream.url, "filesize" : round(stream.filesize_mb), "includes_audio" : stream.includes_audio_track } for stream in streamQuery ]
        return { "list" : streams }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
    # serve(app, host='0.0.0.0', port=80)
 