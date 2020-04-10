from discord import Embed, Message, User
from discord.ext.commands import Bot, Cog, Context, group

from core.checks import has_permissions
from core.models import PermissionLevel


class Partner(Cog):

    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.db: AsyncIOMotorCollection = bot.plugin_db.get_partition(self)

	@group.command()
	@has_permissions(PermissionLevel.Owner)
	async def parnter(self, ctx: Context) -> None:
		"""
        Settings and stuff
        """
        await ctx.send_help(ctx.command)
        return

	@parnter.command(name="setup")
	@has_permissions(PermissionLevel.Owner)
	async def setup(self, ctx: Context) -> None:
		if message.author.bot:
			return

		server = await self.db.find_one({"id": message.channel.guild})

		if server is None:
			
			embed=discord.Embed(title="Aluxes", url="https://discord.gg/ugyxpnC", description="A Relaxing Chill Community!")
			embed.add_field(name="What We Offer", value="Advertising\nGames\nPremium-Advertising\nReactionRoles\nPartnerships\nGiveaways\nSFW-Community\nFriendly-Channels\n\nThis server is meant for entertainment and relaxation. Please join and earn rewards for being active, inviting friends and more as we cannot wait to here from you! https://discord.gg/bAgVPdw https://media1.giphy.com/media/35B3Val0pYgtpScqsz/giphy.gif", inline=False)
			
			parnterid = await ctx.send(embed=embed)
			await self.db.insert_one(
				{
					"id": message.channel.guild,
					"name": message.author.name,
					"channelid": message.channel.id,
					"messageid": parnterid,
				})

		else:

			embed=discord.Embed(description="You are our partner already ")
			await ctx.send(embed=embed)


def setup(bot: Bot) -> None:
    bot.add_cog(Partner(bot))