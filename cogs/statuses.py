import discord, sqlite3
from discord.ext import commands, tasks

from cogs.utilities import Utilites

conn = sqlite3.connect("data/coderz.db")
cursor = conn.cursor()

global server_id

class Statuses(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.server_id = 1088951646886842498 
        self.server = bot.get_guild(self.server_id)
    
    @classmethod
    def create_schedule_embed(self):
        '''
        Creates the scheduled embed in the appropriate channel.
        '''
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

    @classmethod
    @tasks.loop(seconds=60)  # Adjust the interval as needed (e.g., update every hour)
    async def update_schedule_embed(self, name:str):
        '''
        Used to update the scheduled embed for the status of developers every 60 seconds.
        '''
        global schedule_message_id
        schedule_channel_id = 1154179596682543125  # Replace with the actual channel ID
        schedule_channel = self.bot.get_channel(schedule_channel_id)

        try:
            # Fetch the message using the stored message ID
            schedule_message = await schedule_channel.fetch_message(schedule_message_id)
            # Update the embed with the latest information
            updated_embed = self.create_schedule_embed()  # Replace with your updated embed creation logic
            await schedule_message.edit(embed=updated_embed)
        except discord.NotFound:
            # The message doesn't exist; create a new one
            updated_embed = self.create_schedule_embed()  # Replace with your updated embed creation logic
            schedule_message = await schedule_channel.send(embed=updated_embed)
            schedule_message_id = schedule_message.id
    
    @classmethod
    async def get_status_role(self, server, status_name):
        rF = await Utilites.rolesF()
        for role_category in rF:
            if "statuses" in role_category:
                statuses = role_category["statuses"]
                
                # Check if the status_name exists in the statuses dictionary
                if status_name in statuses:
                    # Retrieve the lambda function associated with the status
                    role_lambda = statuses[status_name]
                    
                    # Execute the lambda function to get the role object
                    role_object = role_lambda(server)  # Replace `server` with your actual server object
                    
                    return role_object  # Return the role object
                else:
                    return None
        return None  # Status not found in the dictionaries
