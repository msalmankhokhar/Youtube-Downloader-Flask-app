from flask import Flask, render_template, request, flash, redirect, send_file, Response, stream_with_context, g, session
import requests
from util import get_thumbnail_url, is_valid_youtube_url, seconds_to_duration
from pytube import YouTube, Stream
from pytube.exceptions import VideoUnavailable, RegexMatchError
from waitress import serve
from urllib.parse import urljoin
from svg import svg

app = Flask(__name__)
app.secret_key = "salmank138"
THEME_COLOR = "red"
THEME_COLOR2 = "orange"

@app.before_request
def add_theme_color():
    g.themecolor = THEME_COLOR
    g.themecolor2 = THEME_COLOR2
    g.svg = svg

@app.route('/theme', methods=['GET'])
def theme():
    darkTheme = request.args.get('value')
    if darkTheme == 'true':
        session.update({ 'theme' : True })
        return { 'theme' : True }
    else:
        session.pop('theme')
        return { 'theme' : False }

@app.route('/')
def index():
    link = request.args.get("link")
    # prevImg = urljoin(request.host_url, '/static/logos/apple-touch-icon.png')
    prevImg = urljoin(request.host_url, '/static/mockups/sssrocks/index/light.png')
    # prevImg = urljoin(request.host_url, '/static/mockups/screely/index/index_light.png')
    return render_template('index.html', link =  link, prevImg =  prevImg)

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
            return render_template('video.html', imgSrc = thumbNail_src, info = info, link = link)
        except VideoUnavailable as e:
            flash(f"Sorry this video is unavailable<br>Error: {str(e)}", "danger")
            return redirect("/")
        except RegexMatchError as e:
            flash(f"Invalid URL! Please enter a valid youtube video URL<br>Error: {str(e)}", "warning")
            return redirect("/")
        except Exception as e:
            flash(f"{str(e)}", "danger")
            return redirect("/")
    else:
        flash("Invalid URL! Please enter a valid youtube video URL", "warning")
        return redirect("/")

@app.route('/streams', methods=["GET", "POST"])
def get_streams():
    link = request.args.get("link")
    if request.method == "GET":
        try:
            video = YouTube(link)
            streamQuery = video.streams.filter(file_extension='mp4', only_audio=False, type="video", progressive=False)
            streams = [ { "res" : stream.resolution, "dl_link" : stream.url, "filesize" : round(stream.filesize_mb), "includes_audio" : stream.includes_audio_track } for stream in streamQuery ]
            return { "list" : streams }
        except VideoUnavailable as e:
            return { "error" : True , "msg" : "Sorry, this Video is unavailable"}
        except Exception as e:
            return { "error" : True , "msg" : str(e)}

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
    # serve(app, host='0.0.0.0', port=80)
 