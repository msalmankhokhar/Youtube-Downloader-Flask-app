from flask import Flask, render_template, request, flash, redirect, send_file, Response, stream_with_context
import requests
from util import get_thumbnail_url, is_valid_youtube_url, seconds_to_duration
from pytube import YouTube, Stream
from pytube.exceptions import VideoUnavailable, RegexMatchError
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
        try:
            video = YouTube(link)
            thumbNail_src = video.thumbnail_url
            info = { "title" : video.title, "duration" : seconds_to_duration(video.length), "thumbnailSrc": thumbNail_src, "embed_url": video.embed_url }
            return render_template('dl.html', imgSrc = thumbNail_src, info = info, link = link)
        except VideoUnavailable as e:
            flash(f"Sorry this video is unavailable<br>Error: {str(e)}", "error")
            return redirect("/")
        except RegexMatchError as e:
            flash(f"Invalid URL! Please enter a valid youtube video URL<br>Error: {str(e)}", "error")
            return redirect("/")
    else:
        flash("Invalid URL! Please enter a valid youtube video URL", "error")
        return redirect("/")

@app.route('/streams', methods=["GET", "POST"])
def get_streams():
    link = request.args.get("link")
    if request.method == "GET":
        try:
            video = YouTube(link)
            streamQuery = video.streams.filter(file_extension='mp4', only_audio=False, type="video", progressive=True)
            streams = [ { "res" : stream.resolution, "dl_link" : stream.url, "filesize" : round(stream.filesize_mb), "includes_audio" : stream.includes_audio_track } for stream in streamQuery ]
            return { "list" : streams }
        except VideoUnavailable as e:
            return { "error" : True , "msg" : e.error_string}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
    # serve(app, host='0.0.0.0', port=80)
 