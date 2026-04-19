import discord
from discord.ext import commands
from discord import app_commands

class Ticket(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="ticket_setup", description="Ticket Button Setup")
    @app_commands.checks.has_permissions(administrator=True)
    async def ticket_setup(self, interaction: discord.Interaction):
        if not interaction.guild:
            return await interaction.response.send_message("Only available in servers!", ephemeral=True)

        embed = discord.Embed(title="🎫 Support", description="Click below to open a ticket.", color=0x3498db)
        embed.set_footer(text="Powered by ShreeCloud")
        
        view = discord.ui.View(timeout=None)
        btn = discord.ui.Button(label="Open Ticket", style=discord.ButtonStyle.green, custom_id="shree_t", emoji="📩")
        
        async def button_callback(interaction: discord.Interaction):
            guild = interaction.guild
            if not guild: return
            
            ov = {
                guild.default_role: discord.PermissionOverwrite(view_channel=False), 
                interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True),
                guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True)
            }
            
            ch = await guild.create_text_channel(f"ticket-{interaction.user.name}", overwrites=ov)
            await interaction.response.send_message(f"Created: {ch.mention}", ephemeral=True)
            await ch.send(f"Hello {interaction.user.mention}, how can we help? | Powered by ShreeCloud")

        btn.callback = button_callback
        view.add_item(btn)
        await interaction.response.send_message(embed=embed, view=view)

async def setup(bot: commands.Bot):
    await bot.add_cog(Ticket(bot))