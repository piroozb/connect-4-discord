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
    board = Board()
    send_board = board.print_board()
    message = await ctx.send(send_board)
    # for emoji in EMOTES: idk what this does
    #     await message.add_reaction(emoji)

    reaction = await client.add_reaction()
    c = await on_reaction_add(reaction, player1)
    update_board(reaction, message, board, c)


@client.event
async def on_reaction_add(reaction, user) -> Optional[int]:
    """
    Check which reaction role was pressed from positions 0-5 on EMOTES.
    :return: The corresponding number to that reaction, which is column <c>.
    """
    channel_id = 3123122  # ur channel id, not real.
    if reaction.message.channel.id != channel_id:
        return
    if reaction.emoji == EMOTES[0]:
        return 0
    elif reaction.emoji == EMOTES[1]:
        return 1
    elif reaction.emoji == EMOTES[2]:
        return 2
    elif reaction.emoji == EMOTES[3]:
        return 3
    elif reaction.emoji == EMOTES[4]:
        return 4
    elif reaction.emoji == EMOTES[5]:
        return 5


def update_board(reaction, message, curr_board: Board, c):
    # React to emoji reactions
    # Edit Discord Messages

    # create a new board with the new piece in it.
    # new_board = Board()
    # new_board.drop_piece()
    r = curr_board.current_row()
    # c corresponds to the emoji pressed.

    curr_board.drop_piece(r, c, reaction)
    await message.edit(content="the new content of the message")


keep_alive()
client.run(os.getenv('TOKEN'))
# client.close()
