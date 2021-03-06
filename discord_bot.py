import asyncio
import discord
import json
import ebay_scraper
import gh_scraper
import reddit_scraper

client = discord.Client()
message_list = []
def get_configs():
    with open('discord_config.cfg') as configs:
        configs = json.load(configs)
        return configs

# on_ready function
@client.event
async def on_ready():
    await client.wait_until_ready()
    # Bad logging to show that the bot ran
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

    channel = client.get_channel(id=configs['channel_id'])
    count = 0

    # Open the notification file (can be whatever notification queue in the future)
    with open('notifications.txt', 'r') as message_list:
        json_obj = json.loads(message_list.read())
        print(json_obj)
        # Send the message for each item in the file
        for message in json_obj:
            print('message: ' + message)
            await channel.send(content=message)
        for task in asyncio.Task.all_tasks():
            try:
                task.cancel()
            except Exception as e:
                print(e)
                pass
            #finally:
            #    await client.close()
            #    client.loop.stop()

configs = get_configs()

def main():
    try:
        client.loop.run_until_complete(client.start(configs['bot_auth']))
    except Exception as e:
        pass
    finally:
        try:
            loop.close()
            client.clear()
            client.loop.run_until_complete(client.close()) 
        except Exception as e:
            pass
        return

if __name__ == "__main__":
    main()
