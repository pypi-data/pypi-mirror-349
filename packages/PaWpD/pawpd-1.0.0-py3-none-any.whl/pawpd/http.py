from typing import Any, Callable, Dict, List, Optional, Union
import aiohttp

class HTTPClient:
  def __init__(self, token: str, client):
    self.client = client
    self.token = token
    self.session = None

  async def _get_session(self):
    self.session = aiohttp.ClientSession()
    self.client.logger.info("Aiohttp Session started")

  async def _close_session(self):
    await self.session.close()
    self.client.logger.info("Aiohttp Session stopped")

  async def request(self, method: str, path: str, json_payload: Optional[Dict] = None) -> Any:
    path = f"https://discord.com/api/v10{path}"
    if method == "GET":
      async with self.session.get(path, headers={'Authorization': f'Bot {self.token}', 'Content-Type': 'application/json'}) as response:
        data = await response.json()
    elif method == "POST":
      async with self.session.post(path, headers={'Authorization': f'Bot {self.token}', 'Content-Type': 'application/json'}, json=json_payload) as response:
        data = await response.json()
    elif method == "DELETE":
      async with self.session.delete(path, headers={'Authorization': f'Bot {self.token}', 'Content-Type': 'application/json'}) as response:
        data = await response.json()
    elif method == "PUT":
      async with self.session.put(path, headers={'Authorization': f'Bot {self.token}', 'Content-Type': 'application/json'}, json=json_payload) as response:
        data = await response.json()
    else:
      return []
    if response.status == 200:
      return data
    if response.sttaus == 204:
      return
    else:
      raise Exception(f"HTTP Error: {response.status}")

  async def bulk_override_global_commands(self, application_id: str, commands_payload: List[Dict]) -> List[Dict]:
    return await self.request("PUT", f"/applications/{application_id}/commands", json_payload=commands_payload)

  async def create_interaction_response(self, interaction_id: str, interaction_token: str, response_type: int, data: Optional[Dict]):
    return await self.request('POST', f'/interactions/{interaction_id}/{interaction_token}/callback', json_payload=data)

  async def create_followup_message(self, application_id: str, interaction_token: str, data: Dict) -> Dict:
    return await self.request('POST', f'/webhooks/{application_id}/{interaction_token}', json_payload=data)

  async def bulk_override_guild_commands(self, application_id: str, guild_id: int, commands_payload: List[Dict]) -> List[Dict]:
    return await self.request("PUT", f"/applications/{application_id}/guilds/{guild_id}/commands", json_payload=commands_payload)