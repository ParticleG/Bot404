from __future__ import unicode_literals
from nonebot import on_command, CommandSession
import nonebot
import asyncio
import youtube_dlc
# import threading
import datetime
import shutil
import re
import traceback

bot = nonebot.get_bot()

'''

{
    url:{
        status,
        group
        info
        progress
    }
}

##########
# Status #
##########

- received(Extracting)
- extracted(Downloading)
- downloaded(Converting)
- converted(Uploading)
- uploaded(Verifying)
- verified(Send message, remove status cache)
'''

queue_status = {}


class Logger(object):
    @staticmethod
    def debug(msg):
        pass
        # if 'Deleting' in msg:
        #     video_info = download_list[session.event.message_type + ':' +
        #                                str(session.event.user_id) + ':' +
        #                                str(session.event.message_id)]
        #     if '.flv' in msg or '.m4a' in msg:
        #         if video_info[0] != 'uploading':
        #             video_info[0] = 'uploading'
        #         send_message_auto(
        #             session,
        #             '成功转码视频：“' + video_info[3] + '”，开始上传到OneDrive')
        #         upload_video(session, video_info)

    @staticmethod
    def warning(msg):
        print('Warn: ' + msg)
        pass
        # print('Warning: ' + msg)
        # bot.sync.send_private_msg(user_id=1135989508,
        #                           message="Warning: " + msg)

    @staticmethod
    def error(msg):
        print('Error: ' + msg)
        # bot.sync.send_private_msg(user_id=1135989508,
        #                           message="Error: " + msg)

    pass


class DlError(Exception):
    def __int__(self, msg):
        self.msg = msg

    def __repr__(self):
        return repr(self.msg)

    def __str__(self):
        return str(self.msg)


class ExtractError(DlError):
    def __str__(self):
        return str("[ExtractERROR]An Error Occurred:" + self.msg)


class DownloadError(DlError):
    def __str__(self):
        return str("[DownloadERROR]An Error Occurred:" + self.msg)


class ConvertError(DlError):
    def __str__(self):
        return str("[ConvertERROR]An Error Occurred:" + self.msg)


class UploadError(DlError):
    def __str__(self):
        return str("[UploadERROR]An Error Occurred:" + self.msg)


class VerifyError(DlError):
    def __str__(self):
        return str("[VerifyERROR]An Error Occurred:" + self.msg)


def cq_at_parser(user_id):
    return "[CQ:at,qq=" + str(user_id) + "]"


async def video_info_extract(url):
    try:
        with youtube_dlc.YoutubeDL({}) as yt_dlc:
            queue_status[url]['info'] = dict(yt_dlc.extract_info(url, download=False))
        print("[DEBUG][EXTRACT]INFO={}".format(queue_status[url]['info']))
    except ExtractError:
        print(str(ExtractError))


async def video_preprocess(url, group):
    try:
        if url in queue_status.keys():
            await bot.send_group_msg(group_id=group, message=f"本视频正在下载中，命令已由{queue_status[url]['group']}执行，请勿重复操作。")
            raise VerifyError("重复下载")
        else:
            await bot.send_group_msg(group_id=group, message=f"正在开始下载{url}...")
            queue_status[url] = {
                'status': 'received',
                'group': group,
                'info': {}
            }
    except VerifyError:
        print("[DEBUG][PREPROCESS]{}".format(str(VerifyError)))
    except Exception as e:
        print(e.args)
        print(traceback.format_exc())
    print("[DEBUG][PREPROCESS]STATUS={}".format(str(queue_status[url])))
    return


async def video_download(url):
    now_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    def tracker(data):
        if data['status'] == 'downloading':
            queue_status[url]['progress'] = data['_percent_str']
        if data['status'] == 'finished':
            queue_status[url]['status'] = 'downloaded'

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
            f'../caches/{now_time}.%(ext)s',
    }
    try:
        await bot.send_group_msg(message=f"正在下载：{queue_status[url]['info']['title']}",
                                 group_id=queue_status[url]['group'])
        with youtube_dlc.YoutubeDL(options) as yt_dlc:
            yt_dlc.download([url])
    except Exception:
        # print("Face Problem when Downloading.", str(Exception))
        await bot.send_private_msg(
            user_id=1135989508,
            message="Face Problem when Downloading.")
        raise DownloadError("Download Error Occurred.")


async def video_mount(url):
    video_info = queue_status[url]['info']
    current_group = queue_status[url]['group']
    new_filename = re.sub(r'[\\/:*?"<>|]', '_', video_info[3])

    print('[DEBUG][MOUNT]Group={},old={},filename={}'.format(current_group, video_info[2], new_filename))

    if video_info[4] == 'UCoSrY_IQQVpmIRZ9Xf-y93g':
        shutil.copy(f'/usr/go-cqhttp/quin33/caches/{video_info[2]}.mp4',
                    f'/usr/drive/holoen/gura/{new_filename}.mp4')
        await bot.send_group_msg(group_id=current_group, message='成功上传视频：“' + video_info[3] + '”到Gura组盘')
    elif video_info[4] == 'UCyl1z3jo3XHR1riLFKG5UAg':
        shutil.copy(f'/usr/go-cqhttp/quin33/caches/{video_info[2]}.mp4',
                    f'/usr/drive/holoen/amelia/{new_filename}.mp4')
        await bot.send_group_msg(group_id=current_group, message='成功上传视频：“' + video_info[3] + '”到Amelia组盘')
    elif video_info[4] == 'UCMwGHR0BTZuLsmjY_NT5Pwg':
        shutil.copy(f'/usr/go-cqhttp/quin33/caches/{video_info[2]}.mp4',
                    f'/usr/drive/holoen/ina/{new_filename}.mp4')
        await bot.send_group_msg(group_id=current_group, message='成功上传视频：“' + video_info[3] + '”到Ina组盘')
    elif video_info[4] == 'UCHsx4Hqa-1ORjQTh9TYDhww':
        shutil.copy(f'/usr/go-cqhttp/quin33/caches/{video_info[2]}.mp4',
                    f'/usr/drive/holoen/kiara/{new_filename}.mp4')
        await bot.send_group_msg(group_id=current_group, message='成功上传视频：“' + video_info[3] + '”到Kiara组盘')
    elif video_info[4] == 'UCL_qhgtOy0dy1Agp8vkySQg':
        shutil.copy(f'/usr/go-cqhttp/quin33/caches/{video_info[2]}.mp4',
                    f'/usr/drive/holoen/callio/{new_filename}.mp4')
        await bot.send_group_msg(group_id=current_group, message='成功上传视频：“' + video_info[3] + '”到Callio组盘')
    else:
        shutil.copy(f'/usr/go-cqhttp/quin33/caches/{video_info[2]}.mp4',
                    f'/usr/drive/holoen/others/{new_filename}.mp4')
        await bot.send_group_msg(group_id=current_group, message='成功上传视频：“' + video_info[3] + '”到Others盘')


async def video_verify(url):
    print("[DEBUG][VERIFY]Status={}".format(queue_status(url)))
    if queue_status[url]['status'] == 'uploaded':
        await bot.send_group_msg(group_id=queue_status[url]['group'],
                                 message=f"{queue_status[url]['info']['title']}完成下载，已从队列中移除。")
        del queue_status[url]
    else:
        await bot.send_group_msg(group_id=queue_status[url]['group'],
                                 message=f"{queue_status[url]['info']['title']}出现错误未能下载，将从队列中移除，请检查后重试。")
        del queue_status[url]


@on_command("get", aliases=("DL", "dl", "下载", "扒源", "扒"), only_to_me=False)
async def get(session: CommandSession):
    video_url = session.current_arg.strip()
    if session.event.message_type != 'group':
        await session.send("暂时仅支持群聊，请在群内使用本命令")
        return
    else:
        group = session.event.group_id
    # 具体使用何种Key值需再优化
    try:
        print("[DEBUG][SESSION]URL={}, GROUP={}".format(video_url, group))
        await video_preprocess(video_url, group)
        # await asyncio.sleep(0.5)
        await video_info_extract(video_url)
        # await asyncio.sleep(0.5)
        await video_download(video_url)
        # await asyncio.sleep(0.5)
        await video_mount(video_url)
        # await asyncio.sleep(0.5)
        await video_verify(video_url)
        pass
    except ExtractError:
        # await asyncio.sleep(0.5)
        await session.send(str(ExtractError))
    except DownloadError:
        # await asyncio.sleep(0.5)
        await session.send(str(DownloadError))
    except UploadError:
        # await asyncio.sleep(0.5)
        await session.send(str(UploadError))
    except ConvertError:
        # await asyncio.sleep(0.5)
        await session.send(str(ConvertError))
    else:
        await session.send("下载过程中发生错误，故下载过程已暂停，请联系管理员检查后再次尝试。")
    return


@on_command("queue", aliases=('qu', '任务列表', '队列'), only_to_me=False)
async def queue(session: CommandSession):
    # nonlocal queue_status
    target = session.current_arg.strip().split()
    # #queue url
    if len(target) > 1:
        await session.send("参数过多")
    elif len(target) == 0:
        print("[Debug]", str(queue_status))
        for k, v in queue_status.items():
            pass
        await session.send(str(queue_status))
    else:
        if target[1] in queue_status.keys():
            print("[Debug]", str(queue_status[target[1]]))
            await session.send(str(queue_status[target[1]]))
        else:
            await session.send("目标URL不在当前队列内，请检查！")
    return
