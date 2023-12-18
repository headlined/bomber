# Import libraries:
import discord as Discord;

import json as JSON;
import os as OS;
import inspect as Inspect;
import requests as Requests;

from PIL import Image;

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

            if Data["Debug"] == True:
                await Interaction.response.send_message(f"# Setting Configurated. \n* Debug mode has been set to {Data['Debug']} \n* This means that you will not be able to use most commands.",
                                                        ephemeral = False)
                
            else:
                await Interaction.response.send_message(f"# Setting Configurated. \n* Debug mode has been set to {Data['Debug']} \n* This means that you will be able to use every single command.",
                                                        ephemeral = False)

        except Exception as Exc:
            print(Exc)

            User = await self.Client.fetch_user("1002377371892072498")
            await Interaction.response.send_message("# An Error Has Occurred.. \n* Do not worry, <@1002377371892072498> has already been notified of this bug & will patch it shortly. \n* Please be patient whilst this is being fixed! \n\n__If the bug is not resolved in 24hr, please leave a comment under out [GitHub](https://github.com/Suno0526/Bomber/issues) page.__",
                                                    ephemeral = True)

            Line = Inspect.currentframe().f_lineno + 1
            await User.send(f"# Command Failure @ Line {Line} \n* The command **{Interaction.command.name}** failed to respond, providing the error code: \n\n> {Exc}")

    @AppCommands.command(name = "save", description = "Save the current server's information to a JSON file.")
    async def B(self, Interaction: Discord.Interaction):
        Data = JSON.loads(open("Information.json", "r").read())
        Debug = Data['Debug']

        if Debug == True:
            await Interaction.response.send_message("# An Error Has Occurred. \n* If you want to use any commands, **please disable debug mode** by running **/debug** \n* __This is to prevent any issues with the bot.__ \n\nIf you are a developer, please note that debug mode is enabled & you will not be able to use any commands.** \n\n-Thanks, from <@1002377371892072498>.",
                                                    ephemeral=True)
        else:
            try:
                Previous = f"./Servers/{Interaction.guild.id}.json"
                if OS.path.exists(Previous):
                    OS.remove(Previous)

                Data = {
                    "Name": Interaction.guild.name,
                    "Icon": Interaction.guild.icon.url if Interaction.guild.icon is not None else None,
                    "Channels": {},
                    "VoiceChannels": {},
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

                    elif isinstance(Channel, Discord.VoiceChannel):
                        Data["VoiceChannels"][Channel.id] = {
                            "Name": Channel.name,
                            "Position": Channel.position,
                            "Category": Channel.category.name if Channel.category is not None else None,
                            "Type": Channel.type
                        }

                JSON.dump(Data, open(f"./Servers/{Interaction.guild.id}.json", "w+"), indent=4)

                await Interaction.response.send_message(content = "# Server Saved. \n* Your server has been backed up by a 1:1 replica JSON file. \n\n__To restore your server, please run **/restore**.__", file = Discord.File(f"./Servers/{Interaction.guild.id}.json", filename = f"{Interaction.guild.id}.json"))

            except Exception as Exc:
                print(Exc)

                User = await self.Client.fetch_user("1002377371892072498")
                await Interaction.response.send_message("# An Error Has Occurred.. \n* Do not worry, <@1002377371892072498> has already been notified of this bug & will patch it shortly. \n* Please be patient whilst this is being fixed! \n\n__If the bug is not resolved in 24hr, please leave a comment under out [GitHub](https://github.com/Suno0526/Bomber/issues) page.__",
                                                        ephemeral=True)

                Line = Inspect.currentframe().f_lineno + 1
                await User.send(f"# Command Failure @ Line {Line} \n* The command **{Interaction.command.name}** failed to respond, providing the error code: \n\n> {Exc}")

    @AppCommands.command(name = "restore", description = "Attempt to bring back the corrupted server.")
    async def C(self, Interaction: Discord.Interaction):
        Data = JSON.loads(open("Information.json", "r").read())
        Debug = Data['Debug']

        if Debug == True:
            await Interaction.response.send_message("# An Error Has Occurred. \n* If you want to use any commands, **please disable debug mode** by running **/debug** \n* __This is to prevent any issues with the bot.__ \n\nIf you are a developer, please note that debug mode is enabled & you will not be able to use any commands.** \n\n-Thanks, from <@1002377371892072498>.",
                                                    ephemeral=True)
        else:
            try:
                for Channel in Interaction.guild.channels:
                    try:
                        await Channel.delete()

                    except Exception as Exc:
                        pass

                Data = JSON.load(open(f"./Servers/{Interaction.guild.id}.json", "r+"))

                Categories = {}
                for VoiceChannelID, VoiceChannelData in Data['VoiceChannels'].items():
                    CategoryName = VoiceChannelData['Category']
                    if CategoryName is not None:
                        if CategoryName not in Categories:
                            Category = await Interaction.guild.create_category(name = CategoryName)
                            Categories[CategoryName] = Category
                        else:
                            Category = Categories[CategoryName]
                    else:
                        Category = None

                    await Interaction.guild.create_voice_channel(name = VoiceChannelData['Name'], category = Category)

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

            except Exception as Exc:
                print(Exc)

                User = await self.Client.fetch_user("1002377371892072498")
                await Interaction.response.send_message("# An Error Has Occurred.. \n* Do not worry, <@1002377371892072498> has already been notified of this bug & will patch it shortly. \n* Please be patient whilst this is being fixed! \n\n__If the bug is not resolved in 24hr, please leave a comment under out [GitHub](https://github.com/Suno0526/Bomber/issues) page.__",
                                                        ephemeral=True)

                Line = Inspect.currentframe().f_lineno + 1
                await User.send(f"# Command Failure @ Line {Line} \n* The command **{Interaction.command.name}** failed to respond, providing the error code: \n\n> {Exc}")

    @AppCommands.command(name = "del-save", description = "Delete the current server's save file.")
    async def D(self, Interaction: Discord.Interaction):
        Data = JSON.loads(open("Information.json", "r").read())
        Debug = Data['Debug']

        if Debug == True:
            await Interaction.response.send_message("# An Error Has Occurred. \n* If you want to use any commands, **please disable debug mode** by running **/debug** \n* __This is to prevent any issues with the bot.__ \n\nIf you are a developer, please note that debug mode is enabled & you will not be able to use any commands.** \n\n-Thanks, from <@1002377371892072498>.",
                                                    ephemeral=True)
        else:
            try:
                Previous = f"./Servers/{Interaction.guild.id}.json"
                if OS.path.exists(Previous):
                    OS.remove(Previous)

                await Interaction.response.send_message("# Server Save Deleted. \n* Your server's save file has been deleted. \n\n__To save your server, please run **/save**.__")

            except Exception as Exc:
                print(Exc)

                User = await self.Client.fetch_user("1002377371892072498")
                await Interaction.response.send_message("# An Error Has Occurred.. \n* Do not worry, <@1002377371892072498> has already been notified of this bug & will patch it shortly. \n* Please be patient whilst this is being fixed! \n\n__If the bug is not resolved in 24hr, please leave a comment under out [GitHub](https://github.com/Suno0526/Bomber/issues) page.__",
                                                        ephemeral=True)

                Line = Inspect.currentframe().f_lineno + 1
                await User.send(f"# Command Failure @ Line {Line} \n* The command **{Interaction.command.name}** failed to respond, providing the error code: \n\n> {Exc}")


# Sync our stuff:
async def setup(Client: Commands.Bot):
    await Client.add_cog(Secure(Client))