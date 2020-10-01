from __future__ import unicode_literals
from nonebot import on_command, CommandSession
import nonebot
import aiocqhttp
import youtube_dlc
import threading
import datetime
import shutil
import re

download_list = {}


# 'message_type:user_id:message_id': ['state_str', 'percent_str', 'YYYY-MM-DD_hh-mm-ss', 'title', 'uploader_id']

def _cq_at_parser(user_id):
    return "[CQ:at,qq=" + str(user_id) + "]"


def send_message_auto(session, message):
    bot = nonebot.get_bot()
    if session.event.message_type == 'private':
        bot.sync.send_private_msg(user_id=session.event.user_id, message=message)
    elif session.event.message_type == 'group':
        try:
            bot.sync.send_group_msg(group_id=session.event.group_id, message=message)
        except aiocqhttp.exceptions.ActionFailed:
            bot.sync.send_private_msg(user_id=session.event.user_id, message='Exception on GroupMessage: ' + message)

    else:
        try:
            bot.sync.send_discuss_msg(discuss_id=session.event.discuss_id, message=message)
        except aiocqhttp.exceptions.ActionFailed:
            bot.sync.send_private_msg(user_id=session.event.user_id, message='Exception on DiscussMessage: ' + message)


def upload_video(session, video_info):
    new_filename = re.sub(r'[\\/:*?"<>|]', '_', video_info[3])
    try:
        if video_info[4] == 'UCoSrY_IQQVpmIRZ9Xf-y93g':
            shutil.copy(f'/usr/go-cqhttp/quin33/caches/{video_info[2]}.mp4', f'/usr/drive/holoen/gura/{new_filename}.mp4')
            send_message_auto(session, '成功上传视频：“' + video_info[3] + '”到Gura组盘')
        elif video_info[4] == 'UCyl1z3jo3XHR1riLFKG5UAg':
            shutil.copy(f'/usr/go-cqhttp/quin33/caches/{video_info[2]}.mp4', f'/usr/drive/holoen/amelia/{new_filename}.mp4')
            send_message_auto(session, '成功上传视频：“' + video_info[3] + '”到Amelia组盘')
        elif video_info[4] == 'UCMwGHR0BTZuLsmjY_NT5Pwg':
            shutil.copy(f'/usr/go-cqhttp/quin33/caches/{video_info[2]}.mp4', f'/usr/drive/holoen/ina/{new_filename}.mp4')
            send_message_auto(session, '成功上传视频：“' + video_info[3] + '”到Ina组盘')
        elif video_info[4] == 'UCHsx4Hqa-1ORjQTh9TYDhww':
            shutil.copy(f'/usr/go-cqhttp/quin33/caches/{video_info[2]}.mp4', f'/usr/drive/holoen/kiara/{new_filename}.mp4')
            send_message_auto(session, '成功上传视频：“' + video_info[3] + '”到Kiara组盘')
        elif video_info[4] == 'UCL_qhgtOy0dy1Agp8vkySQg':
            shutil.copy(f'/usr/go-cqhttp/quin33/caches/{video_info[2]}.mp4', f'/usr/drive/holoen/callio/{new_filename}.mp4')
            send_message_auto(session, '成功上传视频：“' + video_info[3] + '”到Callio组盘')
        else:
            shutil.copy(f'/usr/go-cqhttp/quin33/caches/{video_info[2]}.mp4', f'/usr/drive/holoen/others/{new_filename}.mp4')
            send_message_auto(session, '成功上传视频：“' + video_info[3] + '”到Others盘')
        download_list.pop(session.event.message_type + ':' + str(session.event.user_id) + ':' + str(session.event.message_id))
    except FileNotFoundError:
        bot.sync.send_group_msg(group_id=session.event.group_id, message="上传失败，请手动上传临时文件。")
        pass


def download_video(session, url):
    class Logger(object):
        @staticmethod
        def debug(msg):
            if 'Deleting' in msg:
                video_info = download_list[session.event.message_type + ':' + str(session.event.user_id) + ':' + str(session.event.message_id)]
                if '.flv' in msg or '.m4a' in msg:
                    if video_info[0] != 'uploading':
                        video_info[0] = 'uploading'
                    send_message_auto(session, '成功转码视频：“' + video_info[3] + '”，开始上传到OneDrive')
                    upload_video(session, video_info)

        @staticmethod
        def warning(msg):
            print('Warning: ' + msg)
            nonebot.get_bot().sync.send_private_msg(user_id=1135989508, message="Warning: " + msg)

        @staticmethod
        def error(msg):
            print('Error: ' + msg)
            nonebot.get_bot().sync.send_private_msg(user_id=1135989508, message="Error: " + msg)

    def tracker(data):
        if data['status'] == 'downloading':
            video_info = download_list[session.event.message_type + ':' + str(session.event.user_id) + ':' + str(session.event.message_id)]
            if video_info[0] != 'downloading':
                video_info[0] = 'downloading'
            video_info[1] = data['_percent_str']
        if data['status'] == 'finished':
            if '.flv' in data['filename'] or '.m4a' in data['filename']:
                video_info = download_list[session.event.message_type + ':' + str(session.event.user_id) + ':' + str(session.event.message_id)]
                if video_info[0] != 'converting':
                    video_info[0] = 'converting'
                send_message_auto(session, '成功下载视频：“' + video_info[3] + '”，开始转码')

    print("Start Downloading...")
    now_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    options = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'progress_hooks': [tracker],
        'logger': Logger(),
        'merge_output_format': 'mp4',
        'postprocessors': [
            {
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4'
            }
        ],
        'outtmpl': f'../caches/{now_time}.%(ext)s',
    }
    with youtube_dlc.YoutubeDL() as yt_dlc:
        info_dict = yt_dlc.extract_info(url, download=False)
        download_list[session.event.message_type + ':' + str(session.event.user_id) + ':' + str(session.event.message_id)] = ['Waiting',
                                                                                                                              '  0.0%',
                                                                                                                              now_time,
                                                                                                                              info_dict['title'],
                                                                                                                              info_dict['uploader_id']]
    with youtube_dlc.YoutubeDL(options) as yt_dlc:
        yt_dlc.download([url])


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
        download_thread = threading.Thread(target=download_video, args=(session, args[0]))
        download_thread.start()

        with youtube_dlc.YoutubeDL() as yt_dlc:
            info_dict = yt_dlc.extract_info(args[0], download=False)
            session.finish(message="视频：“" + info_dict['title'] + "”加入下载队列")
        return

    session.pause('扒源 指令仅支持 1 个参数')


@queue.args_parser
async def _(session: CommandSession):
    args = session.current_arg_text.strip().split()

    if len(args) == 0:
        response = '下载队列：\n'
        for video_info in download_list:
            print(video_info)
            response += '| 视频名：' + str(video_info[3]) + ' | ' + str(video_info[0]) + ' | ' + str(video_info[1]) + ' | 开始时间：' + str(video_info[2]) + ' |\n'
        session.state['res'] = response
        return
    session.pause('任务列表 指令仅支持 0 个参数')
