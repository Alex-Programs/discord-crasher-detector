import discord
import validator
from threading import *
import os
import re
import database
from dotenv import load_dotenv

load_dotenv()

client = discord.Client()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    attachmentList = []
    extensions = ["mp4", "gif", "mkv"]

    for i in message.attachments:
        for extension in extensions:
            if extension in i.url:
                attachmentList.append(i.url)
                break

    try:
        text = re.search("(?P<url>https?://[^\s]+)", message.content).group("url")
        if "gfycat" in text:
            for extension in extensions:
                if extension in text:
                    attachmentList.append(text)
                    break
                
    except AttributeError:
        pass

    print(str(attachmentList))

    for attachment in attachmentList:
        if database.links.count({"url" : attachment}) > 0:
            await message.delete()
            print("Deleting from stored links " + attachment)
            return

    for attachment in attachmentList:
        result = await validator.get_and_check(attachment)
        if result == True:
            await message.delete()
            print("Deleting " + attachment)
            database.links.update_one({"url" : attachment}, {"$set" : {"url" : attachment}}, upsert=True)
            break
    
client.run(os.environ["TOKEN"])