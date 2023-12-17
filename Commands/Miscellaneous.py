# Import libraries:
import discord as Discord;

import random as Random;
import json as JSON;

from discord import app_commands as AppCommands;
from discord.ext import commands as Commands;


# Create our class:
class Miscellaneous(Commands.Cog):
    def __init__(self, Client: Commands.Bot):
        self.Client = Client
        self.Tree = Client.tree

    
    # Create thy commands:
    @AppCommands.command(name = "cog-test", description = "Attempt a conversation between Discord and the cogs.")
    async def A(self, Interaction: Discord.Interaction):
        await Interaction.response.send_message("Hello, I am a cog! It seems like cogs are configurated correctly, as I am able to respond to your command.")

    @AppCommands.command(name = "test", description = "Respond with a random message to validate the bot's status.")
    async def B(self, Interaction: Discord.Interaction):
        Data = JSON.loads(open("Information.json", "r").read())
        Debug = Data['Debug']

        if Debug == True:
            await Interaction.response.send_message("# An Error Has Occurred. \n* If you want to use any commands, **please disable debug mode** by running **/debug** \n* __This is to prevent any issues with the bot.__ \n\nIf you are a developer, please note that debug mode is enabled & you will not be able to use any commands.** \n\n-Thanks, from <@1002377371892072498>.",
                                                    ephemeral = True)
        else:
            try:
                Messages = ["My friend <@1176985904481566824> says hello.", "Oh, hello there!", "How are you today?", "I love trees.", "Did you know, there are different species of Zebra?", "Chickens don't grow from trees.", "Donations are appreciated! Fun fact: They also can spike my motivation for future projects!", "Unfortunately, this bot is against the Terms of Service...", "If you see this.. HELLO!", "There's a 1 in 13 chance of seeing this!", "I wrote this message on December 13th, 2023 at 11:05 PM. ...Goodnight!", "Hey apple! ...If you understand that reference, consider yourself old.", "Is it just me... ooor do other people realize that a universal languages would be amazing?", "HELLLOOOOOO, from Suno!"]

                await Interaction.response.send_message(Random.choice(Messages),
                                                        ephemeral = False)
            except Exception as Exc:
                print(Exc)

                await Interaction.response.send_message(":warning:  An error has occurred. \n<@1002377371892072498> has been notified of this bug & will report a bug fix that will be released globally shortly.",
                                                        ephemeral = True)

    @AppCommands.command(name = "ping", description = "Respond with the bot's latency.")
    async def C(self, Interaction: Discord.Interaction):
        Data = JSON.loads(open("Information.json", "r").read())
        Debug = Data['Debug']

        if Debug == True:
            await Interaction.response.send_message("# An Error Has Occurred. \n* If you want to use any commands, **please disable debug mode** by running **/debug** \n* __This is to prevent any issues with the bot.__ \n\nIf you are a developer, please note that debug mode is enabled & you will not be able to use any commands.** \n\n-Thanks, from <@1002377371892072498>.",
                                                    ephemeral = True)
        else:
            try:
                Messages = ["Pong!", "Currently running @", "Potato salad is gross..", "Fried chicken!", "I love cows.", "FROGS ARE AMAZING!", "You proomesed my son free Robux!!!"]

                await Interaction.response.send_message(f"{Random.choice(Messages)} (**{round(self.Client.latency * 1000)}ms** of latency)",
                                                        ephemeral = False)
            except Exception as Exc:
                print(Exc)

                await Interaction.response.send_message(":warning:  An error has occurred. \n<@1002377371892072498> has been notified of this bug & will report a bug fix that will be released globally shortly.",
                                                        ephemeral = True)


# Sync our stuff:
async def setup(Client):
    await Client.add_cog(Miscellaneous(Client))
