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
TOKEN = os.getenv('DISCORD_TOKEN_RICKY')
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
        if message.author.name == "Jim Lahey" and message.author.bot:
            with open("./ricky_responses.json") as file_ptr:
                responses = json.load(file_ptr)
            msg = random.choice(responses)["text"]
        else:
            with open("./ricky.json") as file_ptr:
                quotes = json.load(file_ptr)
            quote = random.choice(quotes)
            msg = quote["text"]

        if "_jim_" in msg:
            jim = next((x for x in message.guild.members if x.name == "Jim Lahey"), None)
            if jim is None:
                write_log("couldn't find Jim Lahey in server", log_type="error")
                msg = msg.replace("_jim_", "Lahey")
            else:
                msg = msg.replace("_jim_", jim.mention)
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