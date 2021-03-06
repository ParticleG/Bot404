from __future__ import unicode_literals
from nonebot import on_command, CommandSession
from Bot404.utils.configs import *
from Bot404.utils.cq_utils import *
import nonebot
import youtube_dlc
import threading
import datetime
import logging
import shutil
import os
import re

download_list = {}  # {'timestamp': 'info_dict'}


def upload_video(session, video_info):
    new_filename = re.sub(r'[\\/:*?"<>|]', '_', video_info['title'])
    group_name = 'others'
    try:
        if video_info['uploader_id'] == 'UCoSrY_IQQVpmIRZ9Xf-y93g':
            group_name = 'gura'
        elif video_info['uploader_id'] == 'UCyl1z3jo3XHR1riLFKG5UAg':
            group_name = 'amelia'
        elif video_info['uploader_id'] == 'UCMwGHR0BTZuLsmjY_NT5Pwg':
            group_name = 'ina'
        elif video_info['uploader_id'] == 'UCHsx4Hqa-1ORjQTh9TYDhww':
            group_name = 'kiara'
        elif video_info['uploader_id'] == 'UCL_qhgtOy0dy1Agp8vkySQg':
            group_name = 'callio'
        else:
            pass
        shutil.copy(f'{CACHE_PATH}{video_info["now_time"]}.mp4', f'{DRIVE_PATH}{group_name}/{new_filename}.mp4')
        send_message_auto(session, '成功下载视频：“' + video_info['title'] + f'”，已上传到{group_name}盘')
        os.remove(f'{CACHE_PATH}{video_info["now_time"]}.mp4')
    except FileNotFoundError:
        exception_handler(f'未能上传文件：找不到源文件\n{video_info["now_time"]}.mp4 -> {new_filename}.mp4', logging.ERROR)
    except Exception:
        exception_handler(f'未能上传文件：未知错误，请查看日志\n{video_info["now_time"]}.mp4 -> {new_filename}.mp4', logging.ERROR)


def is_duplicated(info_dict):
    for video_info in download_list.values():
        if info_dict['id'] == video_info['id']:
            return True
    return False


def download_video(session, time):
    bot = nonebot.get_bot()
    video_info = download_list[time]
    logging.info("Start Downloading...")

    class Logger(object):
        @staticmethod
        def debug(msg):
            if 'Deleting' in msg:
                if '.flv' in msg or '.m4a' in msg:
                    if video_info['status'] != '上传中':
                        video_info['status'] = '上传中'
                    # send_message_auto(session, '成功转码视频：“' + video_info['title'] + '”，开始上传到OneDrive')
                    upload_video(session, video_info)
                    if download_list:
                        download_list.pop(time)
                    else:
                        print("[WARN]Download List not exist.")

        @staticmethod
        def warning(msg):
            exception_handler(f'YoutubeDLC：{msg}', logging.WARNING)

        @staticmethod
        def error(msg):
            exception_handler(f'YoutubeDLC：{msg}', logging.ERROR)

    def tracker(data):
        nonlocal video_info
        if data['status'] == 'downloading':
            video_info['status'] = '已下载' + data['_percent_str']
        if data['status'] == 'finished' and ('.flv' in data['filename'] or '.m4a' in data['filename']):
            if video_info['status'] != '转码中':
                video_info['status'] = '转码中'
            # send_message_auto(session, '成功下载视频：“' + video_info['title'] + '”，开始转码')

    options = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'progress_hooks': [tracker],
        'logger': Logger(),
        'merge_output_format': 'mp4',
        'postprocessors': [{'key': 'FFmpegVideoConvertor', 'preferedformat': 'mp4'}],
        'outtmpl': f'{CACHE_PATH}{time}.%(ext)s',
    }
    try:
        with youtube_dlc.YoutubeDL(options) as yt_dlc:
            yt_dlc.download([video_info['webpage_url']])
    except Exception:
        exception_handler(f'下载失败：下载过程中出现错误，请排除队列错误后再试。', logging.ERROR, False, session.event.group_id)


@on_command('get', aliases=('dl', 'download', '扒源', '扒'), only_to_me=False, shell_like=True)
async def get(session: CommandSession):
    args = session.current_arg_text.strip().split()

    if len(args) == 1:
        try:
            with youtube_dlc.YoutubeDL() as yt_dlc:
                info_dict = yt_dlc.extract_info(args[0], download=False)
                if is_duplicated(info_dict):
                    session.send('视频：“' + info_dict["title"] + '”已在队列中，请勿重复下载')
                    return
            info_dict['status'] = '等待中'
            info_dict['now_time'] = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S.%f')
            download_list[info_dict['now_time']] = info_dict
            download_thread = threading.Thread(target=download_video, args=(session, info_dict['now_time']))
            download_thread.start()
            session.send('视频：“' + info_dict["title"] + '”加入下载队列')
        except youtube_dlc.utils.UnsupportedError:
            exception_handler(f'解析失败：视频地址不受支持，请确认地址是否正确后再试。', logging.WARNING, False, session.event.group_id)
        except youtube_dlc.utils.DownloadError as dl_error:
            exception_handler(f'解析失败：{dl_error.exc_info}', logging.ERROR)
        except Exception as e:
            exception_handler(f'解析失败：未知错误，请查看运行日志。', logging.ERROR, False, session.event.group_id)
        return
    else:
        session.send("参数个数错误，仅支持一个参数，请检查后再试。")


@on_command('queue', aliases=('qu', '扒源队列', '队列'), only_to_me=False, shell_like=True)
async def queue(session: CommandSession):
    # args = session.current_arg_text.strip().split()
    if len(download_list.values()) != 0:
        response = '扒源队列：\n'
        for video_info in download_list.values():
            response += '| 视频名：' + str(video_info['title']) + ' | ' + str(video_info['status']) + ' |\n'
    else:
        response = '扒源队列为空'
    await session.send(response)



