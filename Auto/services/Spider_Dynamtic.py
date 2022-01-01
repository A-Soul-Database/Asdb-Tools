"""
    Bili动态爬取
    Version V2.0.0-alpha
"""
import datetime
def ParseClander(content):
    """
        日程表解析
        例https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/get_dynamic_detail?dynamic_id=609209877938177299
    """
    content = "Hello小伙伴们~12.20-12.26的日程表来咯！\n12月24日【A-SOUL夜谈】是在@乃琳Queen 直播间哦！\n12月25日【A-SOUL小剧场】是在@珈乐Carol 的直播间哦！\n12月26日【A-SOUL游戏室】是在@贝拉kira 的直播间哦！\nPS.12月23日嘉然单播为B站限定直播；"

    result = [fn for fn in content.split("\n") if any(keywords in fn for keywords in ["月","直播"]) and any(forbidden  not in fn  for forbidden in ["PS","直播间哦！"])]

    print(result)

ParseClander("")