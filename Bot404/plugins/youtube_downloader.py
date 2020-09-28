from __future__ import unicode_literals
from nonebot import on_command, CommandSession
import youtube_dlc
import datetime
import copy

download_list = {}


async def download_video(event, url):
    class Logger(object):
        @staticmethod
        def debug(msg):
            print(msg)
            pass

        @staticmethod
        def warning(msg):
            print(msg)
            pass

        @staticmethod
        def error(msg):
            print(msg)
            pass

    def tracker(data):
        if data['status'] == 'downloading':
            download_list[data['filename']] = data['_percent_str']
            print(download_list)
        if data['status'] == 'finished':
            print('Completely Downloaded. Converting...')
            print(event.user_id)

    options = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'progress_hooks': [tracker],
        'merge_output_format': 'mp4',
        'postprocessors': [
            {
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4'
            }
        ],
        # 'logger': logger,
        'logger': Logger(),
        # 'proxy': 'http://127.0.0.1:10809'
    }

    with youtube_dlc.YoutubeDL(options) as yt_dlc:
        yt_dlc.download([url])


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
            'proxy': 'http://127.0.0.1:10809'
        }

        await download_video(session.event, args[0])

        with youtube_dlc.YoutubeDL(options) as yt_dlc:
            info_dict = yt_dlc.extract_info(args[0], download=False)
            session.state['res'] = info_dict['title']

        return

    session.pause('Command: \"get\" only support 1 argument.')
