import discord
from discord.ext import commands

from cogs.utilities import Utilites
from cogs.project_management import ProjectManagement
from cogs.database import Database

class Invoice(commands.Cog):
    '''Invoice formatting and saving to the projects database.'''
    def __init__(self, bot):
        self.bot = bot
    
    def saveInvoice(self, data:dict):
        '''Formats invoice information and saves it to the projects database.'''
        refData = Utilites.decode(data["Reference"])
        
        if refData['Service Type'] in ['Catalog/Pre-made']:
            pass
        else:
            items_list = data.get("Items", [])
            
            # Accessing values inside the list
            for item in items_list:
                item_description = item.get("description", "")
                item_unit_amount = item.get("unit_amount", 0.0)
            
                if refData['Service Type'] in ['Server Configuration', 'Mod Configuration', 'JSON']:
                    developer_payment = item_unit_amount * 0.4 - (item_unit_amount * (3 / 100))
                elif refData['Service Type'] in ['Other', 'Map Development', '3D Modelling/Texturing']:
                    developer_payment = item_unit_amount * 0.5 - (item_unit_amount * (3 / 100))
                elif refData['Service Type'] in ['Bot Development', 'Web Development', 'Scripting']:
                    developer_payment = item_unit_amount * 0.55 - (item_unit_amount * (3 / 100))
                    
                Database.insert('''
                    INSERT INTO projects (project_id, game, project_details, developer_payment, deadline, status, assigned_to, client)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (data["Invoice Number"], refData['Game'], item_description, float(developer_payment), refData['Deadline'], "Unassigned", None, int(refData['Discord ID'])))

                ProjectManagement.send_project_embed(project_id=data["Invoice Number"])
    