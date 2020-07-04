#!/usr/bin/env python3
# bot.py

# --------------------- [ IMPORTS ] --------------------- #
import os
import sys
import json
import discord
import random
import time
from datetime import datetime
from dotenv import load_dotenv
# ------------------------------------------------------- #

# ----------------- [ INITIALISATIONS ] ----------------- #
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN_LAHEY')
client = discord.Client()
# ------------------------------------------------------- #

# -------------------- [ FUNCTIONS ] -------------------- #
def write_log(msg, log_type="info"):
    """Custom log function"""
    if log_type == "info":
        prompt = "[-]"
    elif log_type == "warn":
        prompt = "[!]"
    elif log_type == "error":
        prompt = "[x]"
    else:
        prompt = "[~]"

    fmt_msg   = "[{0}] {1} {2}"
    timestamp = datetime.now().strftime("%H:%M:%S.%f")
    print(fmt_msg.format(timestamp, prompt, msg))

# ------------------ [ EVENT HANDLERS ] ----------------- #
@client.event
async def on_ready():
    write_log(f'joined server as {client.user}')

@client.event
async def on_message(message):

    # Ignore messages from self
    if message.author == client.user:
        write_log("{0} says: {1}".format(message.author, message.content))
        return

    # Process commands
    if client.user in message.mentions:
        with open("./lahey.json", 'r') as file_ptr:
            quotes = json.load(file_ptr)
        msg = random.choice(quotes)["text"]

        if "_ricky_" in msg:
            ricky = next((x for x in message.guild.members if x.name == "Ricky LaFleur"), None)
            if ricky is None:
                write_log("couldn't find Jim Lahey in server", log_type="error")
                msg = msg.replace("_ricky_", "Ricky")
            else:
                msg = msg.replace("_ricky_", ricky.mention)
        try:
            await message.channel.send(msg)
        except:
            write_log("error")

# ------------------------------------------------------- #

# -------------------- [ MAIN LOGIC ] ------------------- #
if __name__ == "__main__":
    try:
        client.run(TOKEN)
    except KeyboardInterrupt:
        write_log("Disconnecting...")
        client.close()
# ------------------------------------------------------- #