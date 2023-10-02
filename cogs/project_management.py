import discord, sqlite3
from discord.ext import commands

conn = sqlite3.connect('data/coderz.db')
cursor = conn.cursor()

from cogs.statuses import Statuses
from cogs.ticket_system import TicketSystem

class ProjectManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.project_messages = {}
    
    @commands.command(name="create_project")
    async def create_project(self, ctx):
        def check(message):
            return message.author == ctx.author and isinstance(message.channel, discord.DMChannel)

        await ctx.author.send("What is the project number/project ID? ⭐")
        project_no = await self.bot.wait_for("message", check=check, timeout=120)
        
        # Ask questions in DMs and collect project details with emojis
        await ctx.author.send("What is the project for (DayZ, Arma)? 🎮")
        game = await self.bot.wait_for("message", check=check, timeout=120)
        
        await ctx.author.send("What does the project entail? ℹ️")
        project_details = await self.bot.wait_for("message", check=check, timeout=120)
        
        await ctx.author.send("What is the pay for the developer? 💰")
        developer_payment = await self.bot.wait_for("message", check=check, timeout=120)
        
        await ctx.author.send("When must the project be completed? ⏰")
        deadline = await self.bot.wait_for("message", check=check, timeout=120)
        
        await ctx.author.send("What is the client's Discord User ID? E.g. 1827340182873091")
        clientID = await self.bot.wait_for("message", check=check, timeout=120)

        # Insert the project into the database
        cursor.execute('''
            INSERT INTO projects (project_id, game, project_details, developer_payment, deadline, status, assigned_to, client)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (project_no, game.content, project_details.content, float(developer_payment.content), deadline.content, "Unassigned", None, int(clientID)))
        
        conn.commit()

        # Send an embed to the specified channel with project details
        project_id = cursor.lastrowid  # Get the ID of the inserted project
        await self.send_project_embed(ctx, project_id)

    @commands.command(name="claim_project")
    async def claim_project(self, ctx, project_id: int):
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
                
                await self.send_project_embed(ctx, project_id)
                
                await Statuses.busy(userID=ctx.author.id)
                
                await TicketSystem.add_developer(ctx=ctx, developer_id=ctx.author.id)
                
                await ctx.send(f"Project #{project_id} has been claimed by {ctx.author.display_name}. Good luck!")
            else:
                await ctx.send(f"Project #{project_id} has already been claimed by {ctx.guild.get_member(assigned_to).display_name}.")
        else:
            await ctx.send(f"Project #{project_id} either does not exist or is no longer available.")

    @classmethod
    async def send_project_embed(self, ctx, project_id):
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
            project_channel = self.bot.get_channel(project_channel_id)

            if project_id in self.project_messages:
                # If a message already exists for this project, edit it
                project_message = self.project_messages[project_id]
                await project_message.edit(embed=embed)
            else:
                # If no message exists, send a new one
                project_message = await project_channel.send(embed=embed)
                self.project_messages[project_id] = project_message
            
            try:
                TicketSystem.create_ticket(ctx=ctx, pNo=project_id, pDesc=project_details, pClient=client, pDeadline=deadline)
            except Exception as e:
                print(f"Failed to create ticket: {e}")
        else:
            await ctx.send("Project not found.")

    @commands.command(name="complete_project")
    async def complete_project(self, ctx, project_id: int):
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
                    INSERT INTO completed_projects (developer_id, project_id, developer_payment)
                    VALUES (?, ?, ?)
                ''', (ctx.author.id, project_id, developer_payment))
                
                conn.commit()
                
                await self.send_project_embed(ctx, project_id)
                
                await ctx.send(f"Congratulations, {ctx.author.display_name}! You have completed project #{project_id}. Payment of ${developer_payment} has been added to your earnings and will be sent to your account within 14 days.")
                try:
                    await TicketSystem.close_ticket(ctx=ctx, channel_name=f"ticket-{project_id}")
                except Exception as e: 
                    await ctx.author.send("Could not close the project ticket - please report this to a technical administrator.")
            else:
                await ctx.send(f"You cannot complete project #{project_id} as it is not assigned to you.")
        else:
            await ctx.send(f"Project #{project_id} either does not exist or is not assigned to you.")
