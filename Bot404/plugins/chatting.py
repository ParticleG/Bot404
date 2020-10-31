import numpy as np
import matplotlib.pyplot as plt
from nonebot import on_command, CommandSession
# from Bot404.utils.cq_utils import *
from Bot404.utils.cq_parser import *
from hashlib import md5
import datetime
import base64
import io


# import re


@on_command('ping', only_to_me=False, shell_like=True)
async def ping(session: CommandSession):
    await session.send('Pong!')


@on_command('jrrp',
            aliases=('rp', '今日人品', '人品'),
            only_to_me=False,
            shell_like=True)
async def jrrp(session: CommandSession):
    try:
        args = session.current_arg_text.strip().split()
        response = '"人品满点！芜湖~"'
        if not len(args):
            user_str = str(session.event.user_id) + datetime.date.today().isoformat()
            user_md5 = md5(user_str.encode('utf-8')).hexdigest()
            user_luck = int(user_md5, base=16) % 101
            if user_luck == 100:
                response = cq_at_parser(session.event.user_id) + "你今日的运势竟然是" + str(user_luck) + "分，惊了！这河里吗？"
            elif user_luck >= 80:
                response = cq_at_parser(session.event.user_id) + "你今日的运势高达" + str(user_luck) + "分。好！很有精神！"
            elif user_luck >= 60:
                response = cq_at_parser(session.event.user_id) + "你今日的运势有" + str(
                    user_luck) + "分。不错，可以做加把劲骑士了"
            elif user_luck >= 40:
                response = cq_at_parser(session.event.user_id) + "你今日的运势有" + str(user_luck) + "分。还行，洒洒水"
            elif user_luck == 22:
                response = cq_at_parser(session.event.user_id) + "你今日的运势是□□分。等爽哥结婚了一定发□□剑□□"
            elif user_luck >= 20:
                response = cq_at_parser(session.event.user_id) + "你今日的运势有" + str(user_luck) + "分。遇到困难，睡大觉"
            elif user_luck > 0:
                response = cq_at_parser(session.event.user_id) + "你今日的运势只有" + str(
                    user_luck) + "分。幸福往往是摸得透彻，而敬业的心却常常隐藏"
            else:
                response = cq_at_parser(session.event.user_id) + "你今日的运势居然只有" + str(user_luck) + "分。输的彻底"

        await session.send(response)
    except Exception:
        print("[JRRP ERROR OCCURRED]")
        await session.send("人品满点！芜湖~")


async def radar_maker(values):
    # 中文和负号的正常显示
    plt.rcParams['font.sans-serif'] = 'Microsoft YaHei'
    plt.rcParams['axes.unicode_minus'] = False
    # 使用ggplot的风格绘图
    plt.style.use('ggplot')
    # 构造数据
    # values = [80, 20, 10, 50, 10, 64]
    feature = ['时轴', '翻译', "校对", "剪辑", "美工", "后期"]
    N = len(values)
    # 设置雷达图的角度，用于平分切开一个平面
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False)
    # 使雷达图封闭起来
    values = np.concatenate((values, [values[0]]))
    angles = np.concatenate((angles, [angles[0]]))
    # 绘图
    fig = plt.figure()
    # 设置为极坐标格式
    ax = fig.add_subplot(111, polar=True)
    # 绘制折线图
    ax.plot(angles, values, 'o-', linewidth=2, label='干劲')
    ax.fill(angles, values, 'r', alpha=0.5)
    # 添加每个特质的标签
    ax.set_thetagrids(np.arange(0.0, 360.0, 60.0), feature)
    # 设置极轴范围
    ax.set_ylim(0, 100)
    # 添加标题
    plt.title('今日干劲')
    # 增加网格纸
    ax.grid(True)
    pic_IO_bytes = io.BytesIO()
    plt.savefig(pic_IO_bytes, format='png')
    pic_IO_bytes.seek(0)
    pic_hash = 'base64://' + str(base64.b64encode(pic_IO_bytes.read()))[2:-1]
    plt.close()
    return pic_hash


@on_command('motivation',
            aliases=('jrgj', '今日干劲', '干劲'),
            only_to_me=False,
            shell_like=True)
async def motivation(session: CommandSession):
    try:
        args = session.current_arg_text.strip().split()
        pic = "今天也是干劲满满呢！"
        if not len(args):
            user_str = str(session.event.user_id) + datetime.date.today().isoformat()
            user_md5 = md5(user_str.encode('utf-8')).hexdigest()
            pic = cq_at_parser(session.event.user_id) + cq_image_parser(
                await radar_maker(
                    [
                        int(user_md5[:-4], base=16) % 101,
                        int(user_md5[:-6], base=16) % 101,
                        int(user_md5[:-8], base=16) % 101,
                        int(user_md5[:-10], base=16) % 101,
                        int(user_md5[:-12], base=16) % 101,
                        int(user_md5[:-14], base=16) % 101
                    ]
                )
            )

        await session.send(pic)
    except Exception:
        print("[JRGJ ERROR OCCURRED]")
        await session.send("今天也是干劲满满呢！")


@on_command('jrcp',
            aliases=('cp', '今日CP', 'CP'),
            only_to_me=False,
            shell_like=True)
async def jrcp(session: CommandSession):
    try:
        args = session.current_arg_text.strip().split()
        cp = '未找到对象'
        if not len(args):
            group_member_list = await session.bot.get_group_member_list(group_id=session.event.group_id)
            user_str = str(session.event.user_id) + datetime.date.today().isoformat()
            user_md5 = md5(user_str.encode('utf-8')).hexdigest()
            user_couple = int(user_md5, base=16) % len(group_member_list)
            if group_member_list[user_couple]['user_id'] == session.event.user_id:
                if session.event.group_id == 901231107:
                    cp = cq_at_parser(session.event.user_id) + '你没有今日CP，快和Gura贴贴去吧！'
                elif session.event.group_id == 829619725:
                    cp = cq_at_parser(session.event.user_id) + '你没有今日CP，快和Amelia贴贴去吧！'
                elif session.event.group_id == 203690749:
                    cp = cq_at_parser(session.event.user_id) + '你没有今日CP，快和Ina贴贴去吧！'
                elif session.event.group_id == 643815033:
                    cp = cq_at_parser(session.event.user_id) + '你没有今日CP，快和Kiara贴贴去吧！'
                elif session.event.group_id == 826872326:
                    cp = cq_at_parser(session.event.user_id) + '你没有今日CP，快和Calliope贴贴去吧！'
                else:
                    cp = cq_at_parser(session.event.user_id) + '你没有今日CP，快和VTB贴贴去吧！'
            else:
                cp = cq_at_parser(session.event.user_id) + '你的今日CP是：' + cq_at_parser(
                    group_member_list[user_couple]['user_id']) + '，贴贴~'
        await session.send(cp)
    except Exception:
        print("[JRCP ERROR OCCURRED]")
        await session.send("未找到对象")


@on_command('command',
            aliases=('cm', '命令列表', '命令'),
            only_to_me=False,
            shell_like=True)
async def command(session: CommandSession):
    await session.send(
        '''可用命令列表：
#[download|get|dl|扒|扒源] {url}
   *1个参数：视频链接*  扒源并自动上传到对应组的OneDrive扒源文件夹
#[queue|qu|任务列表|队列]
   *0个参数*  查看当前扒源队列
#[jrrp|rp|今日人品|人品]
   *0个参数*  检测今日人品
#[jrcp|cp|今日CP|CP]
   *0个参数* 查看今日CP
#[command|cm|命令列表|命令]
   *0个参数* 查看本命令列表
注：[]内的|代表触发关键词可替换；{}代表占位符，使用时要按需输入实际内容''')
