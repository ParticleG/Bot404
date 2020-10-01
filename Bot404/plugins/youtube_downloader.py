from __future__ import unicode_literals
from nonebot import on_command, CommandSession
from Bot404.utils.configs import *
from Bot404.utils.cq_utils import *
import nonebot
import youtube_dlc
import threading
import datetime
import shutil
import re
import traceback
import logging

download_list = {}  # 'message_type:user_id:message_id': ['state_str', 'percent_str', 'YYYY-MM-DD_hh-mm-ss', 'title', 'uploader_id']


def upload_video(session, video_info):
    new_filename = re.sub(r'[\\/:*?"<>|]', '_', video_info[3])
    group_name = 'others'
    try:
        if video_info[4] == 'UCoSrY_IQQVpmIRZ9Xf-y93g':
            group_name = 'gura'
        elif video_info[4] == 'UCyl1z3jo3XHR1riLFKG5UAg':
            group_name = 'amelia'
        elif video_info[4] == 'UCMwGHR0BTZuLsmjY_NT5Pwg':
            group_name = 'ina'
        elif video_info[4] == 'UCHsx4Hqa-1ORjQTh9TYDhww':
            group_name = 'kiara'
        elif video_info[4] == 'UCL_qhgtOy0dy1Agp8vkySQg':
            group_name = 'callio'
        else:
            pass
        shutil.copy(f'{CACHE_PATH}{video_info[2]}.mp4', f'{DRIVE_PATH}{group_name}/{new_filename}.mp4')
        send_message_auto(session, '成功上传视频：“' + video_info[3] + f'”到{group_name}盘')
    except FileNotFoundError as file_e:
        exception_handler(file_e, f'未能上传文件：找不到源文件\n{video_info[2]}.mp4 -> {new_filename}.mp4', logging.ERROR)
    except Exception as e:
        exception_handler(e, f'未能上传文件：未知错误，请查看日志\n{video_info[2]}.mp4 -> {new_filename}.mp4', logging.ERROR)


def download_video(session, info):
    bot = nonebot.get_bot()
    info_key = session.event.message_type + ':' + str(session.event.user_id) + ':' + str(session.event.message_id)
    now_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    print("Start Downloading...")

    download_list[session.event.message_type + ':' + str(session.event.user_id) + ':' + str(session.event.message_id)] \
        = ['Waiting',
           '  0.0%',
           now_time,
           info['title'],
           info['uploader_id']
           ]

    class Logger(object):
        @staticmethod
        def debug(msg):
            if 'Deleting' in msg:
                if '.flv' in msg or '.m4a' in msg:
                    video_info = download_list[info_key]
                    if video_info[0] != 'uploading':
                        video_info[0] = 'uploading'
                    send_message_auto(session, '成功转码视频：“' + video_info[3] + '”，开始上传到OneDrive')
                    upload_video(session, video_info)
                    download_list.pop(info_key)

        @staticmethod
        def warning(msg):
            exception_handler(None, f'YoutubeDLC：{msg}', logging.WARNING)

        @staticmethod
        def error(msg):
            exception_handler(None, f'YoutubeDLC：{msg}', logging.ERROR)

    def tracker(data):
        if data['status'] == 'downloading':
            video_info = download_list[info_key]
            if video_info[0] != 'downloading':
                video_info[0] = 'downloading'
            video_info[1] = data['_percent_str']
        if data['status'] == 'finished':
            if '.flv' in data['filename'] or '.m4a' in data['filename']:
                video_info = download_list[info_key]
                if video_info[0] != 'converting':
                    video_info[0] = 'converting'
                send_message_auto(session, '成功下载视频：“' + video_info[3] + '”，开始转码')

    options = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'progress_hooks': [tracker],
        'logger': Logger(),
        'merge_output_format': 'mp4',
        'postprocessors': [{'key': 'FFmpegVideoConvertor', 'preferedformat': 'mp4'}],
        'outtmpl': f'{CACHE_PATH}{now_time}.%(ext)s',
    }
    try:
        with youtube_dlc.YoutubeDL(options) as yt_dlc:
            yt_dlc.download([info['webpage_url']])
    except Exception:
        logging.error(f"下载时出现未知错误：{traceback.format_exc()}")
        bot.sync.send_group_msg(group_id=session.event.group_id,
                                message="下载时出现错误，请排除队列错误后再试。")


@on_command('get', aliases=('dl', 'download', '扒源', '扒'), only_to_me=False, shell_like=True)
async def get():
    pass


@on_command('queue', aliases=('qu', '任务列表', '队列'), only_to_me=False, shell_like=True)
async def queue(session: CommandSession):
    await session.send(session.get('res'))


@get.args_parser
async def _(session: CommandSession):
    args = session.current_arg_text.strip().split()

    if len(args) == 1:
        try:
            with youtube_dlc.YoutubeDL() as yt_dlc:
                info_dict = yt_dlc.extract_info(args[0], download=False)
            download_thread = threading.Thread(target=download_video, args=(session, info_dict))
            download_thread.start()
        except Exception as e:
            logging.error(f"解析时出现位置错误：{traceback.format_exc()}")
            await session.bot.send_group_msg(group_id=session.event.group_id, message="解析时出现错误，请确认地址是否正确后再试。")
        session.finish(message="视频：“" + info_dict['title'] + "”加入下载队列")
        return

    session.pause('扒源 指令仅支持 1 个参数')


@queue.args_parser
async def _(session: CommandSession):
    args = session.current_arg_text.strip().split()

    if len(args) == 0:
        response = '扒源队列：\n'
        for video_info in download_list.values():
            response += '| 视频名：' + str(video_info[3]) + ' | ' + str(video_info[0]) + ' | ' + str(video_info[1]) + ' | 开始时间：' + str(video_info[2]) + ' |\n'
        session.state['res'] = response
        return
    session.pause('任务列表 指令仅支持 0 个参数')
