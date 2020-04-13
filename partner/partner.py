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
        await self.db.find_one_and_update(
            {"_id": "config"}, {"$set": {"channel": channel.id, "guild": channel.guild.id}}, upsert=True
        )

        await ctx.send(f"Partner Channel Set {channel.name}")
        return 

    @partner.command()
    @checks.has_permissions(PermissionLevel.OWNER)
    async def setup(self, ctx):
        if ctx.author.bot:
            return

        channel_config = await self.db.find_one({"_id": "config"})

        if channel_config is None:
            return await ctx.send("There's no configured partner channel.")
        else:
            channel = ctx.guild.get_channel(int(channel_config["channel"]))
            guild = ctx.guild.get_channel(int(channel_config["guild"]))
        
        if channel is None:
            return await ctx.send("Can't find Partner Channel!")

        partner = await self.db.find_one({"_id": "partner"})

        if partner is None:
            partner = await self.db.insert_one({"id": "partner"})

        embed=discord.Embed(description=f"Welcome to the Aluxes Partner setup menu!", color=0x950EE7)
        embed.add_field(name="Setting Your Partner Channel", value=f"Please enter a channel you would like to send a Aluxes Partner Message in\nThis can be done by using the `#` key and entering the channel name directly after it without a space. Make sure your channel is visible to everyone on the server", inline=False)
        await ctx.send(embed=embed)

        channel: discord.Message = await self.bot.wait_for("message", check=check)
        if cancel_check(channel) is True:
            await ctx.send("Cancelled!")
            return
        else:
            if channel.channel_mentions[0] is None:
                await ctx.send("Cancelled as no channel was provided")
                return
            else:
                schan = channel.channel_mentions[0]

        try:
            partnerid = partner[str(ctx.channel.guild.id)]
        except KeyError:
            partnerid = partner[str(ctx.channel.guild.id)] = []

        if partnerid is None:
            embed=discord.Embed(title="Aluxes", url="https://discord.gg/ugyxpnC", description="A Relaxing Chill Community!")
            embed.add_field(name="What We Offer", value="Advertising\nGames\nPremium-Advertising\nReactionRoles\nPartnerships\nGiveaways\nSFW-Community\nFriendly-Channels\n\nThis server is meant for entertainment and relaxation. Please join and earn rewards for being active, inviting friends and more as we cannot wait to here from you! https://discord.gg/bAgVPdw https://media1.giphy.com/media/35B3Val0pYgtpScqsz/giphy.gif", inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send("You are our partner already!")

    @partner.command()
    @checks.has_permissions(PermissionLevel.OWNER)
    async def remove(self, ctx, guild:int):
        """
        Remove Partner from the server
        Usage:
        {prefix}partner remove {guild.id}
        """
        if ctx.author.bot:
            return
        
        channel_config = await self.db.find_one({"_id": "config"})

        if channel_config is None:
            return await ctx.send("There's no configured partner channel.")
        else:
            channel = ctx.guild.get_channel(int(channel_config["channel"]))
        
        if channel is None:
            return 

        try:
            partnerid = partner[int(guild.id)]
        except KeyError:
            return await ctx.send(f"{guild.name} are not our partner.")

        if partnerid is None:
            await ctx.send(f"{guild} are not our partner.")
        
        await self.db.find_one_and_update(
            {"_id": "partner"}, {"$set": {int(guild): []}}
        )

        await ctx.send(f"Successfully removed partner **{guild.name}**")


def setup(bot):
    bot.add_cog(Partner(bot))