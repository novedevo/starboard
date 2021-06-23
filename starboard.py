from discord.channel import TextChannel
from discord.embeds import Embed
from discord.raw_models import RawReactionActionEvent
import bot_key
import discord
from discord.message import Message

client = discord.Client()

starboard_channel: TextChannel = None

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    global starboard_channel
    starboard_channel = filter(
        lambda channel: channel.name == "starboard", client.get_all_channels()).__next__()


@client.event
async def on_raw_reaction_add(reaction: RawReactionActionEvent):
    # print(reaction)
    if reaction.emoji.name == "📌" or reaction.emoji == ":pushpin:" or reaction.emoji == "pushpin":
        channel: TextChannel = client.get_channel(reaction.channel_id)
        message: Message = await channel.fetch_message(reaction.message_id)
        embed: Embed
        if len(list(filter(lambda reaction: reaction.emoji == "📌", message.reactions))) == 1:
            await starboard_channel.send(
                f"{message.author.display_name} *in* **#{channel.name}** *said:*\n> {message.content}"
            )


@client.event
async def on_raw_reaction_remove(reaction: RawReactionActionEvent):
    # print(reaction)
    if reaction.emoji.name == "📌" or reaction.emoji == ":pushpin:" or reaction.emoji == "pushpin":
        channel: TextChannel = client.get_channel(reaction.channel_id)
        message: Message = await channel.fetch_message(reaction.message_id)
        if len(list(filter(lambda reaction: reaction.emoji == "📌", message.reactions))) == 0:
            await starboard_channel.send('Pin removal detected!')

client.run(bot_key.key)
