The server is written in Python 3 and will respond to a JSON REST API call with the following parameters:

- url: The URL of the YouTube live stream.

It will return a JPEG of the captured frame, or a 500 error with the error message as the text.

To run the server, use the following command:

$ uv python3 run.py

# yt-dlp

In order to do this manually using yt-dlp:

```

yt-dlp -o frame --downloader ffmpeg --downloader-args "ffmpeg_i:-t 1" --exec "ffmpeg -y -sseof -0.1 -i {} -update 1 -q:v 2 {}.jpg" [URL]
```

The following will output a frame.jpg to the current directory and that would be the same as what I would want to output from the server.
