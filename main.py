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

EMOTES = {'1️⃣': 0, '2️⃣': 1, '3️⃣': 2, '4️⃣': 3, '5️⃣': 4, '6️⃣': 5, '7️⃣': 6}
TOP_NUM = ':one: :two: :three: :four: :five: :six: :seven: \n'
IDS = {}
P_DICT = {True: [1, 'R', discord.Colour.red()],
          False: [2, 'Y', discord.Colour.gold()]}
GIFS = ['https://media1.tenor.com/images/514b6b9fe1e8afd9caa482275132d42e/'
        'tenor.gif?itemid=19830879', 'https://media1.tenor.com/images/'
        '7f2e03cad4e085c2cf9371bbcab98522/tenor.gif', 'https://'
        'ftw.usatoday.com/wp-content/uploads/sites/90/2013/05/untitled-331.gif',
        'https://media1.tenor.com/images/'
        '1be1127ceaa51b001234009f26a56378/tenor.gif',
        'https://thumbs.gfycat.com/AcademicKnobbyGrouse-max-1mb.gif', 'https://'
        'media3.giphy.com/media/vmon3eAOp1WfK/giphy.gif?cid=790b7611056376e13a'
        'f6146642ba87d9f5911db825664b24&rid=giphy.gif',
        'https://i.makeagif.com/media/1-24-2016/OaJxDC.gif']


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
    player1 = ctx.author
    player2 = ctx.message.mentions[0]
    board = Board()
    message = await ctx.send(TOP_NUM + board.print_board() +
                             f'\n Current player: <@{player1.id}>')
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
    if reaction.message.channel.id not in IDS or \
            user.id == 837837082948534272:
        return None
    elif reaction.emoji not in EMOTES.keys():
        await reaction.remove(user)
        return None
    curr_channel = IDS[reaction.message.channel.id]
    curr_piece = curr_channel[3]
    curr_board = curr_channel[0]
    await reaction.remove(user)
    if curr_piece == 'R':
        player_red = True
    else:
        player_red = False
    curr_player = curr_channel[P_DICT[player_red][0]]
    other_player = curr_channel[P_DICT[not player_red][0]]
    if user != curr_player:
        return None
    curr_channel[3] = P_DICT[not player_red][1]
    r = 5
    while not curr_board.is_valid_location(r, EMOTES[reaction.emoji]):
        r -= 1
    curr_board.drop_piece(r, EMOTES[reaction.emoji], curr_piece)
    if curr_board.winning_move(curr_piece):
        player = str(curr_player)
        curr_color = P_DICT[player_red][2]
        embed = discord.Embed(title=f'{player[:-5]} wins!',
                              color=curr_color)
        channel = client.get_channel(reaction.message.channel.id)
        embed.set_image(url=random.choice(GIFS))
        await channel.send(embed=embed)
        del IDS[reaction.message.channel.id]
    await reaction.message.edit(content=TOP_NUM + curr_board.print_board() +
                                f'\n Current player: <@{other_player.id}>')


keep_alive()
client.run(os.getenv('TOKEN'))
# client.close()
