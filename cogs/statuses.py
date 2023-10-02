import discord, sqlite3
from discord.ext import commands, tasks

from cogs.utilities import Utilites

conn = sqlite3.connect("data/coderz.db")
cursor = conn.cursor()

global server_id

class Statuses(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.schedule_channel_id = 1154179596682543125
        self.schedule_message_id = 1158469022216618095
        self.server_id = 1088951646886842498 
        self.server = bot.get_guild(self.server_id)
    
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
    
    @tasks.loop(seconds=60)
    async def update_schedule_embed(self):
        '''
        Used to update the scheduled embed for the status of developers every 60 seconds.
        '''
        # Replace with the actual channel ID
        schedule_channel = self.bot.get_channel(self.schedule_channel_id)

        try:
            # Fetch the message using the stored message ID
            schedule_message = await schedule_channel.fetch_message(self.schedule_message_id)
            # Update the embed with the latest information
            updated_embed = self.create_schedule_embed()  # Replace with your updated embed creation logic
            await schedule_message.edit(embed=updated_embed)
        except discord.NotFound:
            # The message doesn't exist; create a new one
            updated_embed = self.create_schedule_embed()  # Replace with your updated embed creation logic
            schedule_message = await schedule_channel.send(embed=updated_embed)
            schedule_message_id = schedule_message.id  # Assign schedule_message_id here
    
    async def get_status_role(self, server, status_name):
        '''Used to retrieve the status role of a user.'''
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

    @commands.command(name="available")
    async def available(self, ctx):
        '''Become available for projects and general CoderZ activities.'''
        member = self.server.get_member(ctx.author.id)
        available_role = discord.utils.get(self.server.roles, name="Available")
        unavailable_role = discord.utils.get(self.server.roles, name="Unavailable")
        onBreak_role = discord.utils.get(self.server.roles, name="On Break")
        
        cursor.execute("SELECT status FROM developers WHERE user_id=?", (ctx.author.id,))
        status_tuple = cursor.fetchone()  # Fetch the status from the database
        
        if status_tuple:
            status = status_tuple[0]  # Extract the status from the tuple
            try:
                if status.lower() == "unavailable":
                    await member.remove_roles(unavailable_role)
                elif status.lower() == "onbreak":
                    await member.remove_roles(onBreak_role)
                elif status.lower() == "available":
                    await ctx.author.send("You already have your status as available.")
            except Exception as e:
                print(f"Failed to assign status: {e}")
                await ctx.author.send("There was an error when attempting to assign your role, please contact a technical administrator.")
            else:
                try:
                    await member.add_roles(available_role)
                except Exception as e:
                    print(f"Failed to add role to user: {e}")
                    
                await ctx.author.send("Your status has been updated to available.")
                
                cursor.execute('''
                    UPDATE developers
                    SET status = ?
                    WHERE user_id = ?
                ''', ("available", ctx.author.id))
                
                conn.commit()
        else:
            await ctx.author.send("You are not registered as a developer. Please use the `register_developer` command first.")

    @commands.command(name="unavailable")
    async def unavailable(self, ctx):
        '''Become unavailable for projects and general CoderZ activities.'''
        member = self.server.get_member(ctx.author.id)
        available_role = discord.utils.get(self.server.roles, name="Available")
        unavailable_role = discord.utils.get(self.server.roles, name="Unavailable")
        onBreak_role = discord.utils.get(self.server.roles, name="On Break")
        
        cursor.execute("SELECT status FROM developers WHERE user_id=?", (ctx.author.id,))
        status_tuple = cursor.fetchone()  # Fetch the status from the database
        
        if status_tuple:
            status = status_tuple[0]  # Extract the status from the tuple
            try:
                if status.lower() == "available":
                    await member.remove_roles(available_role)
                elif status.lower() == "onbreak":
                    await member.remove_roles(onBreak_role)
                elif status.lower() == "unavailable":
                    await ctx.author.send("You already have your status as unavailable.")
            except Exception as e:
                print(f"Failed to assign status: {e}")
                await ctx.author.send("There was an error when attempting to assign your role, please contact a technical administrator.")
            else:
                try:
                    await member.add_roles(unavailable_role)
                except Exception as e:
                    print(f"Failed to add role to user: {e}")
                    
                await ctx.author.send("Your status has been updated to unavailable.")
                
                cursor.execute('''
                    UPDATE developers
                    SET status = ?
                    WHERE user_id = ?
                ''', ("unavailable", ctx.author.id))
                
                conn.commit()
        else:
            await ctx.author.send("You are not registered as a developer. Please use the `register_developer` command first.")

    @commands.command(name="onBreak")
    async def onBreak(self, ctx):
        '''Go on leave or take a break from projects and general CoderZ activities.'''
        member = self.server.get_member(ctx.author.id)
        available_role = discord.utils.get(self.server.roles, name="Available")
        unavailable_role = discord.utils.get(self.server.roles, name="Unavailable")
        onBreak_role = discord.utils.get(self.server.roles, name="On Break")
        
        cursor.execute("SELECT status FROM developers WHERE user_id=?", (ctx.author.id,))
        status_tuple = cursor.fetchone()  # Fetch the status from the database
        
        if status_tuple:
            status = status_tuple[0]  # Extract the status from the tuple
            try:
                if status.lower() == "unavailable":
                    await member.remove_roles(unavailable_role)
                elif status.lower() == "available":
                    await member.remove_roles(available_role)
                elif status.lower() == "onbreak":
                    await ctx.author.send("You already have your status as on break.")
            except Exception as e:
                print(f"Failed to assign status: {e}")
                await ctx.author.send("There was an error when attempting to assign your role, please contact a technical administrator.")
            else:
                try:
                    await member.add_roles(onBreak_role)
                except Exception as e:
                    print(f"Failed to add role to user: {e}")
                    
                await ctx.author.send("Your status has been updated to on break.")
                
                cursor.execute('''
                    UPDATE developers
                    SET status = ?
                    WHERE user_id = ?
                ''', ("onbreak", ctx.author.id))
                
                conn.commit()
        else:
            await ctx.author.send("You are not registered as a developer. Please use the `register_developer` command first.")
    
    async def busy(self, userID):
        '''Used to set a user's status to busy.'''
        member = self.server.get_member(userID)
        available_role = discord.utils.get(self.server.roles, name="Available")
        unavailable_role = discord.utils.get(self.server.roles, name="Unavailable")
        onBreak_role = discord.utils.get(self.server.roles, name="On Break")
        busy_role = discord.utils.get(self.server.roles, name="Busy")
        
        cursor.execute("SELECT status FROM developers WHERE user_id=?", (userID,))
        status_tuple = cursor.fetchone()  # Fetch the status from the database
        
        if status_tuple:
            status = status_tuple[0]  # Extract the status from the tuple
            try:
                if status.lower() == "unavailable":
                    await member.remove_roles(unavailable_role)
                elif status.lower() == "available":
                    await member.remove_roles(available_role)
                elif status.lower() == "onbreak":
                    await member.remove_roles(onBreak_role)
            except Exception as e:
                print(f"Failed to assign status: {e}")
            else:
                try:
                    await member.add_roles(busy_role)
                except Exception as e:
                    print(f"Failed to add role to user: {e}")
                
                cursor.execute('''
                    UPDATE developers
                    SET status = ?
                    WHERE user_id = ?
                ''', ("busy", userID))
                
                conn.commit()
        else:
            print("Unable to complete action.")
