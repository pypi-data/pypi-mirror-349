from .channel import Channel
from .user import User
from .message import Message

class Msg:
  def __init__(self, message_data, client, interaction=False):
    self.id = message_data['id']
    self._JSON = message_data
    self.content = message_data.get('content', None)
    self.message = Message(message_data, client)
    self.author = User(message_data.get('author', message_data.get('member').get('user')), client)
    self.channel = Channel(message_data['channel_id'], client)
    self._client = client
    if interaction:
      self._deferred = False
      self._responded = False
      self._interaction = interaction
      self._token: str = message_data['token']
      self.version: int = message_data['version']

  async def defer(self, *, ephemeral: bool = False, thinking: bool = True):
    if self._responded or self._deferred:
      return
    response_type = 5
    data = {}
    if ephemeral:
      data['flags'] = 64
    await self._client.http.create_interaction_response(
      interaction_id=self.interaction.id,
      interaction_token=self.interaction.token,
      response_type=response_type,
      data=data if data else None
    )
    self._deferred = True
    self._responded = True

  async def remove(self):
    return await self.channel.remove_message(self.id)
    
  async def send(self, content=None, embed=None, embeds=None, ephemeral=False):
    return await self.channel.send(content=content, embed=embed, embeds=embeds, ephemeral=ephemeral)

  async def reply(self, content=None, embed=None, embeds=None, ephemeral=False):
    if _interaction:
      self._responded = True
    return await self.channel.send(content=content, embed=embed, embeds=embeds, reference=self.id, ephemeral=False, interaction_token=_token)