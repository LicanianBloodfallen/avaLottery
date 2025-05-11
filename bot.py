import os
import discord
from discord.ext import commands
from google_sheets import GoogleSheetsClient

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
CREDENTIALS_PATH = os.getenv("GOOGLE_SHEETS_CREDENTIALS")

# Initialize Google Sheets client
gs_client = GoogleSheetsClient(SPREADSHEET_ID, CREDENTIALS_PATH)

intents = discord.Intents.default()
intents.voice_states = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command(name='check')
async def check(ctx, voice_channel: discord.VoiceChannel):
    members = [member.name for member in voice_channel.members]
    date = ctx.message.created_at.strftime("%Y-%m-%d")
    leader = ctx.author.name
    # Save locally
    gs_client.record_attendance(date, members, leader)
    # Send confirmation
    await ctx.send(f"Recorded attendance for {date}: {', '.join(members)}")

@bot.command(name='summary')
async def summary(ctx):
    summary_data = gs_client.get_monthly_summary()
    msg = "📅 Monthly Summary:\n"
    for user, points in summary_data['points'].items():
        msg += f"- {user}: {points} pts, {summary_data['leaders'].get(user,0)} RL\n"
    await ctx.send(msg)

@bot.command(name='leaderboard')
async def leaderboard(ctx):
    summary_data = gs_client.get_monthly_summary()
    leaderboard_msg = "**Leaderboard**\n"
    for user, points in sorted(summary_data['points'].items(), key=lambda x: x[1], reverse=True):
        leaderboard_msg += f"- {user}: {points} pts\n"
    await ctx.send(leaderboard_msg)

if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
