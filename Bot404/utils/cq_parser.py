"""
CQ Code Parser
"""


# AT
def cq_at_parser(user_id):
    return '[CQ:at,qq={}]'.format(str(user_id))


# 图片
def cq_image_parser(file_path):
    return f'[CQ:image,file={file_path}]'


# Emoji表情
def cq_emoji_parser(emoji_id):
    return f'[CQ:emoji,id={emoji_id}]'


# QQ表情
def cq_face_parser(face_id):
    return f'[CQ:face,id={face_id}]'


# 语音
def cq_record_parser(file_path):
    return f'[CQ:record,file={file_path}]'


# 猜拳
def cq_rps_parser():
    return f'[CQ:rps]'


# 掷骰子
def cq_dice_parser():
    return f'[CQ:dice]'


# 戳一戳
def cq_shake_parser():
    return f'[CQ:shake]'


# 分享链接
def cq_share_parser(url, title):
    return f'[CQ:share,url={url},title={title}]'


# 位置
def cq_location_parser(latitude, longitude):
    return f'[CQ:location,latitude={latitude},longitude={longitude}]'


# 音乐
def cq_music_parser(url, audio_url, title):
    return f'[CQ:music,url={url},audio={audio_url},title={title}]'
