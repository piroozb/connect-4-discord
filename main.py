import discord
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv
from keep_alive import keep_alive
from connect4 import Board
import math
import random
import asyncio

load_dotenv('.env')

PLAYER_PIECE = 'R'
AI_PIECE = 'Y'
BOT_ID = 837837082948534272
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
# what index stands for what in IDS
BRD, P1, P2, CURR_P, TIMER, CHAN = 0, 1, 2, 3, 4, 5
# to differentiate between both players
P_DICT = {True: [P1, 'R', discord.Colour.red()],
          False: [P2, 'Y', discord.Colour.gold()]}
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
    afk.start()
    await client.change_presence(activity=discord.Game(' connect 4 '
                                                       '| 4help'))


@tasks.loop(seconds=60)
async def afk():
    remove = []
    for key in IDS:
        if IDS[key][TIMER] == 240:
            channel = IDS[key][CHAN]
            await channel.send(f'{IDS[key][P1].display_name} :crossed_swords:'
                               f' {IDS[key][P2].display_name}: '
                               f'Game ended due to inactivity')
            remove.append(key)
        else:
            IDS[key][TIMER] += 1
    for key in remove:
        del IDS[key]


@client.command()
async def help(ctx):
    """Help message for list of commands and how to use them"""
    embed = discord.Embed(color=discord.Colour.green())
    embed.set_author(name='Help')
    embed.add_field(name='How to start playing connect 4',
                    value='4play <user>; if no one/the bot'
                          ' is mentioned, the game will'
                          ' be played against the bot',
                    inline=False)
    await ctx.send(embed=embed)


@client.command()
async def play(ctx):
    """Starts a game with either a mentioned user or the bot and then
    adds it to IDS with message id as key, and a list with the board,
    player ids, and first move as the values"""
    # Doesn't start if no one or a bot is mentioned
    if len(ctx.message.mentions) == 0 or ctx.message.mentions[0] == client.user:
        player2 = client.user
    elif ctx.message.mentions[0].bot or \
            ctx.message.mentions[0] == ctx.author:
        await ctx.send(':x: ERROR: You cannot tag a bot or yourself. '
                       '\nEither tag another user you want to play with'
                       ' or the bot/no one if you want to play with the bot.')
        return None
    else:
        player2 = ctx.message.mentions[0]
    player1 = ctx.author
    board = Board()
    # Prints starting board
    message = await ctx.send(f':red_circle: '
                             f'{player1.display_name} :crossed_swords: '
                             f'{player2.display_name} :yellow_circle: \n'
                             + TOP_NUM + board.print_board() +
                             f'\n Current player: <@{player1.id}>'
                             f'\n :flag_white:: Forfeit')
    # Adds the emotes the players will be clicking on and adds
    # the game to the global dictionary
    for emoji in EMOTES:
        await message.add_reaction(emoji)
    IDS[message.id] = [board, player1, player2, 'R', 0, ctx.channel]


@client.event
async def on_reaction_add(reaction, user) -> None:
    """
    Check which reaction role was pressed and changes the board accordingly.
    """
    # If reaction is in a channel where no one is playing, or if the person
    # adding the reactions is the bot, do nothing.
    if reaction.message.id not in IDS or \
            user.id == BOT_ID:
        return None
    curr_channel = IDS[reaction.message.id]
    channel = curr_channel[CHAN]
    curr_piece = curr_channel[CURR_P]
    curr_board = curr_channel[BRD]
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
        embed = discord.Embed(title=f' {user.display_name} forfeited, '
                                    f'{curr_channel[1].display_name}'
                                    f' :crossed_swords: '
                                    f'{curr_channel[2].display_name}',
                              color=discord.Colour.green())
        embed.set_image(url='https://media1.tenor.com/images/'
                            '8c3cb918305bf277589c6ad84dfcea53/tenor.gif')
        await channel.send(embed=embed)
        return None
    # if the column is already filled, sends error message and does nothing
    # with the board
    if not curr_board.is_valid_location(0, EMOTES[reaction.emoji]):
        await reaction.message.edit(content=f':red_circle:'
                                            f'{curr_channel[1].display_name}'
                                            f' :crossed_swords: '
                                            f'{curr_channel[2].display_name}'
                                            f' :yellow_circle: \n'
                                            + TOP_NUM + curr_board.print_board()
                                            + f':x: ERROR: Column full. :x:'
                                              f'\n Current player: '
                                              f'<@{curr_player.id}>'
                                              f'\n :flag_white:: Forfeit')
        return None
    # stops the function if user is the other player
    if user != curr_player:
        return None
    # changes current piece to next player
    curr_channel[CURR_P] = P_DICT[not player_red][1]
    r = 5
    # finds a valid location to drop the piece in starting from the bottom
    # of the column
    while not curr_board.is_valid_location(r, EMOTES[reaction.emoji]):
        r -= 1
    # drops the piece then edits the message to the updated board
    curr_board.drop_piece(r, EMOTES[reaction.emoji], curr_piece)
    # reset afk timer
    curr_channel[TIMER] = 0
    # Checks if there are no more positions to drop a piece, then ends the game
    # as a draw if this is true.
    if len(curr_board.get_valid_locations()) == 0:
        del IDS[reaction.message.id]
        embed = discord.Embed(title="It's a draw!",
                              color=discord.Colour.red())
        embed.set_image(url='https://media1.tenor.com/images/'
                            '729fc07335063f9d8a23002a71fdb0a8/tenor.gif')
        await channel.send(embed=embed)
        return None
    # Checks if there is a connect 4, and if so, sends a winner message and
    # removes the game from IDS
    if curr_board.is_win(curr_piece):
        curr_color = P_DICT[player_red][2]
        embed = discord.Embed(title=f'{curr_player.display_name} wins!',
                              color=curr_color)
        embed.set_image(url=random.choice(GIFS))
        await channel.send(embed=embed)
        await reaction.message.edit(content=f':red_circle: '
                                            f'{curr_channel[1].display_name}'
                                            f' :crossed_swords: '
                                            f'{curr_channel[2].display_name}'
                                            f' :yellow_circle: \n'
                                            + TOP_NUM + curr_board.print_board()
                                            + f'\n<@{curr_player.id}> wins!')
        del IDS[reaction.message.id]
        return None
    # If there is no connect 4, print the board and go to the next turn.
    else:
        await reaction.message.edit(content=f':red_circle: '
                                            f'{curr_channel[1].display_name}'
                                            f' :crossed_swords: '
                                            f'{curr_channel[2].display_name}'
                                            f' :yellow_circle: \n'
                                            + TOP_NUM + curr_board.print_board()
                                            + f'\n Current player: '
                                              f'<@{other_player.id}>'
                                            f'\n :flag_white:: Forfeit')
    # If playing with bot, run the minimax algorithm and then drop the piece
    # the algorithm has chosen.
    if other_player.bot:
        await asyncio.sleep(1)
        # Goes 6 layers deep into the tree
        col, minimax_score = curr_board.minimax(6, -math.inf, math.inf, True)
        row = curr_board.get_valid_locations()[col]
        # drop the piece into the board
        curr_board.drop_piece(row, col, AI_PIECE)
        curr_channel[TIMER] = 0
        # If bot plays winning move, send winning message and delete
        # game from IDS.
        if curr_board.is_win(curr_channel[CURR_P]):
            other_color = P_DICT[not player_red][2]
            embed = discord.Embed(title=f'{other_player.display_name} '
                                        f'wins!', color=other_color)
            embed.set_image(url=random.choice(GIFS))
            await channel.send(embed=embed)
            await reaction.message.edit(
                content=f':red_circle: '
                        f'{curr_channel[1].display_name}'
                        f' :crossed_swords: '
                        f'{curr_channel[2].display_name}'
                        f' :yellow_circle: \n'
                        + TOP_NUM + curr_board.print_board()
                        + f'\n<@{other_player.id}> wins!')
            del IDS[reaction.message.id]
        # Otherwise, just print the board
        else:
            await reaction.message.edit(
                content=f':red_circle: '
                        f'{curr_channel[1].display_name}'
                        f' :crossed_swords: '
                        f'{curr_channel[2].display_name}'
                        f' :yellow_circle: \n'
                        + TOP_NUM + curr_board.print_board()
                        + f'\n Current player:'
                        f' <@{curr_player.id}>'
                        f'\n :flag_white:: Forfeit')
        # changes current piece back to user
        curr_channel[CURR_P] = curr_piece


keep_alive()
client.run(os.getenv('TOKEN'))
# client.close()
