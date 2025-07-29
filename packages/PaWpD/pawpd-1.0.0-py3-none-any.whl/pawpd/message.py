from .channel import Channel
from .user import User
from .guild import Guild

class Message:
  def __init__(self, message_data, client):
    self.id = message_data['id']
    self._JSON = message_data
    self.guild_id = message_data["guild_id"]
    self.content = message_data.get('content')
    self.author = User(message_data.get('author', message_data.get('member').get('user')), client)
    self.channel = Channel(message_data['channel_id'], client)

  async def remove(self):
    return await self.channel.remove_message(self.id)
  
  async def reply(self, content=None, embed=None):
    return await self.channel.send(content, embed, reference=self.id)