# Import libraries:
import discord as Discord;
import asyncio as Asyncio;

import random as Random;
import json as JSON;
import os as OS;

from discord.ext import commands as Commands;
from typing import Literal, Optional; 


# Create thy instance:
Intents = Discord.Intents.all()
Bomber  = Commands.Bot(command_prefix = "b.", intents = Intents)

Tree = Bomber.tree


# Open our outside information:
Data = JSON.loads(open("Information.json", "r").read())


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


# Create thy syncing command standalone:
"""
Code recycled from https://about.abstractumbra.dev/discord.py/2023/01/29/sync-command-example.html
"""
@Bomber.command()
@Commands.is_owner()

async def sync(CTX: Commands.Context, Guilds: Commands.Greedy[Discord.Object], Spec: Optional[Literal["~", "*", "^"]] = None) -> None:
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

        await CTX.send(f"# Commands Synced. \n* All new commands have been connted to the command tree. \n\n__If the command does not show, please restart Discord using **CTRL + R** or **CMD + R** on MacOS.__")
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


# Create the final instance:
async def Main():
    async with Bomber:
        await Load()
        await Bomber.start(Token)


# Load thy instance:
Asyncio.run(Main())
