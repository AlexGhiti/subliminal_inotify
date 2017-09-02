# Automatic subtitle download with subliminal and inotify

Simple python script that uses inotify to wait for new video files and
download subtitles automatically.

### Installation

```
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

### Use

```
$ python subliminal_inotify.py --path=<PATH_TO_VIDEOS>
```
