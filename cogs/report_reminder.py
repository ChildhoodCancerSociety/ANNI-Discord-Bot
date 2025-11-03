from discord.ext import commands, tasks
import discord
from datetime import datetime, timezone, timedelta
import asyncio

'''

Program automatically sends a message to remind interns to submit their weekly report. This is sent between 12pm-1pm on Saturdays.

Note: this program can be set to send messages at a specific minute in the 12pm-1pm range, but it would need to run 60x as often to check every minute. 
      this can be configured in the wrapper around the weekly_reminder() function

'''

class Report_Reminder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.weekly_reminder.start()

    def cog_unload(self):
        self.weekly_reminder.cancel()

    @tasks.loop(minutes=60)  # NOTE where to configure how often this program runs/checks if it's time for the message. Parameter means it checks every 60 mins obviously. 
    async def weekly_reminder(self):
        now = datetime.now(timezone(timedelta(hours=-8), 'PST')) # NOTE time is set based on PST timezone
        
        if now.weekday() == 0 and now.hour == 10: # NOTE this is where to update the day/time the message is sent
            channel = self.bot.get_channel(895108659552583730)
            if channel:
                five = now.replace(hour=17, minute=0, second=0, microsecond=0)  # NOTE reports must be submitted by 5PM PST
                unix_timestamp = int(five.timestamp())
                discord_timestamp = f"<t:{unix_timestamp}:t>"
                await channel.send(f"Reminder to submit your weekly report by {discord_timestamp} today!")

    @weekly_reminder.before_loop
    async def before_weekly_task(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(Report_Reminder(bot))
