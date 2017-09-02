import argparse
import pyinotify
from babelfish import Language
from subliminal import download_best_subtitles, region, save_subtitles, scan_videos

class EventHandler(pyinotify.ProcessEvent):
	def subliminal_download(self):
		# scan for videos
		videos = scan_videos(args.path)
		# download best subtitles
		subtitles = download_best_subtitles(videos, {Language('eng'), Language('fra')})
		# save them to disk, next to the video
		for v in videos:
			save_subtitles(v, subtitles[v])

	def process_IN_CREATE(self, event):
		self.subliminal_download()

	def process_IN_MOVED_TO(self, event):
		self.subliminal_download()

parser = argparse.ArgumentParser(description = 'Automatic subtitles download')
parser.add_argument('--path', default = "",
		help = 'Path where videos are stored.')

args = parser.parse_args()

wm = pyinotify.WatchManager()
# IN_MOVED_FROM must be watched to get src_pathname in IN_MOVED_TO.
mask = pyinotify.IN_CREATE | pyinotify.IN_MOVED_TO | pyinotify.IN_MOVED_FROM

# Configure subliminal cache
region.configure('dogpile.cache.dbm', arguments={'filename': 'cachefile.dbm'})

# Wait for new file
handler = EventHandler()
notifier = pyinotify.Notifier(wm, handler)
wdd = wm.add_watch(args.path, mask, rec = True)
notifier.loop()
