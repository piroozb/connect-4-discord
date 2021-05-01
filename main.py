import discord
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv
from keep_alive import keep_alive

load_dotenv('.env')

client = commands.Bot(command_prefix='4', case_insensitive=True)
client.remove_command('help')


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
                    value='Type 4play; if someone is mentioned, the game will'
                          ' play against them. Otherwise it will start a game'
                          ' against the bot.',
                    inline=False)
    await ctx.send(embed=embed)


@client.command()
async def play(ctx):
    pass

keep_alive()
client.run(os.getenv('TOKEN'))
# client.close()

