import discord, sqlite3
from discord.ext import commands

from cogs.utilities import Utilites
from cogs.statuses import Statuses

conn = sqlite3.connect("data/coderz.db")
cursor = conn.cursor()

class ManagementPanel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.server_id = 1088951646886842498 
        self.server = bot.get_guild(self.server_id)
    
    @commands.command(name="admin_manage")
    @commands.has_any_role('Chief Executive Officer', 'Chief Operations Officer', 1124886855494668298)
    async def admin_manage(self, ctx, userID: int):
        member = self.server.get_member(userID)
        nickname = Utilites.user_nickname(user_id=userID, guild=self.server)
        
        role_functions = {
            "Chief Executive Officer": lambda server: discord.utils.get(self.server.roles, name="Chief Executive Officer"),
            "Chief Operations Officer": lambda server: discord.utils.get(self.server.roles, name="Chief Operations Officer"),
            "Account Executive": lambda server: discord.utils.get(self.server.roles, name="Account Executive"),
            "Developer": lambda server: discord.utils.get(self.server.roles, name="Developer"),
            "Staff": lambda server: discord.utils.get(self.server.roles, name="Staff"),
            "Sales Representative": lambda server: discord.utils.get(self.server.roles, name="Sales Representative"),
        }

        async def rank_check(message_content, server):
            # Iterate through the role functions to find a match
            for role_name, role_function in role_functions.items():
                if message_content.lower() == role_name.lower():
                    role = role_function(server)
                    if role:
                        return role  # Return the role object

            return None  # Return None if no matching role is found
        
        def check(message):
            return message.author == ctx.author and isinstance(message.channel, discord.DMChannel)

        async def remove_roles_from_user(self, server):
            for role_name, role_function in role_functions[0]["ranks"].items():
                role = role_function(server)
                if role:
                    try:
                        await member.remove_roles(role)
                    except Exception as e:
                        print(f"Failed to remove role {role_name} from {member.name}: {e}")
            
        try:
            cursor.execute('''
                SELECT developer_name, developer_rank
                FROM developers
                WHERE user_id = ?
            ''', (userID,))
            
            developerData = cursor.fetchone()
            developerRoles = Utilites.get_certified_roles(userID)
        except Exception as e:
            print(f"Failed to fetch data: {e}")
        
        qEmbed = discord.Embed(
            title=f"Managing {developerData[0]}",
            description=f"__Please select a function that you would like to perform below from the list below.__\n"
                        f"*Once you have made a decision, just put in the number for it below.*\n\n"
                        f"----------------------------------------------------------------------------------------\n\n"
                        f"1️⃣ | Change Rank\n"
                        f"2️⃣ | Adjust Certifications\n"
                        f"3️⃣ | Force Status\n",
            colour=0x00ff00
            )
        
        await ctx.author.send(embed=qEmbed)
        qResp = await self.bot.wait_for("message", check=check, timeout=120)
        
        if qResp.content.lower() in ['1️⃣', '1', 'one']:
            while True:
                await ctx.author.send("What rank will they be put up to?")
                rank = await self.bot.wait_for("message", check=check, timeout=120)
                
                await ctx.author.send(f"Are you sure you want to give {nickname} the rank {rank.content}?")
                d = await self.bot.wait_for("message", check=check, timeout=120)
                
                if d.content.lower() == "yes" or d.content.lower() == "y":
                    await remove_roles_from_user(server=self.server)
                    
                    rankMsg = rank.content
                    rank_function = role_functions[0]["ranks"].get(rankMsg.lower())
                    
                    if rank_function:
                        rankObj = rank_function(self.server)
                        if rankObj:
                            await member.add_roles(rankObj)
                    
                    await ctx.author.send("Would you like the person to have the developer or staff role or shall they only have their rank role?\nPlease type either developer, staff or none.")
                    d1 = await self.bot.wait_for("message", check=check, timeout=120)
                    
                    if d1.content.lower() == "developer" or "dev":
                        dev = discord.utils.get(self.server.roles, name="Developer")
                        await member.add_roles(dev)
                    elif d1.content.lower() == "staff":
                        staff = discord.utils.get(self.server.roles, name="Staff")
                        await member.add_roles(staff)
                    elif d1.content.lower() == "none":
                        pass
                    
                    try:
                        cursor.execute('''
                            UPDATE developers
                            SET developer_rank = ?
                            WHERE user_id = ?
                        ''', (rankMsg, userID))
                        
                        conn.commit()
                    except Exception as e:
                        await ctx.author.send("Failed to save information to database.")
                        print(f"Error saving information to database: {e}")
                        
                    await ctx.author.send(f"Succesfully given {rankMsg} to {nickname}")
                    
                    break
                elif d.content.lower() == "no" or "n":
                    continue
                else:
                    await ctx.author.send("Invalid input detected, would you like to return back to start?")
                    d2 = await self.bot.wait_for("message", check=check, timeout=120)
                    
                    if d2.content.lower() == "yes" or "y":
                        continue
                    elif d2.content.lower() == "no" or "n":
                        break
                    else:
                        await ctx.author.send("Invalid input detected.")
                        break
        elif qResp.content.lower() in ['2️⃣', '2', 'two']:
            
            await ctx.author.send("Would you like to add or remove a certification?")
            d1 = await self.bot.wait_for("message", check=check, timeout=120)
            
            if d1.content.lower() == "remove":
                await ctx.author.send("What certification would you like to remove from the developer?")
                await ctx.author.send(f"These are their current certifications: {developerRoles[:]}")
                r = await self.bot.wait_for("message", check=check, timeout=120)
                
                # Check if the role exists in the certifications dictionary
                if r.content in role_functions[1]["certs"]:
                    role_lambda = role_functions[1]["certs"][r.content]
                    role_to_remove = role_lambda(self.server)
                    await member.remove_roles(role_to_remove)
                    rMsg = r.content
                    Utilites.remove_certified_role(userID, rMsg)
                else:
                    await ctx.author.send("The specified certification role doesn't exist.")
            elif d1.content.lower() == "add":
                await ctx.author.send("What certifications would you like to add?")
                await ctx.author.send(f"These are their current certifications: {developerRoles[:]}")
                r = await self.bot.wait_for("message", check=check, timeout=120)
                
                if r.content in role_functions[1]["certs"]:
                    role_lambda = role_functions[1]["certs"][r.content]
                    role_to_add = role_lambda(self.server)
                    await member.add_roles(role_to_add)
                    rMsg = r.content
                    Utilites.add_certified_role(userID, r.content)
                else:
                    await ctx.author.send("The specified certification role doesn't exist.")
        elif qResp.content.lower() in ['3️⃣', '3', 'three']:
            statuses = ['available', 'unavailable', 'onbreak', 'busy']
            
            async def statusFunc():
                        await ctx.author.send("What status would you like to force this developer to have?")
                        r = await self.bot.wait_for("message", check=check, timeout=120)
                        
                        while True:
                            if r.content.lower() in statuses:
                                await ctx.author.send(f"To confirm: {nickname} will have the status: {r.content}.\nIs this correct?")
                                d = await self.bot.wait_for("message", check=check, timeout=120)
                                
                                if d.content.lower() in ['yes', 'y']:
                                    try:
                                        statusObj = Statuses.get_status_role(server=self.server, status_name=r.content)
                                    except Exception as e:
                                        await ctx.author.send("Failed to retrieve role object.")
                                        print(f"Error adding finding status role: {e}")
                                        break
                                    finally:
                                        try:
                                            await member.add_roles(statusObj)
                                        except Exception as e:
                                            await ctx.author.send("Failed to assign status role to user.")
                                            print(f"Error adding finding status role: {e}")
                                            break
                                        finally:
                                            try:
                                                cursor.execute('''
                                                    UPDATE developers
                                                    SET status = ?
                                                    WHERE user_id = ?
                                                ''', (r.content.lower(), userID))
                                                
                                                conn.commit()
                                                
                                                await ctx.author.send("Status succesfully set on developer.")
                                                await member.remove_roles(currentStatusObj)
                                                break
                                            except sqlite3.Error as e:
                                                await ctx.author.send("Failed to save information to database.")
                                                print(f"Error setting information in database: {e}")
                                                break
                                elif d.content.lower() in ['no', 'n']:
                                    await ctx.author.send("Would you like to try again?")
                                    r = self.bot.wait_for("message", check=check, timeout=120)
                                    
                                    if r.content.lower() in ['yes', 'y']:
                                        continue
                                    elif r.content.lower() in ['no', 'n']:
                                        break
                                    else:
                                        await ctx.author.send("Invalid input detected.")
                                        break
                                else:
                                    await ctx.author.send("Invalid input detected.")
                                    break
                            else:
                                await ctx.author.send(f"The status: {r.content} does not exist.")
                                await ctx.author.send("Would you like to try again?")
                                r = self.bot.wait_for("message", check=check, timeout=120)
                                
                                if r.content.lower() in ['yes', 'y']:
                                    continue
                                elif r.content.lower() in ['no', 'n']:
                                    break
                                else:
                                    await ctx.author.send("Invalid input detected.")
                                    break
            try:
                cursor.execute("SELECT status FROM developers WHERE user_id=?", (userID,))
                currentStatus = cursor.fetchone()
                if currentStatus:
                    if currentStatus[0].lower() == "onBreak":
                        currentStatusU = "On Break"
                    else:
                        currentStatusU = currentStatus[0]
                        
                    currentStatusObj = discord.utils.get(self.server.roles, name=currentStatusU)
                    await statusFunc()
                else:
                    await ctx.author.send("Developer does not currently have a status.\nIf they have not been registered, it is recommended that they do first.\nIf you, please type override to continue.")
                    r = await self.bot.wait_for("message", check=check, timeout=120)
                    
                    if r.content.lower() != "override":
                        await ctx.author.send("Current process has been stopped.")
                    elif r.content.lower() == "override":
                        await statusFunc()
            except Exception as e:
                await ctx.author.send("Failed to fetch developers current status.")
                print(f"Error retrieving information from database: {e}")