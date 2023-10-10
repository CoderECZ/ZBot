import discord, sqlite3, requests
from discord.ext import commands

conn = sqlite3.connect("data/coderz.biz")
cursor = conn.cursor()

class Payment(commands.Cog):
    '''Handles the payment of developer payments when a project is completed.'''
    def __init__(self, bot):
        self.bot = bot
    
    async def payment(self, ctx, author: int, project_id: int):
        if int(project_id):
            cursor.execute('SELECT developer_payment, status FROM projects WHERE project_id = ?', (project_id,))
            developer_payment = cursor.fetchmany()
            if developer_payment:
                # Make payment request to PayPal
                ## Possible verification/authorisation method to ensure that the command is valid and allowed
                pass
            else:
                ctx.author.send("Failed to send developer payment.")