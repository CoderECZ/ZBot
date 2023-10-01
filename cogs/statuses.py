import discord, sqlite3
from discord.ext import commands

from cogs.utilities import Utilites

conn = sqlite3.connect("data/developers.db")
cursor = conn.cursor()

class Statuses(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.server_id = 1088951646886842498 # Replace with your server ID
        self.server = bot.get_guild(self.server_id)
    
    def create_schedule_embed(self):
        # Get a list of developers and their statuses
        cursor.execute('''
            SELECT user_id, status
            FROM developers
        ''')
        developer_statuses = cursor.fetchall()

        embed = discord.Embed(
            title="📅 Schedule 📅",
            description="__Select your status below!__\n\n"
                        "🟢 - Available for Projects\n"
                        "`!available`\n\n"
                        "🟠 - Not available for Projects\n"
                        "`!unavailable`\n\n"
                        "🔴 - On Leave/Taking a break\n"
                        "`!onBreak`\n\n"
                        "🟡 - Working on a project!\n"
                        "`This role cannot be manually added, it is given when you claim a project.`\n\n"
                        "*Once you have done this, a role will be assigned to you.*\n\n"
                        "__Staff Statuses__\n",
            colour=0xffffff
        )

        # Add developer names and statuses to the embed
        for developer in developer_statuses:
            user_id, status = developer
            
            if status.lower() == "available":
                status = "🟢 | Available"
            elif status.lower() == "unavailable":
                status = "🟠 | Unavailable"
            elif status.lower() == "onbreak":
                status = "🔴 | On Break"
            elif status.lower() == "busy":
                status = "🟡 | Busy"

            developerNick = Utilites.user_nickname(user_id=user_id, guild=self.server)
            
            embed.add_field(name=developerNick, value=f"➥ {status}", inline=True)

        return embed