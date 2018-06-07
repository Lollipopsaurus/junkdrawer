import asyncio
import discord
import json
import ebay_scraper
import gh_scraper
import reddit_scraper

client = discord.Client()

def get_configs():
    with open('discord_config.cfg') as configs:
        configs = json.load(configs)
        return configs

async def reddit_background_task(configs):
    await client.wait_until_ready()
    channel = discord.Object(id=configs['channel_id'])
    while not client.is_closed:
        stuff = reddit_scraper.main()
        for item in stuff:
            await client.send_message(channel, configs['user_id'] + ' item found! '+ item)
        await asyncio.sleep(configs['period']) # task runs every 30 seconds

async def ebay_background_task(configs):
    await client.wait_until_ready()
    channel = discord.Object(id=configs['channel_id'])
    while not client.is_closed:
        stuff = ebay_scraper.main()
        for item in stuff:
            await client.send_message(channel, configs['user_id'] + ' item found! '+ item)
        await asyncio.sleep(configs['period']) # task runs every 30 seconds

async def gh_background_task(configs):
    await client.wait_until_ready()
    channel = discord.Object(id=configs['channel_id'])
    while not client.is_closed:
        stuff = gh_scraper.main()
        for item in stuff:
            await client.send_message(channel, configs['user_id'] + ' item found! '+ item)
        await asyncio.sleep(configs['period']) # task runs every 30 seconds

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

configs = get_configs()
client.loop.create_task(reddit_background_task(configs))
client.loop.create_task(ebay_background_task(configs))
client.loop.create_task(gh_background_task(configs))
client.run(configs['bot_auth']) 
