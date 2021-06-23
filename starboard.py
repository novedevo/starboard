import bot_key
import discord
from discord.message import Message
from discord.reaction import Reaction
from discord.user import User

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message: Message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

@client.event
async def on_reaction_add(reaction: Reaction, user: User):
    # print(reaction)
    if reaction.emoji == "📌" or reaction.emoji == ":pushpin:" or reaction.emoji == "pushpin":
        if len(list(filter(lambda reaction: reaction.emoji == "📌", reaction.message.reactions))) == 1:
            await reaction.message.channel.send('Pin detected!')

@client.event
async def on_reaction_remove(reaction: Reaction, user: User):
    print(reaction)
    if reaction.emoji == "📌" or reaction.emoji == ":pushpin:" or reaction.emoji == "pushpin":
        if len(list(filter(lambda reaction: reaction.emoji == "📌", reaction.message.reactions))) == 0:
            await reaction.message.channel.send('Pin removal detected!')

client.run(bot_key.key)
