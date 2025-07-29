class Channel:
  def __init__(self, channel_id, client):
    self.id = channel_id
    self._client = client
    self.session = client.http.session

  async def remove_message(self, message_id):
    url = f'https://discord.com/api/v10/channels/{self.id}/messages/{message_id}'
    headers = {
      'Authorization': f'Bot {self._client.token}',
      'Content-Type': 'application/json',
    }
    async with self.session.delete(url, headers=headers) as response:
      return await response.json()
  
  async def send(self, content=None, embed=None, reference=None, embeds=None, ephemeral=False, interaction_token=None):     
    url = f'https://discord.com/api/v10/channels/{self.id}/messages'
    headers = {
      'Authorization': f'Bot {self._client.token}',
      'Content-Type': 'application/json',
    }
    actual_embeds = []
    if embed:
      actual_embeds.append(embed)
    if embeds:
      actual_embeds.extend(embeds)
    payload = {
      'content': str(content) if content else None,
      "embeds": [e.to_dict() for e in actual_embeds if hasattr(e, 'to_dict')],
      'message_reference': {'message_id': reference} if reference else None
    }
    if ephemeral:
      payload['flags'] = 64
    if reference:
      message_data = await self._client.http.create_followup_message(
        application_id=_client.id,
        interaction_token=interaction_token,
        data=payload
      )
      if message_data:
        return message_data
    async with self.session.post(url, headers=headers, json=payload) as response:
      return await response.json()