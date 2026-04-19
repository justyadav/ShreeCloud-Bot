import discord
import os
import json
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from flask import Flask, jsonify
from threading import Thread

# 1. Setup Flask (The Website Backend)
app = Flask('')

@app.route('/api/stats')
def get_stats():
    return jsonify({
        "servers": len(bot.guilds),
        "users": sum(guild.member_count for guild in bot.guilds if guild.member_count),
        "status": "Online"
    })

def run_web():
    app.run(host='0.0.0.0', port=5000)

# 2. Load Token
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# 3. Database Functions
def get_config():
    if not os.path.exists('config.json'):
        with open('config.json', 'w') as f: json.dump({}, f)
    with open('config.json', 'r') as f:
        return json.load(f)

def save_config(data):
    with open('config.json', 'w') as f:
        json.dump(data, f, indent=4)

# 4. Bot Class
class ShreeCloudBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=discord.Intents.all(), help_command=None)

    async def setup_hook(self):
        # Load Cogs
        base_path = os.path.dirname(os.path.abspath(__file__))
        cogs_path = os.path.join(base_path, 'cogs')
        for filename in os.listdir(cogs_path):
            if filename.endswith('.py') and filename != '__init__.py':
                await self.load_extension(f'cogs.{filename[:-3]}')
                print(f"✅ Loaded: {filename}")

    async def on_ready(self):
        # Set Activity
        activity = discord.Game(name="Powered by ShreeCloud")
        await self.change_presence(status=discord.Status.online, activity=activity)
        
        # Sync Slash Commands
        try:
            synced = await self.tree.sync()
            print(f"🔄 Synced {len(synced)} commands.")
        except Exception as e:
            print(f"❌ Sync error: {e}")
        
        print(f"🚀 {self.user} is live!")

bot = ShreeCloudBot()

# --- SERVER-SPECIFIC SETTING COMMAND ---
@bot.tree.command(name="setup_logs", description="Set log channel for this server")
@app_commands.checks.has_permissions(administrator=True)
async def setup_logs(interaction: discord.Interaction, channel: discord.TextChannel):
    data = get_config()
    data[str(interaction.guild_id)] = {"log_channel": channel.id}
    save_config(data)
    await interaction.response.send_message(f"✅ Logs set to {channel.mention} | Powered by ShreeCloud", ephemeral=True)

# 5. Start Everything
if __name__ == "__main__":
    Thread(target=run_web).start() # Start Web API
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("❌ No token found in .env")