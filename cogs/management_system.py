import discord
from discord.ext import commands

class ManagementPanel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot