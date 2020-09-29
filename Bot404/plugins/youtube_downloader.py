from __future__ import unicode_literals
from nonebot import on_command, CommandSession
import nonebot
import youtube_dlc
import threading
import datetime

download_list = {}


def _cq_at_parser(user_id):
    return "[CQ:at,qq=" + str(user_id) + "]"


def send_message_auto(session, message):
    bot = nonebot.get_bot()
    if session.event.message_type == 'private':
        bot.sync.send_private_msg(user_id=session.event.user_id, message=message)
    elif session.event.message_type == 'group':
        bot.sync.send_group_msg(group_id=session.event.group_id, message=message)
    else:
        bot.sync.send_discuss_msg(discuss_id=session.event.discuss_id, message=message)


def upload_video(uploader, filename):
    if uploader == 'Gawr Gura Ch. hololive-EN':
        print('Gawr Gura')
    elif uploader == 'Watson Amelia Ch. hololive-EN':
        print('Watson Amelia')
    elif uploader == 'Ninomae Ina\'nis Ch. hololive-EN':
        print('Ninomae Ina\'nis')
    elif uploader == 'Takanashi Kiara Ch. hololive-EN':
        print('Takanashi Kiara')
    elif uploader == 'Mori Calliope Ch. hololive-EN':
        print('Mori Calliope')
    else:
        print(uploader)


def download_video(session, url):
    print("Start Downloading...")

    class Logger(object):
        @staticmethod
        def debug(msg):
            if 'Deleting' in msg:
                send_message_auto(session, '已成功转码视频：“' + download_list[session.event.message_type + ':' + str(session.event.user_id) + ':' + str(session.event.message_id)][0] + '”，开始上传到OneDrive……')
            pass

        @staticmethod
        def warning(msg):
            print('Warning: ' + msg)
            nonebot.get_bot().send_private_msg(user_id=1135989508, message="Warning: " + msg)
            pass

        @staticmethod
        def error(msg):
            print('Error: ' + msg)
            nonebot.get_bot().send_private_msg(user_id=1135989508, message="Error: " + msg)
            pass

    def tracker(data):
        if data['status'] == 'downloading':
            download_list[session.event.message_type + ':' + str(session.event.user_id) + ':' + str(session.event.message_id)][1] = data['_percent_str']
            print(download_list)
        if data['status'] == 'finished':
            send_message_auto(session, '已成功下载视频：“' + data['filename'] + '”，开始转码……')

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
        'logger': Logger(),
        # 'proxy': 'http://127.0.0.1:10809'
    }

    with youtube_dlc.YoutubeDL(options) as yt_dlc:
        yt_dlc.download([url])


@on_command('get', aliases=('dl', 'download', '扒'), only_to_me=False, shell_like=True)
async def get():
    pass


@get.args_parser
async def _(session: CommandSession):
    args = session.current_arg_text.strip().split()

    if len(args) == 1:
        download_thread = threading.Thread(target=download_video, args=(session, args[0]))
        download_thread.start()

        with youtube_dlc.YoutubeDL() as yt_dlc:
            info_dict = yt_dlc.extract_info(args[0], download=False)
            download_list[session.event.message_type + ':' + str(session.event.user_id) + ':' + str(session.event.message_id)] = [0,
                                                                                                                                  datetime.datetime.now().isoformat(),
                                                                                                                                  info_dict['title'],
                                                                                                                                  info_dict['uploader_id']]
            session.finish(message="开始下载视频：“" + info_dict['title'] + "”……")

    session.pause('扒源 指令仅支持 1 个参数')
