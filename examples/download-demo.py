from __future__ import unicode_literals
import youtube_dlc
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def tracker(d):
    if d['status'] == 'downloading':
        percent = d['_percent_str']
        print(d)
    if d['status'] == 'finished':
        print('Completely Downloaded. Converting...')


options = {
    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
    'progress_hooks': [tracker],
    'merge_output_format': 'mp4',
    'logger': logger,
    'proxy': 'http://127.0.0.1:10809'
}

if __name__ == '__main__':
    with youtube_dlc.YoutubeDL(options) as yt_dlc:
        # 夸宝好き
        yt_dlc.download(['https://www.youtube.com/watch?v=coIo0JtK-yA'])
