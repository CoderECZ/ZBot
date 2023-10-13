import discord
from discord.ext import commands

class Embeds():
    def __init__(self, bot):
        self.bot = bot
        
    async def questions(self, question: str = None) -> object:
        if question is None:
            return None
        elif question is not None:
            embed = discord.Embed(
                title=question, 
                color=discord.Color.blue(),
                description=f""
                )
        
        return embed
    