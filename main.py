import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from keep_alive import keep_alive
from connect4 import print_board, create_board

load_dotenv('.env')

client = commands.Bot(command_prefix='4', case_insensitive=True)
client.remove_command('help')
EMOTES = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣']
CONNECT4_EMOTES = {':blue_circle:': 0, ':red_circle:': 1, ':yellow_circle:': 2}


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    await client.change_presence(activity=discord.Game(' connect 4 '
                                                       '| 4help'))


@client.command()
async def help(ctx):
    embed = discord.Embed(color=discord.Colour.green())
    embed.set_author(name='Help')
    embed.add_field(name='How to start playing connect 4',
                    value='4play <user>; if no one is mentioned, the game will'
                          'be played against the bot',
                    inline=False)
    await ctx.send(embed=embed)


@client.command()
async def play(ctx):
    player1 = ctx.author
    player2 = ctx.message.mentions[0]
    board = create_board()
    send_board = print_board(board)
    message = await ctx.send(send_board)
    for emoji in EMOTES:
        await message.add_reaction(emoji)

keep_alive()
client.run(os.getenv('TOKEN'))
# client.close()

