import asyncio
import discord
import json
import ebay_scraper
import gh_scraper
import reddit_scraper
import argparse

client = discord.Client()
message_list = []
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
            await client.send_message(channel, 'item found! '+ item)
        await asyncio.sleep(configs['period']) # task runs every 30 seconds

async def ebay_background_task(configs):
    await client.wait_until_ready()
    channel = discord.Object(id=configs['channel_id'])
    while not client.is_closed:
        stuff = ebay_scraper.main()
        for item in stuff:
            await client.send_message(channel,  'item found! '+ item)
        await asyncio.sleep(configs['period']) # task runs every 30 seconds

async def send_mess(messages):
    await client.wait_until_ready()
    channel = discord.Object(id=configs['channel_id'])
    for message in messages:
        await client.send_message(channel, message)

# on_ready function
@client.event
async def on_ready():
    client.wait_until_ready()
    # Bad logging to show that the bot ran
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

    channel = discord.Object(id=configs['channel_id'])
    count = 0

    # Open the notification file (can be whatever notification queue in the future)
    with open('notifications.txt', 'r') as message_list:
        json_obj = json.loads(message_list.read())
        # Send the message for each item in the file
        for message in json_obj:
            await client.send_message(channel, '' + message)
            #count += 1
        # If we reach the end, 
        #if count == len(json_obj):
        for task in asyncio.Task.all_tasks():
            try:
                task.cancel()
            except Exception as e:
                pass
            client.loop.stop()

configs = get_configs()

#client.run(configs['bot_auth']) 
def main():
    #client.run(configs['bot_auth'])
    try:
        client.loop.run_until_complete(client.start(configs['bot_auth']))
    except Exception as e:
        pass
    finally:
        client.logout()
        return

if __name__ == "__main__":
    main()
