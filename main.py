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

load_dotenv('.env')

client = commands.Bot(command_prefix='4', case_insensitive=True)
client.remove_command('help')
EMOTES = {'1️⃣': 0, '2️⃣': 1, '3️⃣': 2, '4️⃣': 3, '5️⃣': 4, '6️⃣': 5, '7️⃣': 6}
CONNECT4_EMOTES = {':blue_circle:': 0, ':red_circle:': 1, ':yellow_circle:': 2}
IDS = {}
BRD, P1, P2, CURR_P = 0, 1, 2, 3

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
    board = Board()
    message = await ctx.send(board.print_board() +
                             f'Current player: <@{player1.id}>')
    # idk what this does <- it reacts to the message with the seven emotes;
    # this is so that the players can click on the reactions rather than
    # having to add the reactions themselves
    for emoji in EMOTES:
        await message.add_reaction(emoji)
    IDS[ctx.message.channel.id] = [board, player1, player2, 'R']


@client.event
async def on_reaction_add(reaction, user) -> Optional[int]:
    """
    Check which reaction role was pressed from positions 0-5 on EMOTES.
    The corresponding number to that reaction, which is column <c>.
    """
    # If reaction is in a channel where no one is playing, or if reaction is
    # not a valid reaction, or if the person adding the reactions is the bot,
    # do nothing.
    if reaction.message.channel.id not in IDS or \
            reaction.emoji not in EMOTES.keys() or \
            user.id == 837837082948534272:
        return None
    curr_channel = IDS[reaction.message.channel.id]
    curr_piece = curr_channel[CURR_P]
    curr_board = curr_channel[BRD]
    await reaction.remove(user)
    if curr_piece == 'R':
        curr_player = curr_channel[P1]
        other_player = curr_channel[P2]
        if user != curr_player:
            return None
        else:
            player = str(curr_player)
            embed = discord.Embed(title=f'{player[:-5]} wins!',
                                  color=discord.Colour.red())
            curr_channel[CURR_P] = 'Y'
    else:
        curr_player = curr_channel[P2]
        other_player = curr_channel[P1]
        if user != curr_player:
            return None
        else:
            player = str(curr_player)
            embed = discord.Embed(title=f'{player[:-5]} wins!',
                                  color=discord.Colour.gold())
            curr_channel[CURR_P] = 'R'
    r = 5
    while not curr_board.is_valid_location(r, EMOTES[reaction.emoji]):
        r -= 1
    curr_board.drop_piece(r, EMOTES[reaction.emoji], curr_piece)
    if curr_board.winning_move(curr_piece):
        channel = client.get_channel(reaction.message.channel.id)
        embed.set_image(url='https://i.makeagif.com/media/1-24-2016/OaJxDC.gif')
        await channel.send(embed=embed)
        del IDS[reaction.message.channel.id]
    await reaction.message.edit(content=curr_board.print_board() +
                                f'\n Current player: <@{other_player.id}>')


keep_alive()
client.run(os.getenv('TOKEN'))
# client.close()
