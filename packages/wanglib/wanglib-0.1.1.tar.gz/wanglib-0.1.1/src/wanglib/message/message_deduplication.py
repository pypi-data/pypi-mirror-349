from . import message_cache


def message_deduplication(message_id: int | str):
    """
    消息去重
    """
    # 通过缓存消息的消息id进内存来判断消息是否重复
    # 如果消息id已经存在于缓存中则返回False
    # 否则返回True
    if message_cache.get(str(message_id)) is None:
        message_cache.set(str(message_id), 1)
        return True
    return False
