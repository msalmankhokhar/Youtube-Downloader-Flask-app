from pytubefix import YouTube, StreamQuery, Stream
from typing import Iterable

# link = "https://youtu.be/KCQEJZLD0pI?si=9fQnvt3XZMo59UzJ"
# link = "https://www.youtube.com/watch?v=KCQEJZLD0pI&t=64s"
link = "https://youtu.be/6x-NlZkbd-U?si=HvsIx4zRaZZ6DaXw"

video = YouTube(link)

# print(video.age_restricted)

query : list[Stream] = video.streams.filter(type='video', res="720p", mime_type='video/mp4', progressive=False).order_by('resolution')

for stream in query:
    print(f'{stream} {stream.filesize_mb} {stream.audio_codec} {stream.url}')