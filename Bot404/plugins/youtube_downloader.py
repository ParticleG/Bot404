from __future__ import unicode_literals
from nonebot import on_command, CommandSession
import youtube_dlc
import datetime
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def tracker(d):
    if d['status'] == 'downloading':
        percent = d['_percent_str']
        print(percent)
    if d['status'] == 'finished':
        print('Completely Downloaded. Converting...')


def _cq_at_parser(user_id):
    return "[CQ:at,qq=" + str(user_id) + "]"


@on_command('get', only_to_me=False, shell_like=True)
async def get(session: CommandSession):
    await session.send(session.get('res'))


@get.args_parser
async def _(session: CommandSession):
    args = session.current_arg_text.strip().split()

    if len(args) == 1:
        options = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'progress_hooks': [tracker],
            'merge_output_format': 'mp4',
            'logger': logger,
            'proxy': 'http://127.0.0.1:10809'
        }
        print(options)
        # with youtube_dlc.YoutubeDL(options) as yt_dlc:
        #     yt_dlc.download([args[0]])
        return

    session.pause('Command: \"get\" only support 1 argument.')
