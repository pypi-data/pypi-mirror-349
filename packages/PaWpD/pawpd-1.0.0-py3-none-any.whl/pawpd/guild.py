class Guild:
  def __init__(self, guild_data, client):
    self.id = guild_data.get("id", None)
    self.name = guild_data.get("name", None)
    self.members = guild_data.get("members", None)
    self.channels = guild_data.get("channels", None)
    self.member_count = guild_data.get("member_count", None)
    #self.categories = guild_data["categories"]