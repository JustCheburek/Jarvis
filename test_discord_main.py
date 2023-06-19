import asyncio

import discord

import config

bot = discord.Bot()


@bot.command()
async def start(ctx):  # If you're using commands.Bot, this will also work
    channel = ctx.channel
    voice = ctx.author.voice

    if not voice:
        return await ctx.respond("Ты не в войсе!")

    vc = await voice.channel.connect()  # Connect to the voice channel the author is in

    await ctx.respond("Запись началась!")

    vc.start_recording(
        discord.sinks.WaveSink(),  # The sink type to use
        once_done,  # What to do once done
        channel  # The channel to disconnect from
    )

    await asyncio.sleep(10)

    vc.stop_recording()  # Stop recording, and call the callback (once_done)


async def once_done(
    sink: discord.sinks, channel: discord.TextChannel, *_
):  # Our voice client already passes these in
    recorded_users = []
    files = []

    for user_id, audio in sink.audio_data.items():
        user_id = str(user_id)
        recorded_users.append(user_id)
        files.append(discord.File(audio.file, f"{user_id}.{sink.encoding}"))

    await channel.send(
        f"Запись закончена, эти люди участвовали в ней:\n" + '\n'.join(recorded_users), files=files
    )


bot.run(config.DISCORD_TOKEN)
