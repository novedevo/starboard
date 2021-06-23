import bot_key
import discord
from discord.channel import TextChannel
from discord.raw_models import RawReactionActionEvent
from discord.message import Message

client = discord.Client()

starboard_channel: TextChannel = None  # global variable


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    global starboard_channel
    # grab a reference to the channel called starboard
    starboard_channel = filter(
        lambda channel: channel.name == "starboard", client.get_all_channels()
    ).__next__()


@client.event
async def on_raw_reaction_add(reaction: RawReactionActionEvent):
    # print(reaction)
    if reaction.emoji.name == "📌":
        channel: TextChannel = client.get_channel(reaction.channel_id)
        message: Message = await channel.fetch_message(reaction.message_id)
        # ensure this is the first pin emote to avoid repetition
        if len(list(filter(lambda reaction: reaction.emoji == "📌", message.reactions))) == 1:
            # Future: use embeds, not quotations
            # Future: enable attachments?
            await starboard_channel.send(
                f"{message.author.display_name} *in* **#{channel.name}** *said:*\n> {message.content}"
            )


@client.event
# Future: remove previous messages when they are unpinned. Search function?
async def on_raw_reaction_remove(reaction: RawReactionActionEvent):
    # print(reaction)
    if reaction.emoji.name == "📌":
        channel: TextChannel = client.get_channel(reaction.channel_id)
        message: Message = await channel.fetch_message(reaction.message_id)
        # if a pin was removed and there are no pins, we should remove the pin message.
        if len(list(filter(lambda reaction: reaction.emoji == "📌", message.reactions))) == 0:
            await starboard_channel.send('Pin removal detected!')

client.run(bot_key.key)
