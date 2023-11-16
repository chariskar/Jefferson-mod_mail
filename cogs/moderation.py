import disnake
from disnake.ext import commands


class ModerationCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @commands.slash_command()
    @commands.has_permissions(ban_members=True)
    async def ban(self,
                  inter: disnake.ApplicationCommandInteraction,
                  member: disnake.Member = commands.param('member'),
                  reason: str = commands.param('reason')):
        permissions = inter.channel.permissions_for(member)
        if permissions.ban_members:
            baned = inter.guild.get_member(member.id)
            await baned.ban(reason=reason)

            await inter.response.send_message(f"{inter.author.display_name} kicked {baned.display_name} ")
        else:
            await inter.response.send_message(
                f"{inter.author.display_name} does not have the 'Kick Members' permission.")
def setup(bot):
    bot.add_cog(ModerationCommands(bot))
