import discord
import discord.utils
import os
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setLevel(logging.INFO)

logger.addHandler(handler)

intents = discord.Intents.default()
intents.message_content=True

target_channel = os.getenv("TARGET_CHANNEL")

bot_token = os.getenv("BOT_TOKEN")

# create an instance of a Client, which is our connection to Discord
client = discord.Client(intents=intents) 

@client.event
async def on_ready():
    print(f'Comrade is ready to spread propoganda!')
    logger.info(f'Comrade is ready to spread propoganda!')


@client.event
async def on_message(message):
    # ignores messages from ourselves
    if message.author == client.user:
        logging.info("Message was from the bot. Ignoring.")
        return
    
    # if messages starts with hello
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
        logging.info("Message Sent: Hello!")


@client.event
async def on_voice_state_update(member, before, after):
    # if the bot is not already in a channel
    print(f"before: {before}")
    print(f"after: {after}")
    if after.channel:
        # User connected to a voice channel
        print(f"{member.name} connected to {after.channel.name}")
        logging.info("User connected to a voice channel")

        print(f"channel id: {after.channel.id}")
        print(f"voice clients: {client.voice_clients}")

        # if channel matches gulag and bot not connected to a voice channel
        # I should probably break this into its own function, which I can then unit test separately
        if after.channel.id == target_channel and not client.voice_clients:
            play_audio(after, 'ussr_anthem.mp3')
            logging.info("playing comrade anthem")
            

    if before.channel:
        # User disconnected from a voice channel
        logging.info(f"{member.name} disconnected from the {before.channel.name} voice channel")

        print(client.voice_clients)

        guild = before.channel.guild

        voice_client = discord.utils.get(client.voice_clients, guild=guild)

        print(len(client.voice_clients[0].channel.members))

        if client.voice_clients:
            if len(client.voice_clients[0].channel.members) == 1 and voice_client.is_connected():
                await voice_client.disconnect()


async def play_audio(voice_state, audio_source):
    voice = await voice_state.channel.connect(self_deaf=True)
    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(source=audio_source), volume=0.1)
    await voice.play(source)

if __name__ == "__main__":
    client.run(bot_token, log_handler=handler)
