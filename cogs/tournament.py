import discord
from discord.ext import commands
from random import randint
from random import choice as randchoice
import asyncio
from .utils.dataIO import fileIO
from .utils import checks
import os
from __main__ import settings

admins = {} #Should probably have this imported from a admins.json or something. It'll work for now though.

class Tournament:
    """Tournament commands."""

    def __init__(self, bot):
        self.bot = bot
        self.entrylist = fileIO("data/tournament/entrylist.json","load")

    def save_entries(self):
        fileIO("data/tournament/entrylist.json","save",self.entrylist)


    @commands.command(pass_context=True, no_pm=True)
    async def enter(self, ctx):
        """Enters user into tournament"""
        entrant = str(ctx.message.author.id)
        if entrant not in self.entrylist:
            self.entrylist[entrant] = entrant
            await self.bot.say("Added <@" + entrant + "> to current entrants.")
            self.save_entries()
        else:
            await self.bot.say("<@" + entrant + "> is already present in the entrants list.")

    @commands.command(pass_context=True, no_pm=True)
    async def unenter(self, ctx):
        """Removes user from entrants list"""
        entrant = str(ctx.message.author.id)
        if entrant not in self.entrylist:
            await self.bot.say("<@" + entrant + "> is not present in the entrant list.")
        else:
            await self.bot.say("Removing <@" + entrant + "> from the entry list...")
            del self.entrylist[entrant]
            self.save_entries()

    @commands.command(pass_context=True, no_pm=True)
    async def draw(self, ctx, value):
        """Draws [value] entrants from the list."""
        author = str(ctx.message.author.id)
        if author not in admins:
            await self.bot.say("Only admins are allowed to use this command.")
        else:
            try:
                for _ in range(int(value)):
                    entry = randchoice(list(self.entrylist.keys()))
                    await self.bot.say("<@" + entry + "> has been choosen.")
                    del self.entrylist[entry]
                    self.save_entries()
            except IndexError as e:
                print(e)
                await self.bot.say("No more entries in the list.")
                self.save_entries()

    @commands.command(no_pm=True, pass_context=False, hidden=True)
    async def entrantlist(self):
        """Lists all entries"""
        await self.bot.say(self.entrylist)
            
def check_folders():
    if not os.path.exists("data/tournament"):
        print("Creating data/tournament folder...")
        os.makedirs("data/tournament")

def check_files():
    f = "data/tournament/entrylist.json"
    if not fileIO(f, "check"):
        fileIO(f, "save", {})

def setup(bot):
    check_folders()
    check_files()
    n = Tournament(bot)
    bot.add_cog(n)
