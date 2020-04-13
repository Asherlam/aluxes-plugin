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
            {"_id": "config"}, {"$set": {"channel": channel.id}}, upsert=True
        )

        await ctx.send("Partner Channel Set")
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
        
        if channel is None:
            return await ctx.send("Can't find Partner Channel!")

        partner = await self.db.find_one({"_id": "partner"})

        if partner is None:
            partner = await self.db.insert_one({"id": "partner"})

        try:
            partnerid = partner[str(ctx.message.guild.id)]
        except KeyError:
            partnerid = partner[str(ctx.message.guild.id)] = []

        if partnerid is None:
            newpartner = []
        else:
            newpartner = partnerid.copy()

        newpartner.append({"guildid": ctx.message.guild.id})

    @partner.command()
    @checks.has_permissions(PermissionLevel.OWNER)
    async def remove(self, ctx, guild_id:int):
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
            partnerid = partner[str(guild_id.id)]
        except KeyError:
            return await ctx.send(f"{guild_id} are not our partner.")

        if partnerid is None:
            await ctx.send(f"{guild_id} are not our partner.")
        
        await self.db.find_one_and_update(
            {"_id": "partner"}, {"$set": {str(guild_id): []}}
        )

        await ctx.send(f"Successfully removed partner **{guild_id}**")


def setup(bot):
    bot.add_cog(Partner(bot))