import discord
from discord.ext import commands, tasks
import sqlite3
import sys
import os
import json
from cogs.ticket_system import TicketSystem as Tickets

intents = discord.Intents.all()

bot = commands.Bot(command_prefix="!", intents=intents)

conn = sqlite3.connect("data/developers.db")
cursor = conn.cursor()

# Create the enlistments table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS developers (
        user_id INTEGER PRIMARY KEY,
        developer_name TEXT,
        developer_rank TEXT,
        status TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS certified_roles (
        developer_id INTEGER,
        role_name TEXT,
        FOREIGN KEY (developer_id) REFERENCES developers (user_id)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS projects (
        project_id INTEGER PRIMARY KEY,
        game TEXT,
        project_details TEXT,
        developer_payment REAL,
        deadline TEXT,
        status TEXT,
        assigned_to INTEGER,
        client INTEGER
    )
''')

conn.commit()

def user_nickname(user_id: int, guild: discord.Guild):
    # Iterate through the members of the specified guild to find the user with the given ID
    for member in guild.members:
        if member.id == user_id:
            nickname = member.nick if member.nick else member.name
            return nickname
    # If the user is not found in the specified guild, return None or an appropriate message
    return None

# Define a function to add certified roles to a developer
# developer_id is the user's ID, and role_name is the name of the certified role
def add_certified_role(developer_id, role_name):
    cursor.execute('''
        INSERT INTO certified_roles (developer_id, role_name)
        VALUES (?, ?)
    ''', (developer_id, role_name))
    conn.commit()

# Define a function to get the certified roles for a developer
# developer_id is the user's ID for whom you want to retrieve certified roles
def get_certified_roles(developer_id):
    cursor.execute('''
        SELECT role_name
        FROM certified_roles
        WHERE developer_id = ?
    ''', (developer_id,))
    return [row[0] for row in cursor.fetchall()]

def remove_certified_role(developer_id, role_name):
    developerRoles = get_certified_roles(developer_id=developer_id)
    # Check if the role_name exists in lowercase
    lowercase_role_name = role_name.lower()
    if lowercase_role_name in [cert.lower() for cert in developerRoles]:
        # Remove the role_name from the database
        cursor.execute('''
            DELETE FROM certified_roles
            WHERE developer_id = ? AND LOWER(role_name) = ?
        ''', (developer_id, lowercase_role_name))
        conn.commit()

schedule_message_id = 1155742171899633696
server = None
project_messages = {}
developer_earnings = {}
rF = []

async def rolesF():
    rF = [
        {
            "ranks": {
                "Chief Executive Officer": lambda server: discord.utils.get(server.roles, name="Chief Executive Officer"),
                "Chief Operations Officer": lambda server: discord.utils.get(server.roles, name="Chief Operations Officer"),
                "Account Executive": lambda server: discord.utils.get(server.roles, name="Account Executive"),
                "Developer": lambda server: discord.utils.get(server.roles, name="Developer"),
                "Staff": lambda server: discord.utils.get(server.roles, name="Staff"),
                "Sales Representative": lambda server: discord.utils.get(server.roles, name="Sales Representative"),
            },
        },
        {
            "certs": {
                "JSON Creator": lambda server: discord.utils.get(server.roles, name="JSON Creator"),
                "Server Configuration": lambda server: discord.utils.get(server.roles, name="Server Configuration"),
                "Script Developer": lambda server: discord.utils.get(server.roles, name="Script Developer"),
                "3D Modelling Engineer": lambda server: discord.utils.get(server.roles, name="3D Modelling Engineer"),
                "Web Developer": lambda server: discord.utils.get(server.roles, name="Web Developer"),
                "Bot Developer": lambda server: discord.utils.get(server.roles, name="Bot Developer"),
                "Social Media Engineer": lambda server: discord.utils.get(server.roles, name="Social Media Engineer"),
                "Map Developer": lambda server: discord.utils.get(server.roles, name="Map Developer"), 
                "Mod Technician": lambda server: discord.utils.get(server.roles, name="Mod Technician"),
                "Technical Administrator": lambda server: discord.utils.get(server.roles, name="Technical Administrator")
            },
        },
        {
            "statuses": {
                "Available": lambda server: discord.utils.get(server.roles, name="Available"),
                "Unavailable": lambda server: discord.utils.get(server.roles, name="Unavailable"),
                "onBreak": lambda server: discord.utils.get(server.roles, name="On Break"),
                "Busy": lambda server: discord.utils.get(server.roles, name="Busy"),
            },
        },
    ]
    
    return rF

async def get_status_role(server, status_name):
    rF = await rolesF()
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

@bot.event
async def on_ready():
    global server  # Make server a global variable
    server_id = 1088951646886842498 # Replace with your server ID
    server = bot.get_guild(server_id)  # Retrieve the server here
    
    global schedule_message_id
    schedule_channel_id = 1154179596682543125  # Replace with the actual channel ID
    schedule_channel = bot.get_channel(schedule_channel_id)
    
    # Check if the schedule message exists
    if schedule_message_id:
        try:
            # Fetch the message using the stored message ID
            schedule_message = await schedule_channel.fetch_message(schedule_message_id)
            # Update the embed with the latest information
            updated_embed = create_schedule_embed()  # Replace with your updated embed creation logic
            await schedule_message.edit(embed=updated_embed)
        except discord.NotFound:
            # The message doesn't exist; create a new one
            updated_embed = create_schedule_embed()  # Replace with your updated embed creation logic
            schedule_message = await schedule_channel.send(embed=updated_embed)
            schedule_message_id = schedule_message.id
    else:
        # Schedule message doesn't exist; create a new one
        updated_embed = create_schedule_embed()  # Replace with your updated embed creation logic
        schedule_message = await schedule_channel.send(embed=updated_embed)
        schedule_message_id = schedule_message.id

    # Start a background task to periodically update the embed
    update_schedule_embed.start()
    
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="CoderZ code!"))
    print(f'Logged in as {bot.user.name}')

@bot.command(name="restart", hidden=True)  # Hidden to prevent users from accidentally triggering it
@commands.is_owner()  # Only allow the bot owner to use this command
async def restart(ctx):
    await ctx.send("Restarting...")  # Send a message to indicate the restart

    # Change the bot's status to "Restarting"
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Game("Restarting..."))

    await bot.close()  # Gracefully close the bot

    # Use sys.executable to restart the bot using the same Python executable
    os.execl(sys.executable, sys.executable, *sys.argv)

@bot.command(name="admin_manage")
@commands.has_any_role('Chief Executive Officer', 'Chief Operations Officer', 1124886855494668298)
async def admin_manage(ctx, userID: int):
    member = server.get_member(userID)
    nickname = user_nickname(user_id=userID, guild=server)
    
    role_functions = {
        "Chief Executive Officer": lambda server: discord.utils.get(server.roles, name="Chief Executive Officer"),
        "Chief Operations Officer": lambda server: discord.utils.get(server.roles, name="Chief Operations Officer"),
        "Account Executive": lambda server: discord.utils.get(server.roles, name="Account Executive"),
        "Developer": lambda server: discord.utils.get(server.roles, name="Developer"),
        "Staff": lambda server: discord.utils.get(server.roles, name="Staff"),
        "Sales Representative": lambda server: discord.utils.get(server.roles, name="Sales Representative"),
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

    async def remove_roles_from_user(server):
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
        developerRoles = get_certified_roles(userID)
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
    qResp = await bot.wait_for("message", check=check, timeout=120)
    
    if qResp.content.lower() in ['1️⃣', '1', 'one']:
        while True:
            await ctx.author.send("What rank will they be put up to?")
            rank = await bot.wait_for("message", check=check, timeout=120)
            
            await ctx.author.send(f"Are you sure you want to give {nickname} the rank {rank.content}?")
            d = await bot.wait_for("message", check=check, timeout=120)
            
            if d.content.lower() == "yes" or d.content.lower() == "y":
                await remove_roles_from_user(server=server)
                
                rankMsg = rank.content
                rank_function = role_functions[0]["ranks"].get(rankMsg.lower())
                
                if rank_function:
                    rankObj = rank_function(server)
                    if rankObj:
                        await member.add_roles(rankObj)
                
                await ctx.author.send("Would you like the person to have the developer or staff role or shall they only have their rank role?\nPlease type either developer, staff or none.")
                d1 = await bot.wait_for("message", check=check, timeout=120)
                
                if d1.content.lower() == "developer" or "dev":
                    dev = discord.utils.get(server.roles, name="Developer")
                    await member.add_roles(dev)
                elif d1.content.lower() == "staff":
                    staff = discord.utils.get(server.roles, name="Staff")
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
                d2 = await bot.wait_for("message", check=check, timeout=120)
                
                if d2.content.lower() == "yes" or "y":
                    continue
                elif d2.content.lower() == "no" or "n":
                    break
                else:
                    await ctx.author.send("Invalid input detected.")
                    break
    elif qResp.content.lower() in ['2️⃣', '2', 'two']:
        
        await ctx.author.send("Would you like to add or remove a certification?")
        d1 = await bot.wait_for("message", check=check, timeout=120)
        
        if d1.content.lower() == "remove":
            await ctx.author.send("What certification would you like to remove from the developer?")
            await ctx.author.send(f"These are their current certifications: {developerRoles[:]}")
            r = await bot.wait_for("message", check=check, timeout=120)
            
            # Check if the role exists in the certifications dictionary
            if r.content in role_functions[1]["certs"]:
                role_lambda = role_functions[1]["certs"][r.content]
                role_to_remove = role_lambda(server)
                await member.remove_roles(role_to_remove)
                rMsg = r.content
                remove_certified_role(userID, rMsg)
            else:
                await ctx.author.send("The specified certification role doesn't exist.")
        elif d1.content.lower() == "add":
            await ctx.author.send("What certifications would you like to add?")
            await ctx.author.send(f"These are their current certifications: {developerRoles[:]}")
            r = await bot.wait_for("message", check=check, timeout=120)
            
            if r.content in role_functions[1]["certs"]:
                role_lambda = role_functions[1]["certs"][r.content]
                role_to_add = role_lambda(server)
                await member.add_roles(role_to_add)
                rMsg = r.content
                add_certified_role(userID, r.content)
            else:
                await ctx.author.send("The specified certification role doesn't exist.")
    elif qResp.content.lower() in ['3️⃣', '3', 'three']:
        statuses = ['available', 'unavailable', 'onbreak', 'busy']
        
        async def statusFunc():
                    await ctx.author.send("What status would you like to force this developer to have?")
                    r = await bot.wait_for("message", check=check, timeout=120)
                    
                    while True:
                        if r.content.lower() in statuses:
                            await ctx.author.send(f"To confirm: {nickname} will have the status: {r.content}.\nIs this correct?")
                            d = await bot.wait_for("message", check=check, timeout=120)
                            
                            if d.content.lower() in ['yes', 'y']:
                                try:
                                    statusObj = get_status_role(server=server, status_name=r.content)
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
                                r = bot.wait_for("message", check=check, timeout=120)
                                
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
                            r = bot.wait_for("message", check=check, timeout=120)
                            
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
                    
                currentStatusObj = discord.utils.get(server.roles, name=currentStatusU)
                await statusFunc()
            else:
                await ctx.author.send("Developer does not currently have a status.\nIf they have not been registered, it is recommended that they do first.\nIf you, please type override to continue.")
                r = await bot.wait_for("message", check=check, timeout=120)
                
                if r.content.lower() != "override":
                    await ctx.author.send("Current process has been stopped.")
                elif r.content.lower() == "override":
                    await statusFunc()
        except Exception as e:
            await ctx.author.send("Failed to fetch developers current status.")
            print(f"Error retrieving information from database: {e}")

@bot.command(name="ref")
async def ref(ctx):
    def check(message):
        return message.author == ctx.author and isinstance(message.channel, discord.DMChannel)

    await ctx.author.send("What is the service type?\n\n> 1 | Web Development\n> 2 | Server Configuration\n> 3 | Mod Configuration\n> 4 | JSON\n> 5 | Map Development\n> 6 | 3D Modelling (Texturing, Rigging, Animations...)\n> 7 | Bot Development\n> 8 | Scripting\n> 9 | Catalog\n> 10 | Other")

    def validate_service_type(message):
        return check(message) and message.content.isdigit() and 1 <= int(message.content) <= 10

    t = await bot.wait_for("message", timeout=120, check=validate_service_type)

    await ctx.author.send("What is the user's Discord ID?\n[How to get a user's Discord ID](https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-)")

    def validate_user_id(message):
        return check(message) and message.content.isdigit()  # You can add more specific validation if needed

    u = await bot.wait_for("message", timeout=120, check=validate_user_id)

    await ctx.author.send("What game is it for?\n\n> 1 | DayZ\n> 2 | Arma\n> 3 | Discord\n> 4 | Other")

    def validate_game(message):
        return check(message) and message.content.isdigit() and 1 <= int(message.content) <= 4

    g = await bot.wait_for("message", timeout=120, check=validate_game)

    await ctx.author.send("What is the deadline for the project?\n\nIn this format specifically: DDMMYYYY")

    def validate_deadline(message):
        return check(message) and len(message.content) == 8 and message.content.isdigit()

    d = await bot.wait_for("message", timeout=120, check=validate_deadline)

    await ctx.author.send("What is the invoice number?")

    def validate_invoice_number(message):
        return check(message) and message.content.isdigit()  # You can add more specific validation if needed

    i = await bot.wait_for("message", timeout=120, check=validate_invoice_number)
    
    service_type = t.content
    user_id = u.content
    game = g.content
    deadline = d.content
    invoice_number = i.content

async def createProjectDB(ctx, project_details, developer_payment, deadline, game, clientID):
    # Insert the project into the database
    cursor.execute('''
        INSERT INTO projects (game, project_details, developer_payment, deadline, status, assigned_to, client)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (game, project_details, float(developer_payment), deadline, "Unassigned", None, int(clientID)))
    
    conn.commit()

    # Send an embed to the specified channel with project details
    project_id = cursor.lastrowid  # Get the ID of the inserted project
    await send_project_embed(ctx, project_id=project_id)

@bot.command(name="create_project")
async def create_project(ctx):
    def check(message):
        return message.author == ctx.author and isinstance(message.channel, discord.DMChannel)

    # Ask questions in DMs and collect project details with emojis
    await ctx.author.send("What is the project for (DayZ, Arma)? 🎮")
    game = await bot.wait_for("message", check=check, timeout=120)
    
    await ctx.author.send("What does the project entail? ℹ️")
    project_details = await bot.wait_for("message", check=check, timeout=120)
    
    await ctx.author.send("What is the pay for the developer? 💰")
    developer_payment = await bot.wait_for("message", check=check, timeout=120)
    
    await ctx.author.send("When must the project be completed? ⏰")
    deadline = await bot.wait_for("message", check=check, timeout=120)

    # Insert the project into the database
    cursor.execute('''
        INSERT INTO projects (game, project_details, developer_payment, deadline, status, assigned_to)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (game.content, project_details.content, float(developer_payment.content), deadline.content, "Unassigned", None))
    
    conn.commit()

    # Send an embed to the specified channel with project details
    project_id = cursor.lastrowid  # Get the ID of the inserted project
    await send_project_embed(ctx, project_id)

@bot.command(name="claim_project")
async def claim_project(ctx, project_id: int):
    # Check if the project is already claimed
    cursor.execute('''
        SELECT assigned_to
        FROM projects
        WHERE project_id = ? AND status = 'Unassigned'
    ''', (project_id,))
    
    data = cursor.fetchone()
    
    if data:
        assigned_to = data[0]
        if assigned_to is None:
            # Mark the project as claimed
            cursor.execute('''
                UPDATE projects
                SET assigned_to = ?
                WHERE project_id = ?
            ''', (ctx.author.id, project_id))
            
            # Update the project status to 'In Progress'
            cursor.execute('''
                UPDATE projects
                SET status = 'In Progress'
                WHERE project_id = ?
            ''', (project_id,))
            
            conn.commit()
            
            await send_project_embed(ctx, project_id)
            
            await busy(userID=ctx.author.id)
            
            await ctx.send(f"Project #{project_id} has been claimed by {ctx.author.display_name}. Good luck!")
        else:
            await ctx.send(f"Project #{project_id} has already been claimed by {ctx.guild.get_member(assigned_to).display_name}.")
    else:
        await ctx.send(f"Project #{project_id} either does not exist or is no longer available.")

async def send_project_embed(ctx, project_id):
    cursor.execute('''
        SELECT game, project_details, developer_payment, deadline, status, assigned_to, client
        FROM projects
        WHERE project_id = ?
    ''', (project_id,))
    
    project_data = cursor.fetchone()

    if project_data:
        game, project_details, developer_payment, deadline, status, assigned_to, client = project_data
        
        embed = discord.Embed(
            title=f"Project #{project_id}",
            description=f"**🎮 | Game:** {game} \n\n"
                        f"**ℹ️ | Details:** {project_details} \n\n"
                        f"**💰 | Payment:** ${developer_payment} \n\n"
                        f"**⏰ | Deadline:** {deadline} \n\n"
                        f"**{'✅' if status == 'Completed' else '🚧' if status == 'In Progress' else '❓'} | Status:** {status} \n\n"
                        f"**Assigned To:** {ctx.guild.get_member(assigned_to).display_name if assigned_to else 'Unassigned'}\n\n\n"
                        f"*To assign this project to yourself, please go to bot commands and type `!claim_project {project_id}` to claim it.*",
            color=0x00ff00 if status == "Completed" else 0xff0000 if status == "Unassigned" else 0xffa500,
        )
        
        footer_image_url = "https://cdn.discordapp.com/attachments/1153394339691630676/1154519490411905187/Picsart_23-09-17_19-07-53-355-removebg-preview.png"  # Replace with the URL of your footer image
        embed.set_footer(icon_url=footer_image_url, text="CoderZ")
        
        project_channel_id = 1093241161587626065  # Replace with your project channel ID
        project_channel = bot.get_channel(project_channel_id)

        if project_id in project_messages:
            # If a message already exists for this project, edit it
            project_message = project_messages[project_id]
            await project_message.edit(embed=embed)
        else:
            # If no message exists, send a new one
            project_message = await project_channel.send(embed=embed)
            project_messages[project_id] = project_message
        
        try:
            Tickets.create_ticket(ctx=ctx, pNo=project_id, pDesc=project_details, pClient=client, pDeadline=deadline)
        except Exception as e:
            print("Failed to create ticket.")
    else:
        await ctx.send("Project not found.")

@bot.command(name="complete_project")
async def complete_project(ctx, project_id: int):
    # Check if the project is assigned to the developer
    cursor.execute('''
        SELECT assigned_to, developer_payment
        FROM projects
        WHERE project_id = ? AND assigned_to = ?
    ''', (project_id, ctx.author.id))
    
    data = cursor.fetchone()
    
    if data:
        assigned_to, developer_payment = data
        
        if assigned_to is not None:
            # Update the project status to 'Completed'
            cursor.execute('''
                UPDATE projects
                SET status = 'Completed'
                WHERE project_id = ?
            ''', (project_id,))
            
            conn.commit()
            
            # Record the completed project for the developer
            cursor.execute('''
                INSERT INTO completed_projects (developer_id, project_id)
                VALUES (?, ?)
            ''', (ctx.author.id, project_id))
            
            conn.commit()
            
            # Add the developer payment to the developer's earnings
            if ctx.author.id in developer_earnings:
                developer_earnings[ctx.author.id] += developer_payment
            else:
                developer_earnings[ctx.author.id] = developer_payment
            
            await send_project_embed(ctx, project_id)
            
            await ctx.send(f"Congratulations, {ctx.author.display_name}! You have completed project #{project_id}. Payment of ${developer_payment} has been added to your earnings.")
        else:
            await ctx.send(f"You cannot complete project #{project_id} as it is not assigned to you.")
    else:
        await ctx.send(f"Project #{project_id} either does not exist or is not assigned to you.")

@bot.command(name="developer_earnings")
async def developer_earnings(ctx):
    if ctx.author.id in developer_earnings:
        total_earnings = developer_earnings[ctx.author.id]
        await ctx.send(f"{ctx.author.display_name}, your total earnings are: ${total_earnings:.2f}")
    else:
        await ctx.send(f"{ctx.author.display_name}, you have not earned any money from completed projects yet.")
    
@tasks.loop(seconds=60)  # Adjust the interval as needed (e.g., update every hour)
async def update_schedule_embed():
    global schedule_message_id
    schedule_channel_id = 1154179596682543125  # Replace with the actual channel ID
    schedule_channel = bot.get_channel(schedule_channel_id)

    try:
        # Fetch the message using the stored message ID
        schedule_message = await schedule_channel.fetch_message(schedule_message_id)
        # Update the embed with the latest information
        updated_embed = create_schedule_embed()  # Replace with your updated embed creation logic
        await schedule_message.edit(embed=updated_embed)
    except discord.NotFound:
        # The message doesn't exist; create a new one
        updated_embed = create_schedule_embed()  # Replace with your updated embed creation logic
        schedule_message = await schedule_channel.send(embed=updated_embed)
        schedule_message_id = schedule_message.id

    # You can add additional logic here for handling exceptions, if necessary

@update_schedule_embed.before_loop
async def before_update_schedule_embed():
    await bot.wait_until_ready()

# Replace this function with your updated embed creation logic
def create_schedule_embed():
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

        developerNick = user_nickname(user_id=user_id, guild=server)
        
        embed.add_field(name=developerNick, value=f"➥ {status}", inline=True)

    return embed

@bot.command(name="register_developer")
async def register_developer(ctx):
    # Initialize an empty list to store certifications
    certifications = []
    
    def check(message):
        return message.author == ctx.author and isinstance(message.channel, discord.DMChannel)
    
    await ctx.author.send("What is the user ID of the developer who you are registering?")
    
    # Wait for the user's response
    r = await bot.wait_for("message", check=check, timeout=120)
    userID = r.content
    
    await ctx.author.send("What is the developer's name?\nE.g., Breath, Omni, Danny")
    
    # Wait for the user's response
    r = await bot.wait_for("message", check=check, timeout=120)
    developerName = r.content
    
    await ctx.author.send("What is the developer's rank?")
    
    # Wait for the user's response
    r = await bot.wait_for("message", check=check, timeout=120)
    developerRank = r.content
    
    await ctx.author.send("Enter the certifications one at a time. Type 'stop' to finish.")
    
    while True:
        # Wait for the user's response
        r = await bot.wait_for("message", check=check, timeout=120)
        
        # Check if the user wants to stop
        if r.content.lower() == "stop":
            break
        
        # Add the certification to the list
        certifications.append(r.content)
    
    try:
        cursor.execute('''
            INSERT INTO developers (user_id, developer_name, developer_rank, status)
            VALUES (?, ?, ?, ?)
        ''', (userID, developerName, developerRank, "available"))
        
        developer_id = cursor.lastrowid  # Get the ID of the inserted developer
        
        # Insert certifications into the certified_roles table
        for certification in certifications:
            cursor.execute('''
                INSERT INTO certified_roles (developer_id, role_name)
                VALUES (?, ?)
            ''', (developer_id, certification))
        
        conn.commit()
        await ctx.author.send(f"Developer {developerName} ({userID}) has been registered with rank {developerRank} and certifications: {', '.join(certifications)}")
    except sqlite3.Error as e:
        ctx.author.send("Error saving information to the database.")
        print(f"Error saving data to DB: {e}")

@bot.command(name="schedule")
async def schedule(ctx):
    embed = create_schedule_embed()
    
    await ctx.channel.purge(check=lambda msg: not msg.embeds or msg.embeds[0] != embed)
    
    # Send the embed message
    await ctx.send(embed=embed)
    
    # Wait for and delete any messages sent after the command
    def check_message(message):
        return message.author == ctx.author and message.channel == ctx.channel
    
    await bot.wait_for("message", check=check_message)  # Adjust the timeout as needed
        
    await ctx.channel.purge(limit=1)  # Delete the last message (the one sent after the command)

@bot.command(name="available")
async def available(ctx):
    member = server.get_member(ctx.author.id)
    available_role = discord.utils.get(server.roles, name="Available")
    unavailable_role = discord.utils.get(server.roles, name="Unavailable")
    onBreak_role = discord.utils.get(server.roles, name="On Break")
    
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

@bot.command(name="unavailable")
async def unavailable(ctx):
    member = server.get_member(ctx.author.id)
    available_role = discord.utils.get(server.roles, name="Available")
    unavailable_role = discord.utils.get(server.roles, name="Unavailable")
    onBreak_role = discord.utils.get(server.roles, name="On Break")
    
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

@bot.command(name="onBreak")
async def onBreak(ctx):
    member = server.get_member(ctx.author.id)
    available_role = discord.utils.get(server.roles, name="Available")
    unavailable_role = discord.utils.get(server.roles, name="Unavailable")
    onBreak_role = discord.utils.get(server.roles, name="On Break")
    
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

async def busy(userID):
    member = server.get_member(userID)
    available_role = discord.utils.get(server.roles, name="Available")
    unavailable_role = discord.utils.get(server.roles, name="Unavailable")
    onBreak_role = discord.utils.get(server.roles, name="On Break")
    busy_role = discord.utils.get(server.roles, name="Busy")
    
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
                await member.remove_roles(onBreak)
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

with open("config.json", "r") as f:
    config = json.load(f)
    
bot.run(f"{config['botkey']}")