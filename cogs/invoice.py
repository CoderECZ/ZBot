import discord, sqlite3
from discord.ext import commands

conn = sqlite3.connect("data/coderz.db")
cursor = conn.cursor()

class Invoice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    