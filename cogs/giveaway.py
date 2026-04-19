import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import random

class Giveaway(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="giveaway", description="Start a giveaway")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def giveaway(self, interaction: discord.Interaction, duration: int, prize: str):
        # Assertion to fix Pylance "send" error
        if not isinstance(interaction.channel, (discord.TextChannel, discord.Thread)):
            return await interaction.response.send_message("Use this in a text channel!", ephemeral=True)

        embed = discord.Embed(title="🎁 GIVEAWAY! 🎁", description=f"Prize: **{prize}**\nEnds in: **{duration}s**", color=0xFFAA00)
        embed.set_footer(text="Powered by ShreeCloud")
        
        await interaction.response.send_message("Giveaway Started!", ephemeral=True)
        msg = await interaction.channel.send(embed=embed)
        await msg.add_reaction("🎉")
        
        await asyncio.sleep(duration)
        
        msg = await interaction.channel.fetch_message(msg.id)
        if msg.reactions:
            users = [u async for u in msg.reactions[0].users() if not u.bot]
            if users:
                winner = random.choice(users)
                await interaction.channel.send(f"🎊 {winner.mention} won the **{prize}**!")
                return
        await interaction.channel.send("No entries found.")

async def setup(bot: commands.Bot):
    await bot.add_cog(Giveaway(bot))