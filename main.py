"""
This file contains all the functions relating to discord API calls.
"""
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from keep_alive import keep_alive
from connect4 import Board
from typing import Optional
import random

load_dotenv('.env')

client = commands.Bot(command_prefix='4', case_insensitive=True)
client.remove_command('help')

EMOTES = {'1️⃣': 0, '2️⃣': 1, '3️⃣': 2, '4️⃣': 3, '5️⃣': 4, '6️⃣': 5, '7️⃣': 6,
          '🏳': 'F'}
TOP_NUM = '** **\n:one: :two: :three: :four: :five: :six: :seven: \n'
IDS = {}
P_DICT = {True: [1, 'R', discord.Colour.red()],
          False: [2, 'Y', discord.Colour.gold()]}
GIFS = []
gif_file = open("win_gifs.txt", "r")
content = gif_file.readline()
while content != '':
    content = gif_file.readline()
    GIFS.append(content)


@client.event
async def on_ready():
    """Sends messages once bot connects and sets bot activity"""
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
    if ctx.message.channel.id in IDS.keys():
        await ctx.send(':x: ERROR: Someone is already playing in this channel')
        return None
    player1 = ctx.author
    try:
        player2 = ctx.message.mentions[0]
    except IndexError:
        await ctx.send('Mention a person!')
        return None
    board = Board()
    message = await ctx.send(f'{player1.display_name} :vs: '
                             f'{player2.display_name} \n'
                             + TOP_NUM + board.print_board() +
                             f'\n Current player: <@{player1.id}>'
                             f'\n :flag_white:: Forfeit')
    # idk what this does <- it reacts to the message with the seven emotes;
    # this is so that the players can click on the reactions rather than
    # having to add the reactions themselves
    for emoji in EMOTES:
        await message.add_reaction(emoji)
    IDS[ctx.message.channel.id] = [board, player1, player2, 'R']


@client.event
async def on_reaction_add(reaction, user) -> None:
    """
    Check which reaction role was pressed from positions 0-5 on EMOTES.
    The corresponding number to that reaction, which is column <c>.
    """
    # If reaction is in a channel where no one is playing, or if reaction is
    # not a valid reaction, or if the person adding the reactions is the bot,
    # do nothing.
    channel = client.get_channel(reaction.message.channel.id)
    if reaction.message.channel.id not in IDS or \
            user.id == 837837082948534272:
        return None
    elif reaction.emoji not in EMOTES.keys():
        await reaction.remove(user)
        return None
    elif EMOTES[reaction.emoji] == 'F':
        del IDS[reaction.message.channel.id]
        embed = discord.Embed(title=f'{user.display_name} forfeited!',
                              color=discord.Colour.green())
        embed.set_image(url='https://media1.tenor.com/images/'
                            '8c3cb918305bf277589c6ad84dfcea53/tenor.gif')
        await channel.send(embed=embed)
        return None
    curr_channel = IDS[reaction.message.channel.id]
    curr_piece = curr_channel[3]
    curr_board = curr_channel[0]
    player_red = True if curr_piece == 'R' else False
    curr_player = curr_channel[P_DICT[player_red][0]]
    other_player = curr_channel[P_DICT[not player_red][0]]
    await reaction.remove(user)
    if not curr_board.is_valid_location(0, EMOTES[reaction.emoji]):
        await reaction.message.edit(content=f'{curr_channel[1].display_name} '
                                            f':crossed_swords: '
                                            f'{curr_channel[2].display_name} \n'
                                            + TOP_NUM + curr_board.print_board()
                                            + f':x: ERROR: Column full. :x:'
                                    f'\n Current player: <@{curr_player.id}>'
                                    f'\n :flag_white:: Forfeit')
        return None
    if user != curr_player:
        return None
    curr_channel[3] = P_DICT[not player_red][1]
    r = 5
    while not curr_board.is_valid_location(r, EMOTES[reaction.emoji]):
        r -= 1
    curr_board.drop_piece(r, EMOTES[reaction.emoji], curr_piece)
    await reaction.message.edit(content=f'{curr_channel[1].display_name} '
                                        f':crossed_swords: '
                                        f'{curr_channel[2].display_name} \n' +
                                        TOP_NUM + curr_board.print_board() +
                                f'\n Current player: <@{other_player.id}>'
                                f'\n :flag_white:: Forfeit')
    if curr_board.winning_move(curr_piece):
        curr_color = P_DICT[player_red][2]
        embed = discord.Embed(title=f'{curr_player.display_name} wins!',
                              color=curr_color)
        embed.set_image(url=random.choice(GIFS))
        await channel.send(embed=embed)
        await reaction.message.edit(content=f'{curr_channel[1].display_name}'
                                            f' :crossed_swords: '
                                            f'{curr_channel[2].display_name}\n'
                                            + TOP_NUM + curr_board.print_board()
                                            + f'\n<@{curr_player.id}> wins!')
        del IDS[reaction.message.channel.id]


keep_alive()
client.run(os.getenv('TOKEN'))
# client.close()
