import discord, sqlite3
from discord.ext import commands

class Communications(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def check(self, ctx, message):
        return message.author == ctx.author and isinstance(message.channel, discord.DMChannel)
    
    @commands.command(name="comm")
    async def comm(self, ctx, *, message: str = None):
        ctx.user.send("Who will you be communicating with?\n\n1 | Client\n2 | Staff")
        msg = await self.bot.wait_for("message", check=self.check(ctx=ctx, message=message), timeout=120)
        
        if msg.content.lower() in ['1', 'client']:
            pass
