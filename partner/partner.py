import discord
from discord.ext import commands

from core import checks
from core.models import PermissionLevel


class Partner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.plugin_db.get_partition(self)

    @commands.group(invoke_without_command=True)
    @checks.has_permissions(PermissionLevel.OWNER)
    async def partner(self, ctx):
        """
        Settings and stuff
        """
        await ctx.send_help(ctx.command)
        return

    @partner.command()
    @checks.has_permissions(PermissionLevel.OWNER)
    async def channel(self, ctx, channel: discord.TextChannel):
        """
        Set the partner channel
        """
        if ctx.message.guild == 686724930687074372:
            await self.db.find_one_and_update(
                {"_id": "config"}, {"$set": {"channel": channel.id}}, upsert=True
            )

            await ctx.send("Partner Channel Set")
            return 

    @partner.command()
    @checks.has_permissions(PermissionLevel.OWNER)
    async def setup(self, ctx):
        if ctx.author.bot:
          return

        channel_config = await self.db.fine_one({"_id": "config"})

        if channel_config is None:
            return await ctx.send("There's no configured partner channel.")
        else:
            channel = ctx.guild.get_channel(int(channel_config["channel"]))
        
        if channel is None:
            return

        server = await self.db.find_one({"guildid": ctx.channel.guild})

        if server is None:
        
            embed=discord.Embed(title="Aluxes", url="https://discord.gg/ugyxpnC", description="A Relaxing Chill Community!")
            embed.add_field(name="What We Offer", value="Advertising\nGames\nPremium-Advertising\nReactionRoles\nPartnerships\nGiveaways\nSFW-Community\nFriendly-Channels\n\nThis server is meant for entertainment and relaxation. Please join and earn rewards for being active, inviting friends and more as we cannot wait to here from you! https://discord.gg/bAgVPdw https://media1.giphy.com/media/35B3Val0pYgtpScqsz/giphy.gif", inline=False)
            
            partnerid = await ctx.send(embed=embed)
            
            await self.db.insert_one(
              {
                "id": ctx.author.id,
                "name": ctx.author.name,
                "guildid": ctx.channel.guild,
                "channelid": ctx.channel.id,
                "messageid": partnerid,
              })

        else:

            embed=discord.Embed(description="You are our partner already ")
            await ctx.send(embed=embed)
    
def setup(bot):
    bot.add_cog(Partner(bot))