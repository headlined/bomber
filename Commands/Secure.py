# Import libraries:
import discord as Discord;
from discord import Permissions;

import json as JSON;
import os as OS;

from discord import app_commands as AppCommands;
from discord.ext import commands as Commands;


# Disclose our JSON:
with open("Information.json", "r+") as Info:
    Data = JSON.load(Info)


# Create our class:
class Secure(Commands.Cog):
    def __init__(self, Client: Commands.Bot):
        self.Client = Client
        self.Tree = Client.tree

    
    # Create thy commands:
    @AppCommands.command(name = "debug", description = "Toggle debug mode.")
    async def A(self, Interaction: Discord.Interaction):
        global Data

        try:
            Data["Debug"] = not Data["Debug"]
            JSON.dump(Data, open("Information.json", "w+"), indent = 4)

        except Exception as Exc:
            print(Exc)

            await Interaction.response.send_message(":warning:  An error has occurred. \n<@1002377371892072498> has been notified of this bug & will report a bug fix that will be released globally shortly.",
                                                    ephemeral = True)

    @AppCommands.command(name="save-test", description="Save the current server's information to a JSON file.")
    async def B(self, Interaction: Discord.Interaction):
        Data = JSON.loads(open("Information.json", "r").read())
        Debug = Data['Debug']

        if Debug == True:
            await Interaction.response.send_message("# An Error Has Occurred. \n* If you want to use any commands, **please disable debug mode** by running **/debug** \n* __This is to prevent any issues with the bot.__ \n\nIf you are a developer, please note that debug mode is enabled & you will not be able to use any commands.** \n\n-Thanks, from <@1002377371892072498>.",
                                                    ephemeral = True)
        else:
            try:
                await Interaction.response.send_message("Saving server information to a JSON file...")

                Data = {
                    "Channels": {},
                    "Roles": {},
                    "Categories": {}
                }

                for Category in Interaction.guild.categories:
                    Data["Categories"][Category.id] = {
                        "Name": Category.name,
                        "Position": Category.position
                    }

                for Channel in Interaction.guild.channels:
                    if isinstance(Channel, Discord.TextChannel):
                        Data["Channels"][Channel.id] = {
                            "Name": Channel.name,
                            "Position": Channel.position,
                            "Category": Channel.category.name if Channel.category is not None else None,
                            "Type": Channel.type
                        }

                JSON.dump(Data, open(f"./Servers/{Interaction.guild.id}.json", "w+"), indent=4)

                await Interaction.edit_original_response(content = "Saved server information to a JSON file.")

            except Exception as Exc:
                print(Exc)

                await Interaction.response.send_message(":warning:  An error has occurred. \n<@1002377371892072498> has been notified of this bug & will report a bug fix that will be released globally shortly.",
                                                        ephemeral = True)

    @AppCommands.command(name = "restore", description = "Attempt to bring back the corrupted server.")
    async def C(self, Interaction: Discord.Interaction):
        Data = JSON.loads(open("Information.json", "r").read())
        Debug = Data['Debug']

        if Debug == True:
            await Interaction.response.send_message("# An Error Has Occurred. \n* If you want to use any commands, **please disable debug mode** by running **/debug** \n* __This is to prevent any issues with the bot.__ \n\nIf you are a developer, please note that debug mode is enabled & you will not be able to use any commands.** \n\n-Thanks, from <@1002377371892072498>.",
                                                    ephemeral = True)
            
        else:
            try:
                for Channel in Interaction.guild.channels:
                    try:
                        await Channel.delete()

                    except Exception as Exc:
                        pass

                Data = JSON.load(open(f"./Servers/{Interaction.guild.id}.json", "r+"))

                Categories = {}

                for ChanneliD, ChannelData in Data['Channels'].items():
                    CategoryName = ChannelData['Category']
                    if CategoryName is not None:
                        if CategoryName not in Categories:
                            Category = await Interaction.guild.create_category(name = CategoryName)
                            Categories[CategoryName] = Category

                        else:
                            Category = Categories[CategoryName]

                    else:
                        Category = None

                    await Interaction.guild.create_text_channel(name = ChannelData['Name'], category = Category)

                OS.remove(f"./Servers/{Interaction.guild.id}.json")

            except Exception as Exc:
                print(Exc)

                await Interaction.response.send_message(":warning:  An error has occurred. \n<@1002377371892072498> has been notified of this bug & will report a bug fix that will be released globally shortly.",
                                                        ephemeral = True)


# Sync our stuff:
async def setup(Client: Commands.Bot):
    await Client.add_cog(Secure(Client))
