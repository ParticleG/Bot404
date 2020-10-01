from nonebot import on_command, CommandSession
from hashlib import md5
import datetime


def _cq_at_parser(user_id):
    return "[CQ:at,qq=" + str(user_id) + "]"


@on_command('ping', only_to_me=False, shell_like=True)
async def ping(session: CommandSession):
    await session.send(session.get('res'))


@on_command('jrrp',
            aliases=('rp', '今日人品', '人品'),
            only_to_me=False,
            shell_like=True)
async def jrrp(session: CommandSession):
    await session.send(session.get('res'))


@on_command('jrcp',
            aliases=('cp', '今日CP', 'CP'),
            only_to_me=False,
            shell_like=True)
async def jrcp(session: CommandSession):
    await session.send(session.get('res'))


@ping.args_parser
async def _(session: CommandSession):
    args = session.current_arg_text.strip().split()
    print(args)

    if not len(args):
        session.state['res'] = "Pong!"
        return

    session.pause('Command: \"ping\" only support 0 argument.')


@jrrp.args_parser
async def _(session: CommandSession):
    args = session.current_arg_text.strip().split()

    if not len(args):
        user_str = str(
            session.event.user_id) + datetime.date.today().isoformat()
        user_md5 = md5(user_str.encode('utf-8')).hexdigest()
        user_luck = int(user_md5, base=16) % 101
        if user_luck == 100:
            session.state['res'] = _cq_at_parser(
                session.event.user_id) + "你今日的运势竟然是" + str(
                user_luck) + "分，惊了！这河里吗？"
        elif user_luck >= 80:
            session.state['res'] = _cq_at_parser(
                session.event.user_id) + "你今日的运势高达" + str(
                user_luck) + "分。好！很有精神！"
        elif user_luck >= 60:
            session.state['res'] = _cq_at_parser(
                session.event.user_id) + "你今日的运势有" + str(
                user_luck) + "分。不错，可以做加把劲骑士了"
        elif user_luck >= 40:
            session.state['res'] = _cq_at_parser(
                session.event.user_id) + "你今日的运势有" + str(
                user_luck) + "分。还行，洒洒水"
        elif user_luck == 22:
            session.state['res'] = _cq_at_parser(
                session.event.user_id) + "你今日的运势是□□分。等爽哥结婚了一定发□□剑□□"
        elif user_luck >= 20:
            session.state['res'] = _cq_at_parser(
                session.event.user_id) + "你今日的运势有" + str(
                user_luck) + "分。遇到困难，睡大觉"
        elif user_luck > 0:
            session.state['res'] = _cq_at_parser(
                session.event.user_id) + "你今日的运势只有" + str(
                user_luck) + "分。幸福往往是摸得透彻，而敬业的心却常常隐藏"
        else:
            session.state['res'] = _cq_at_parser(
                session.event.user_id) + "你今日的运势居然只有" + str(
                user_luck) + "分。输的彻底"
        return

    session.pause('Command: \"jrrp\" only support 0 argument.')


@jrcp.args_parser
async def _(session: CommandSession):
    args = session.current_arg_text.strip().split()

    if not len(args):
        group_member_list = await session.bot.get_group_member_list(
            group_id=session.event.group_id)
        user_str = str(
            session.event.user_id) + datetime.date.today().isoformat()
        user_md5 = md5(user_str.encode('utf-8')).hexdigest()
        user_couple = int(user_md5, base=16) % len(group_member_list)
        if group_member_list[user_couple]['user_id'] == session.event.user_id:
            if session.event.group_id == 901231107:
                session.state['res'] = _cq_at_parser(
                    session.event.user_id) + '你没有今日CP，快和Gura贴贴去吧！'
            elif session.event.group_id == 829619725:
                session.state['res'] = _cq_at_parser(
                    session.event.user_id) + '你没有今日CP，快和Amelia贴贴去吧！'
            elif session.event.group_id == 203690749:
                session.state['res'] = _cq_at_parser(
                    session.event.user_id) + '你没有今日CP，快和Ina贴贴去吧！'
            elif session.event.group_id == 643815033:
                session.state['res'] = _cq_at_parser(
                    session.event.user_id) + '你没有今日CP，快和Kiara贴贴去吧！'
            elif session.event.group_id == 826872326:
                session.state['res'] = _cq_at_parser(
                    session.event.user_id) + '你没有今日CP，快和Calliope贴贴去吧！'
            else:
                session.state['res'] = _cq_at_parser(
                    session.event.user_id) + '你没有今日CP，快和VTB贴贴去吧！'
        else:
            session.state['res'] = _cq_at_parser(
                session.event.user_id) + '你的今日CP是：' + _cq_at_parser(
                group_member_list[user_couple]['user_id']) + '，贴贴~'
        return

    session.pause('Command: \"jrcp\" only support 0 argument.')
