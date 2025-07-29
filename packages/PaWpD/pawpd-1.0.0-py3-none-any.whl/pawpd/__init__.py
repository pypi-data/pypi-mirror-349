import asyncio, time, aiohttp, logging, json, websockets, inspect
from typing import Any, Callable, Dict, List, Optional, Union
from .message import Message
from .msg import Msg
from . import intents
from .intents import all
from .embed import Embed
from .guild import Guild
from .user import User
from . import color as Color
from .http import HTTPClient
from enum import IntEnum

version = "1.0.0"

class ApplicationCommandOptionType(IntEnum):
    SUB_COMMAND = 1
    SUB_COMMAND_GROUP = 2
    STRING = 3
    INTEGER = 4
    BOOLEAN = 5
    USER = 6
    CHANNEL = 7
    ROLE = 8
    MENTIONABLE = 9
    NUMBER = 10
    ATTACHMENT = 11

class Command:
  def __init__(self, func, name, **attrs):
    self.func = func
    self.name = name or func.__name__
    self.params = attrs.get('params', {})
    self.description = attrs.get('description', None)
    self.slash = attrs.get('slash', False)
    self.guild_ids = attrs.get('guild_ids', [])
    self.hybrid = attrs.get('hybrid', False)
    self.aliases = attrs.get('aliases', [])
    self.help_text = attrs.get('help', None)

  async def invoke(self, context, *args, **kwargs):
    return await self.func(context, *args, **kwargs)

  def _get_param_type(self, annotation: Any) -> Optional[ApplicationCommandOptionType]:
    if annotation == str:
      return ApplicationCommandOptionType.STRING
    elif annotation == int:
      return ApplicationCommandOptionType.INTEGER
    elif annotation == bool:
      return ApplicationCommandOptionType.BOOLEAN
    elif annotation == float:
      return ApplicationCommandOptionType.NUMBER
    elif annotation == User:
      return ApplicationCommandOptionType.USER
    return None

  def to_application_command_payload(self) -> Optional[Dict[str, Any]]:
    """Converts this command into a Discord Application Command JSON payload."""
    if not self.slash:
      if not self.hybrid:
        return None

    payload_options: List[Dict[str, Any]] = []
    param_names = list(self.params.keys())
    if param_names and (param_names[0] == 'ctx' or param_names[0] == 'self'):
      actual_params = list(self.params.values())[1:]
    else:
      actual_params = list(self.params.values())

    for param in actual_params:
      if param.annotation == inspect.Parameter.empty:
        option_type = ApplicationCommandOptionType.STRING
        param_description = f"The {param.name} argument."
      else:
        option_type = self._get_param_type(param.annotation)
        if option_type is None:
          print(f"Warning: Could not map type {param.annotation} for param '{param.name}' in command '{self.name}'. Skipping.")
          continue
        param_description = f"Value for {param.name}."
        is_required = (param.default == inspect.Parameter.empty)

        payload_options.append({
          "name": param.name,
          "description": param_description,
          "type": option_type.value,
          "required": is_required,
          # "choices": [] # You'd handle choices here if supported
        })

    return {
      "name": self.name,
      "description": self.description if self.description else "No description provided.",
      "options": payload_options,
      # "type": 1, # CHAT_INPUT, default
      # "dm_permission": True, # Default
      # "default_member_permissions": None # For permission restricting
    }

class Client:
  def __init__(self, token, intents=None, prefix=None, builtin_help=True):
    self.token = token
    self.prefix = prefix
    self.event_handlers = {}
    self.commands = {}
    self.guilds = []
    self.user = None
    self.id = None
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    self.logger = logger
    self.http = HTTPClient(token=token, client=self)
    if intents == None:
      self.intents = all()
      self.logger.warn("Intents were not set! Using default Intents (all)")
    else:
      self.intents = intents
    if prefix == None:
      self.logger.warn("Prefix was not set! Bot commands won't be available!")
    if builtin_help:
      async def help_cmd(msg, page=0):
        help_embed = Embed(title="Help GUI", description=f"Commands Are specified down below \n **Page {page}**")
        fro = page*10 if not page*10 > len(self.commands) else int(len(self.commands)/10)
        to = page*10+10 if not page*10+10 > len(self.commands) else len(self.commands)
        commands_list = list(self.commands.keys())[fro:to]
        for command in commands_list:
          command = self.commands[command]
          help_embed.add_field(name=f"{command.name}", value=f"**Description:** {command.description} \n **Help:** {command.help_text}")
        global version
        help_embed.set_footer(text=f"PaWpD {version}")
        await msg.send(embed=help_embed)
      help_command = Command(help_cmd, "help")
      self.add_command(help_command)
    
  def add_command(self, command: Command):
    if command.name in self.commands:
      self.logger.info(f"Warning: Command '{command.name}' is being overwritten.")
    self.commands[command.name] = command

  async def sync(self, *, guild_id: Optional[int] = None) -> List[Dict[str, Any]]:
    """
        Registers or updates application commands with Discord.

        Args:
            guild_id: If provided, syncs commands to this specific guild.
                      Otherwise, syncs globally.

        Returns:
            A list of the application command data as returned by Discord.
    """
    if not self.id:
      self.logger.error("Error: Bot id is not set. Cannot sync commands.")
      return []

    payloads_to_send: List[Dict[str, Any]] = []
    for cmd_name, command_obj in self.commands.items():
      if command_obj.slash == False:
        continue
      if command_obj.hybrid == False:
        continue 
      is_guild_specific_command_match = guild_id and command_obj.guild_ids and guild_id in command_obj.guild_ids
      is_global_command_for_global_sync = not guild_id and not command_obj.guild_ids
      is_global_command_for_guild_sync = guild_id and not command_obj.guild_ids

      should_include = False
      if guild_id:
        if command_obj.guild_ids:
          if guild_id in command_obj.guild_ids:
            should_include = True
        else:
          should_include = True
      else:
        if not command_obj.guild_ids:
          should_include = True

      if should_include:
        payload = command_obj.to_application_command_payload()
        if payload:
          payloads_to_send.append(payload)

    if not payloads_to_send:
      self.logger.info(f"No application commands found to sync for {'guild ' + str(guild_id) if guild_id else 'global'}.")
      return []

    try:
      if guild_id:
        self.logger.info(f"Syncing {len(payloads_to_send)} commands to guild {guild_id}...")
                
        response_data = await self.http.bulk_override_guild_commands(
          self.id, guild_id, payloads_to_send
        )
        self.logger.info(f"Successfully synced {len(response_data)} commands to guild {guild_id}.")
      else:
        self.logger.info(f"Syncing {len(payloads_to_send)} commands globally...")
  
        response_data = await self.http.bulk_override_global_commands(
          self.id, payloads_to_send
        )
        self.logger.info(f"Successfully synced {len(response_data)} commands globally.")
        return response_data
    except Exception as e:
      self.logger.error(f"Error during command sync: {e}")
      return []

  def event(self, coro):
    if asyncio.iscoroutinefunction(coro):
      self.event_handlers[coro.__name__] = coro
    else:
      raise TypeError('Event handler must be a coroutine function')
    return coro

  def command(self, name=None, **attrs):
    def decorator(func):
      cmd_name = name or func.__name__
      command_obj = Command(func, cmd_name, **attrs)
      self.commands[command_obj.name] = command_obj
      for alias in command_obj.aliases:
        self.commands[alias] = command_obj
      return func
    return decorator

  async def latency(self):
    start_time = time.perf_counter()
    await self.http.request(method="GET", path="/gateway")
    latency = (time.perf_counter() - start_time) * 1000  
    return latency
        
  async def _connect(self):
    while True:
      try:
        self.logger.info("Starting Connection to Discord API")
        async with websockets.connect("wss://gateway.discord.gg/?v=10&encoding=json", max_size=10000000) as ws:
          await self._identify(ws)
          hello_message = await ws.recv()
          hello_data = json.loads(hello_message)
          heartbeat_interval = hello_data['d']['heartbeat_interval'] / 1000
          async def send_heartbeat():
            while True:
              await asyncio.sleep(heartbeat_interval)
              heartbeat_payload = {
                'op': 1,
                'd': None
              }
              await ws.send(json.dumps(heartbeat_payload))
          asyncio.create_task(send_heartbeat())                 
                    
          self.logger.info(f"Connection Successful. Latency {await self.latency()} MS")
          async for message in ws:
            try:
              await self._handle(message)
            except websockets.exceptions.PayloadTooBig:
              self.logger.error("Payload too big. Skipping this message.")
            except Exception as e:
              self.logger.error(e)

      except websockets.ConnectionClosed as e:
        self.logger.error(f'Connection closed: {e}')
        await asyncio.sleep(1)
        
      except Exception as e:
        self.logger.error(f'An error occurred: {e}')
        await asyncio.sleep(1)
      self.logger.info("Trying to Establish Connection")

  async def _identify(self, ws):
    await ws.send(json.dumps({
      "op": 2,
      "d": {
        "token": self.token,
        'intents': self.intents,
        "properties": {
          "$os": "PaWpD",
          "$browser": "PaWpD",
          "$device": "PaWpD",
        },
        "presence": {"status": "online", "afk": False},
      },
    }))

  async def _handle(self, message):
    event = json.loads(message)
    event_name = event.get('t')
    event_data = event.get('d')
    if event_name == 'MESSAGE_CREATE':
      handler = self.event_handlers.get('on_message_create')
      msg_obj = Message(event_data, self)
      if handler:
        await handler(msg_obj)
      elif self.prefix and event_data['content'].startswith(self.prefix):
        await self.process(event_data, _side=True)
    elif event_name == "INTERACTION_CREATE":
      name = event_data['data']['name']
      handler = self.commands.get(name)
      args = event_data['data'].get('options')
      message_obj = Msg(event_data, self, interaction=True)
      if handler:
        if args:
          await handler.invoke(message_obj, *args)
        else:
          await handler.invoke(message_obj)
    elif event_name == "READY":
      handler = self.event_handlers.get('on_ready')
      self.user = User(event_data['user'], self)
      self.id = self.user.id
      for guild in event_data['guilds']:
        self.guilds.append(Guild(guild, self))
      if handler:         
        await handler(self.user)
    elif event_name == 'MESSAGE_UPDATE':
      handler = self.event_handlers.get('on_message_update')
      msg_obj = Msg(event_data, self)
      if handler:
        await handler(msg_obj)
    elif event_name == 'MESSAGE_DELETE':
      handler = self.event_handlers.get('on_message_delete')
      msg_obj = Message(event_data, self)
      if handler:
        await handler(msg_obj)
    elif event_name == "GUILD_CREATE":
      handler = self.event_handlers.get('on_guild_join')
      guild_obj = Guild(event_data, self)
      self.guilds.append(guild_obj)
      if handler:
        await handler(guild_obj)
    elif event_name == "GUILD_DELETE":
      handler = self.event_handlers.get('on_guild_leave')
      guild_obj = Guild(event_data, self)
      self.guilds.pop(guild_obj)
      if handler:
        await handler(guild_obj)
    elif event_name == "GUILD_UPDATE":
      handler = self.event_handlers.get('on_guild_update')
      guild_obj = Guild(event_data, self)
      if handler:
        await handler(guild_obj)
    elif event_name == "GUILD_MEMBER_ADD":
      handler = self.event_handlers.get('on_member_join')
      user_obj = User(event_data, self)
      if handler:
        await handler(user_obj)
    elif event_name == "GUILD_MEMBER_REMOVE":
      handler = self.event_handlers.get('on_member_leave')
      user_obj = User(event_data, self)
      if handler:
        await handler(user_obj)

  async def process(self, event_data, _side=False):
    if _side == False:
      event_data = event_data._JSON
    parts = event_data['content'][len(self.prefix):].split()
    command = parts[0]
    args = parts[1:]          
    msg_obj = Msg(event_data, self)
    handler = self.commands.get(command).invoke
    if handler:
      await handler(msg_obj, *args)
        
  def start(self):
    asyncio.get_event_loop().run_until_complete(self.http._get_session())
    asyncio.get_event_loop().run_until_complete(self._connect())
    asyncio.get_event_loop().run_forever()