import json

from channels.backends.redis_py import RedisChannelBackend


class PubSubRedisChannelBackend(RedisChannelBackend):
    u"""
    If a message is sent on a specially prefixed channel, publishes it instead of sending it.
    Also subscribes to all channels (specially prefixed) and receives messages from there too.
    """

    def __init__(self, *args, **kwargs):
        self.pub_prefix = kwargs.pop('pub_prefix','PUB:')
        self.sub_prefix = kwargs.pop('sub_prefix','SUB:')
        super(PubSubRedisChannelBackend, self).__init__(*args,**kwargs)

    _pubsub = None
    
    def __del__(self):
        if self._pubsub:
            self._pubsub.unsubscribe()
        super(PubSubRedisChannelBackend, self).__del__()
            
    @property
    def pubsub(self):
        if not self._pubsub:
            self._pubsub = self.connection.pubsub(ignore_subscribe_messages=True)
            self._pubsub.subscribe([self.prefix + self.sub_prefix + channel for channel in self.registry.all_channel_names()])
        return self._pubsub 
           
    def send(self, channel, message):
        if channel.startswith(self.pub_prefix):
            self.connection.publish(self.prefix + channel,json.dumps(message))
        else:
            super(PubSubRedisChannelBackend, self).send(channel, message)

    def receive_many(self, channels):
        u"""
        Copied from the superclass and enhanced with getting published messages. 
        """
        if not channels:
            raise ValueError("Cannot receive on empty channel list!")
        res = (None, None)
        while True:
            message = self.pubsub.get_message()       #peek at subscribed channels
            if message and message.get('type',None) in ['message','pmessage']:
                try:
                    res = (message.get('channel','')[len(self.prefix + self.sub_prefix):],json.loads(message.get('data',None)))
                    break
                except:
                    #log error and ignore it!!!
                    pass              
            result = self.connection.blpop([self.prefix + channel for channel in channels], timeout=1)
            if result:
                content = self.connection.get(result[1])
                if content is None:
                    continue
                res = (result[0][len(self.prefix):], json.loads(content))
                break
            else:
                break
        return res
