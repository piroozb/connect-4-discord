import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from keep_alive import keep_alive
from connect4 import Board
from typing import Optional
import random

load_dotenv('.env')

# Prefix to call bot
client = commands.Bot(command_prefix='4', case_insensitive=True)
client.remove_command('help')  # Removes default help command

# Emotes used for the player to choose their move
EMOTES = {'1️⃣': 0, '2️⃣': 1, '3️⃣': 2, '4️⃣': 3, '5️⃣': 4, '6️⃣': 5, '7️⃣': 6,
          '🏳': 'F'}
# numbers to print above connect 4 board
TOP_NUM = '** **\n:one: :two: :three: :four: :five: :six: :seven: \n'
# dictionary to keep track of where the game is happening
IDS = {}
# to differentiate between both players
P_DICT = {True: [1, 'R', discord.Colour.red()],
          False: [2, 'Y', discord.Colour.gold()]}
# list of gifs to send when a player wins
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
    """Help message for list of commands and how to use them"""
    embed = discord.Embed(color=discord.Colour.green())
    embed.set_author(name='Help')
    embed.add_field(name='How to start playing connect 4',
                    value='4play <user>; if no one is mentioned, the game will'
                          ' be played against the bot',
                    inline=False)
    await ctx.send(embed=embed)


@client.command()
async def play(ctx):
    """Starts a game with either a mentioned user or the bot and then
    adds it to IDS with channel id, board, player ids, and first move"""
    # Doesn't start a game if someone is already playing in that channel
    if ctx.message.channel.id in IDS.keys():
        await ctx.send(':x: ERROR: Someone is already playing in this channel')
        return None
    # Doesn't start if no one or a bot is mentioned
    if len(ctx.message.mentions) == 0 or ctx.message.mentions[0].bot:
        await ctx.send('Mention a person!')
        return None
    player1 = ctx.author
    player2 = ctx.message.mentions[0]
    board = Board()
    # Prints starting board
    message = await ctx.send(f'{player1.display_name} :crossed_swords: '
                             f'{player2.display_name} \n'
                             + TOP_NUM + board.print_board() +
                             f'\n Current player: <@{player1.id}>'
                             f'\n :flag_white:: Forfeit')
    # Adds the emotes the players will be clicking on and adds
    # the game to the global dictionary
    for emoji in EMOTES:
        await message.add_reaction(emoji)
    IDS[message.id] = [board, player1, player2, 'R']


@client.event
async def on_reaction_add(reaction, user) -> None:
    """
    Check which reaction role was pressed and changes the board accordingly.
    """
    channel = client.get_channel(reaction.message.channel.id)
    # If reaction is in a channel where no one is playing, or if the person
    # adding the reactions is the bot, do nothing.
    if reaction.message.id not in IDS or \
            user.id == 837837082948534272:
        return None
    curr_channel = IDS[reaction.message.id]
    curr_piece = curr_channel[3]
    curr_board = curr_channel[0]
    # for P_DICT
    player_red = True if curr_piece == 'R' else False
    curr_player = curr_channel[P_DICT[player_red][0]]
    other_player = curr_channel[P_DICT[not player_red][0]]
    await reaction.remove(user)
    # stops the function if a reaction was added or if the reaction
    # was sent by a non-player
    if reaction.emoji not in EMOTES.keys() \
            or (user != curr_player and user != other_player):
        return None
    # At this point we know it's one of the two players who reacted to an emote.
    # Thus, we can directly cancel the game if one of the players forfeit.
    elif EMOTES[reaction.emoji] == 'F':
        del IDS[reaction.message.id]
        embed = discord.Embed(title=f'{user.display_name} forfeited!',
                              color=discord.Colour.green())
        embed.set_image(url='https://media1.tenor.com/images/'
                            '8c3cb918305bf277589c6ad84dfcea53/tenor.gif')
        await channel.send(embed=embed)
        return None
    # if the column is already filled, sends error message and does nothing
    # with the board
    if not curr_board.is_valid_location(0, EMOTES[reaction.emoji]):
        await reaction.message.edit(content=f'{curr_channel[1].display_name} '
                                            f':crossed_swords: '
                                            f'{curr_channel[2].display_name} \n'
                                            + TOP_NUM + curr_board.print_board()
                                            + f':x: ERROR: Column full. :x:'
                                    f'\n Current player: <@{curr_player.id}>'
                                    f'\n :flag_white:: Forfeit')
        return None
    # stops the function if user is the other player
    if user != curr_player:
        return None
    # changes current piece to next player
    curr_channel[3] = P_DICT[not player_red][1]
    r = 5
    # finds a valid location to drop the piece in starting from the bottom
    # of the column
    while not curr_board.is_valid_location(r, EMOTES[reaction.emoji]):
        r -= 1
    # drops the piece then edits the message to the updated board
    curr_board.drop_piece(r, EMOTES[reaction.emoji], curr_piece)
    await reaction.message.edit(content=f'{curr_channel[1].display_name} '
                                        f':crossed_swords: '
                                        f'{curr_channel[2].display_name} \n' +
                                        TOP_NUM + curr_board.print_board() +
                                f'\n Current player: <@{other_player.id}>'
                                f'\n :flag_white:: Forfeit')
    # Checks if player has won. If they did, sends a winner message
    # and then removes the board from IDS
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
        del IDS[reaction.channel.id]


keep_alive()
client.run(os.getenv('TOKEN'))
# client.close()
