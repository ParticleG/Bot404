from nonebot import on_command, CommandSession
from hashlib import md5

from Bot404.configs import *
from Bot404.utils.cq_utils import *
from Bot404.utils.cq_parser import *

import numpy as np
import matplotlib.pyplot as plt
import datetime
import base64
import io


@on_command('ping', only_to_me=False, shell_like=True)
async def ping(session: CommandSession):
    args = session.current_arg_text.strip().split()
    if len(args) == 0:
        await send_message_async(session, 'Pong!')


async def radar_maker(values, radar_type):
    # 中文和负号的正常显示
    plt.rcParams['font.sans-serif'] = 'Microsoft YaHei'
    plt.rcParams['axes.unicode_minus'] = False
    # 使用ggplot的风格绘图
    plt.style.use('ggplot')
    feature = {
        'normal': [
            "阅读书籍", "追剧看番", "欣赏音乐", "享受美食",
            "游戏娱乐", "社交水群", "工作学习", "运动健身",
            "逛街购物", "走亲访友", "出行旅游", "研究整活"
        ],
        'translate': [
            "剪辑", "时轴", "翻译", "校对",
            "美工", "后期", "击剑", "杂务"
        ],
        'code': [
            "网站端", "服务端", "桌面端", "移动端",
            "底层工具", "脚本", "人工智能", "大数据",
            "工业控制", "数据库", "游戏开发", "信息安全"
        ]
    }
    section_count = len(feature[radar_type])
    values = values[0:section_count]
    # 设置雷达图的角度，用于平分切开一个平面
    angles = np.linspace(0, 2 * np.pi, section_count, endpoint=False)
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
    ax.set_thetagrids(np.arange(0.0, 360.0, (360.0 / section_count)), feature[radar_type])
    # 设置极轴范围
    ax.set_ylim(0, 100)
    # 添加标题
    plt.title('今日干劲')
    # 增加网格纸
    ax.grid(True)
    pic_io_bytes = io.BytesIO()
    plt.savefig(pic_io_bytes, format='png')
    pic_io_bytes.seek(0)
    pic_hash = 'base64://' + str(base64.b64encode(pic_io_bytes.read()))[2:-1]
    plt.close()
    return pic_hash


@on_command('motivation',
            aliases=('rp', 'gj', '人品', '干劲'),
            only_to_me=False,
            shell_like=True)
async def motivation(session: CommandSession):
    args = session.current_arg_text.strip().split()
    if len(args) == 0:
        motivation_list = [0] * 16
        user_md5 = md5(
            str(
                str(session.event.user_id) + datetime.date.today().isoformat()
            ).encode('utf-8')
        ).hexdigest()

        for index in range(16):
            temp_motivation_str = user_md5[2 * index:2 * (index + 1)]
            motivation_list[index] = np.ceil(
                int(temp_motivation_str, base=16) / 255.0 * 100.0
            )

        user_luck = np.round(np.average(motivation_list), 2)
        if user_luck >= 90:
            luck_str = "你今日的运势竟然是" + str(user_luck) + "分，惊了！这河里吗？"
        elif user_luck >= 80:
            luck_str = "你今日的运势高达" + str(user_luck) + "分。好！很有精神！"
        elif user_luck >= 60:
            luck_str = "你今日的运势有" + str(
                user_luck) + "分。不错，可以做加把劲骑士了"
        elif user_luck >= 40:
            luck_str = "你今日的运势有" + str(user_luck) + "分。还行，洒洒水"
        elif user_luck == 22:
            luck_str = "你今日的运势是□□分。等爽哥结婚了一定发□□剑□□"
        elif user_luck >= 20:
            luck_str = "你今日的运势有" + str(user_luck) + "分。遇到困难，睡大觉"
        elif user_luck > 10:
            luck_str = "你今日的运势只有" + str(user_luck) + "分。幸福往往是摸得透彻，而敬业的心却常常隐藏"
        else:
            luck_str = "你今日的运势居然只有" + str(user_luck) + "分。输的彻底"
        motivation_type = 'normal'
        for temp_group in GROUPS:
            if session.event.message_type == 'private':
                break
            elif session.event.group_id == temp_group["group"]:
                motivation_type = temp_group["type"]
                break

        motivation_figure = cq_at_parser(session.event.user_id) + luck_str + cq_image_parser(
            await radar_maker(motivation_list, motivation_type)
        )
        await send_message_async(session, motivation_figure)


@on_command('couple',
            aliases=('cp', '今日CP', 'CP'),
            only_to_me=False,
            shell_like=True)
async def couple(session: CommandSession):
    args = session.current_arg_text.strip().split()
    if len(args) == 0:
        # noinspection PyBroadException
        try:
            group_member_list = await session.bot.get_group_member_list(group_id=session.event.group_id)
            user_md5 = md5(
                str(
                    str(session.event.user_id) + datetime.date.today().isoformat()
                ).encode('utf-8')
            ).hexdigest()
            user_str = cq_at_parser(session.event.user_id)
            couple_user_id = group_member_list[int(user_md5, base=16) % len(group_member_list)]['user_id']
            couple_user_str = cq_at_parser(couple_user_id)
            response = user_str + '你没有今日CP，快和VTB贴贴去吧！'
            if couple_user_id == session.event.user_id:
                for temp_group in GROUPS:
                    if session.event.group_id == temp_group['group'] and temp_group['channel'] is not None:
                        response = f'{user_str}你没有今日CP，快和{temp_group["nickname"]}贴贴去吧！'
                        break
            else:
                response = user_str + '你的今日CP是：' + couple_user_str + '，贴贴~'

            await send_message_async(session, response)

        except Exception:
            exception_handler("获取群成员列表失败", logging.WARNING, False, session.event.group_id)


@on_command('command',
            aliases=('cm', '命令列表', '命令'),
            only_to_me=False,
            shell_like=True)
async def command(session: CommandSession):
    response = '''可用命令列表：
#[download|get|dl|扒|扒源] {url}
   *1个参数：视频链接*  扒源并自动上传到对应组的OneDrive扒源文件夹
#[queue|qu|任务列表|队列]
   *0个参数*  查看当前扒源队列
#[motivation|rp|gj|人品|干劲]
   *0个参数*  查看今日干劲
#[couple|cp|今日CP|CP]
   *0个参数* 查看今日CP
#[command|cm|命令列表|命令]
   *0个参数* 查看本命令列表
注：[]内的|代表触发关键词可替换；{}代表占位符，使用时要按需输入实际内容
'''
    await send_message_async(session, response)
