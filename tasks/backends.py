import json

from channels.backends.redis_py import RedisChannelBackend


class PublishingRedisChannelBackend(RedisChannelBackend):
    u"""
    If a message is sent on a psecially prefixed channel ("PUB:"), publishes it instead...
    """
        
    def send(self, channel, message):
        if channel.startswith("PUB:"):
            self.connection.publish(self.prefix + channel,json.dumps(message))
        else:
            super(PublishingRedisChannelBackend, self).send(channel, message)
