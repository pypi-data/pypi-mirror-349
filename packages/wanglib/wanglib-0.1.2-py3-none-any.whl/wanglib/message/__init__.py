from ..cache import CacheManager
from .bot_message import message_deduplication

message_cache = CacheManager("message", 512)  # 消息缓存，这个缓存被用于消息去重，防止重复发送消息
