class Embed:
  def __init__(self, title="", description="", color=0):
    self.title = title
    self.description = description
    self.color = color
    self.fields = []
    self.footer_text = None
    self.footer_icon = None
    self.author_name = None
    self.author_url = None
    self.author_icon = None

  def add_field(self, name, value, inline=False):
    self.fields.append({"name": name, "value": value, "inline": inline})

  def set_footer(self, text, icon_url=None):
    self.footer_text = text
    self.footer_icon = icon_url

  def set_author(self, author, url=None, icon_url=None):
    self.author_name = author
    self.author_url = url
    self.author_icon = icon_url

  def to_dict(self):
    return {"title": self.title, "description": self.description, "color": self.color, "author": {"name": self.author_name, "url": self.author_url, "icon_url": self.author_icon}, "footer": {"text": self.footer_text, "icon_url": self.footer_icon}, "fields": self.fields}