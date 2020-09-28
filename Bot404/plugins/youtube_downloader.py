from __future__ import unicode_literals
from nonebot import on_command, CommandSession
import youtube_dlc
import threading
import datetime

download_list = {}


async def download_video(session, url):
    class Logger(object):
        @staticmethod
        async def debug(msg):
            if 'Deleting' in msg:
                await session.send("The video: \"" + download_list[session.event.user_id + session.event.message_id][0] + "\" has been converted. Start uploading...")
            pass

        @staticmethod
        async def warning(msg):
            print('Warning: ' + msg)
            pass

        @staticmethod
        async def error(msg):
            print('Error: ' + msg)
            pass

    async def tracker(data):
        if data['status'] == 'downloading':
            download_list[session.event.user_id + session.event.message_id][1] = data['_percent_str']
            print(download_list)
        if data['status'] == 'finished':
            print('Completely Downloaded. Converting...')
            await session.send("The video: \"" + data['filename'] + "\" has been downloaded. Start converting...")

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
        download_thread = threading.Thread(target=download_video, args=(session, args[0]))
        download_thread.start()

        with youtube_dlc.YoutubeDL() as yt_dlc:
            info_dict = yt_dlc.extract_info(args[0], download=False)
            download_list[session.event.user_id + session.event.message_id] = [info_dict['title'], 0]
            session.state['res'] = "Start downloading the video: \"" + info_dict['title'] + "\" ..."
        return

    session.pause('Command: \"get\" only support 1 argument.')
