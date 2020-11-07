from __future__ import unicode_literals
from nonebot import on_command, CommandSession

from Bot404.configs import *
from Bot404.utils.cq_utils import *
from Bot404.utils.ytdl_spliter import *

import youtube_dlc
import threading
import datetime
import logging
import shutil
import os
import re

download_list = {}  # {'timestamp': 'info_dict'}


def upload_video(session, video_info):
    new_filename = re.sub(r'[\\/:*?"<>|]', '&', video_info['title'])
    is_in_group = False
    if CONSTANTS["ENABLE_WEBDAV"]:
        # noinspection PyBroadException
        try:
            split_count = execute_split(f'{PATHS["CACHE_PATH"]}{video_info["now_time"]}.mp4')
            for temp_group in GROUPS:
                if video_info['uploader_id'] == temp_group['channel']:
                    is_in_group = True
                    logging.info(f'Uploading to {temp_group["nickname"]} ...')
                    for clip_number in range(1, split_count):
                        shutil.copy(
                            f'{PATHS["CACHE_PATH"]}{video_info["now_time"]}_{clip_number}.mp4',
                            f'{temp_group["drive"]}/{new_filename}_{clip_number}.mp4'
                        )
                    send_message_auto(session, '成功下载视频：“' + video_info['title'] + f'”，已上传到“{temp_group["nickname"]}”的WebDav缓存，请等待完全上传后再操作文件')
            if not is_in_group:
                logging.info(f'Uploading to {GROUPS[0]["nickname"]} ...')
                for clip_number in range(1, split_count):
                    shutil.copy(
                        f'{PATHS["CACHE_PATH"]}{video_info["now_time"]}_{clip_number}.mp4',
                        f'{GROUPS[0]["drive"]}/{new_filename}_{clip_number}.mp4'
                    )
                send_message_auto(session, '成功下载视频：“' + video_info['title'] + f'”，已上传到“{GROUPS[0]["nickname"]}”的WebDav缓存，请等待完全上传后再操作文件')
            os.remove(f'{PATHS["CACHE_PATH"]}{video_info["now_time"]}.mp4')
            for clip_number in range(1, split_count):
                os.remove(f'{PATHS["CACHE_PATH"]}{video_info["now_time"]}_{clip_number}.mp4')
        except FileNotFoundError:
            exception_handler(
                f'未能上传文件：找不到源文件\n{video_info["now_time"]}.mp4 -> {new_filename}.mp4',
                logging.ERROR)
        except Exception:
            exception_handler(
                f'未能上传文件：未知错误，请查看日志\n{video_info["now_time"]}.mp4 -> {new_filename}.mp4',
                logging.ERROR)
    else:
        # noinspection PyBroadException
        try:
            for temp_group in GROUPS:
                if video_info['uploader_id'] == temp_group['channel']:
                    is_in_group = True
                    shutil.copy(
                        f'{PATHS["CACHE_PATH"]}{video_info["now_time"]}.mp4',
                        f'{temp_group["drive"]}/{new_filename}.mp4'
                    )
                    send_message_auto(session, '成功下载视频：“' + video_info['title'] + f'”，已上传到“{temp_group["nickname"]}”的OneDrive')
            if not is_in_group:
                shutil.copy(
                    f'{PATHS["CACHE_PATH"]}{video_info["now_time"]}.mp4',
                    f'{GROUPS[0]["drive"]}/{new_filename}.mp4'
                )
                send_message_auto(session, '成功下载视频：“' + video_info['title'] + f'”，已上传到“{GROUPS[0]["nickname"]}”的OneDrive')
            os.remove(f'{PATHS["CACHE_PATH"]}{video_info["now_time"]}.mp4')
        except FileNotFoundError:
            exception_handler(
                f'未能上传文件：找不到源文件\n{video_info["now_time"]}.mp4 -> {new_filename}.mp4',
                logging.ERROR)
        except Exception:
            exception_handler(
                f'未能上传文件：未知错误，请查看日志\n{video_info["now_time"]}.mp4 -> {new_filename}.mp4',
                logging.ERROR)


def is_duplicated(info_dict):
    for video_info in download_list.values():
        if info_dict['id'] == video_info['id']:
            return True
    return False


def download_video(session, time):
    video_info = download_list[time]
    logging.info("Start Downloading...")

    class Logger(object):
        @staticmethod
        def debug(msg):
            if 'Deleting' in msg:
                if '.flv' in msg or '.m4a' in msg:
                    if video_info['status'] != '上传中':
                        video_info['status'] = '上传中'
                    logging.info("Start Uploading...")
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
        if data['status'] == 'finished' and ('.flv' in data['filename']
                                             or '.m4a' in data['filename']):
            if video_info['status'] != '转码中':
                video_info['status'] = '转码中'
                logging.info("Start Converting...")

    options = {
        'format':
            'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'progress_hooks': [tracker],
        'logger':
            Logger(),
        'merge_output_format':
            'mp4',
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4'
        }],
        'outtmpl':
            f'{PATHS["CACHE_PATH"]}{time}.%(ext)s',
    }
    # noinspection PyBroadException
    try:
        with youtube_dlc.YoutubeDL(options) as yt_dlc:
            yt_dlc.download([video_info['webpage_url']])
    except Exception:
        exception_handler(f'下载失败：下载过程中出现错误，请排除队列错误后再试。', logging.ERROR, False,
                          session.event.group_id)
        if download_list:
            download_list.pop(time)
        else:
            print("[WARN]Download List not exist.")


@on_command('get',
            aliases=('dl', 'download', '扒源', '扒'),
            only_to_me=False,
            shell_like=True)
async def get(session: CommandSession):
    args = session.current_arg_text.strip().split()

    if len(args) == 1:
        # noinspection PyBroadException
        try:
            with youtube_dlc.YoutubeDL() as yt_dlc:
                info_dict = yt_dlc.extract_info(args[0], download=False)
                if is_duplicated(info_dict):
                    await session.send('视频：“' + info_dict["title"] +
                                       '”已在队列中，请勿重复下载')
                    return
            info_dict['status'] = '等待中'
            info_dict['now_time'] = datetime.datetime.now().strftime(
                '%Y-%m-%d_%H:%M:%S.%f')
            download_list[info_dict['now_time']] = info_dict
            download_thread = threading.Thread(target=download_video,
                                               args=(session,
                                                     info_dict['now_time']))
            download_thread.start()
            await session.send('视频：“' + info_dict["title"] + '”加入下载队列')
        except youtube_dlc.utils.UnsupportedError:
            exception_handler(f'解析失败：视频地址不受支持，请确认地址是否正确后再试。', logging.WARNING,
                              False, session.event.group_id)
        except youtube_dlc.utils.DownloadError as dl_error:
            exception_handler(f'解析失败：{dl_error.exc_info}', logging.ERROR)
        except Exception:
            exception_handler(f'解析失败：未知错误，请查看运行日志。', logging.ERROR, False,
                              session.event.group_id)
        return
    else:
        await session.send("参数个数错误，仅支持一个参数，请检查后再试。")


@on_command('queue',
            aliases=('qu', '扒源队列', '队列'),
            only_to_me=False,
            shell_like=True)
async def queue(session: CommandSession):
    # args = session.current_arg_text.strip().split()
    if len(download_list.values()) != 0:
        response = '扒源队列：\n'
        for video_info in download_list.values():
            response += '| 视频名：' + str(video_info['title']) + ' | ' + str(
                video_info['status']) + ' |\n'
    else:
        response = '扒源队列为空'
    await session.send(response)
