import disnake
from disnake.ext import commands
from Utils.Embeds import Embeds
import json


class dm(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guild_id = 1038964213961457674
        self.owner_id = 439623921369874442
        self.head_admin = 927581845787402240
        self.admin = 776741719814438933
        self.category_id = 1140097773098766406
        self.footer = 'made by charis_k'

    @commands.slash_command(description='Open a dm with info on how to get help')
    async def open_dm(self, inter: disnake.ApplicationCommandInteraction):
        try:
            await inter.response.defer()
            author = inter.author
            guild = inter.guild

            if guild and guild.id == self.guild_id:
                member = await guild.fetch_member(int(author.id))

                if member:
                    try:
                        with open('cogs/banned_users.json', 'r') as f:
                            banned_users = json.load(f)

                        if author.id not in banned_users:
                            channel_dm = await author.create_dm()
                            await channel_dm.send(
                                f'Hi {author.display_name}, I saw you asked for support in the server. '
                                f'I created a private channel for us to chat on. <3')

                            category_name = f'Support for {author.display_name}'
                            category = disnake.utils.get(guild.categories, id=self.category_id)

                            # Create a text channel within the specified category
                            private_channel = await guild.create_text_channel(category_name, category=category)
                            embed = Embeds.embed_builder(
                                'Support Created',
                                author=author,
                                footer=self.footer
                            )
                            embed.add_field(name=f'Support chanel {private_channel.mention}',value='')

                            owner = await guild.fetch_member(self.owner_id)
                            head_admin = await guild.fetch_member(self.head_admin)
                            admin = await guild.fetch_member(self.admin)
                            await inter.edit_original_response(embed)
                            await private_channel.set_permissions(target=author, read_messages=True, send_messages=True)
                            await private_channel.send(f'Hi {author.mention}')
                            await private_channel.send(
                                f'The admins are {owner.mention}, {head_admin.mention}, and {admin.mention}')

                            # Save the channel ID under the user's category
                            issues = {}
                            if author.id in issues:
                                issues[private_channel.id][author.id] = True
                            else:
                                issues[private_channel.id] = {'author': author.id}

                            with open('cogs/issues.json', 'r') as g:
                                json.dump(issues, g, indent=4)

                            mod_channel = await guild.fetch_channel(1039098304350404649)
                            await mod_channel.send(
                                f'Hi admins, a wild {author.display_name} wants support in {private_channel.mention}')
                        else:
                            embed = Embeds.embed_builder(
                                title='Problem',
                                author=author
                            )
                            embed.add_field(name=f'Sorry {author.mention} you are banned from support')
                            await inter.edit_original_response(embed=embed)
                    except Exception as e:
                        embed = Embeds.error_embed(
                            footer=self.footer,
                            value=e
                        )
                        await inter.edit_original_response(embed=embed)
                else:
                    await inter.send("Unable to find member.")
        except Exception as e:
            embed = Embeds.error_embed(
                footer=self.footer,
                value=e
            )
            await inter.edit_original_response(embed=embed)

    @commands.slash_command(description='Ban someone from support')
    async def ban_user(
            self,
            inter: disnake.ApplicationCommandInteraction,
            member: disnake.Member = commands.param(name='member')
    ):
        try:
            await inter.response.defer()
            with open('cogs/banned_users.json', 'r') as f:
                banned_users = json.load(f)

            author = inter.author
            if author.id in {self.owner_id, self.head_admin, self.admin}:
                banned_users[member.id] = True
                with open('cogs/banned_users.json', 'w') as f:
                    json.dump(banned_users, f, indent=4)
            else:
                await inter.send(
                    f'Hi {author.mention}, you are not an admin, so don\'t try to ban people.')
        except Exception as e:
            embed = Embeds.error_embed(
                footer=self.footer,
                value=e
            )
            await inter.edit_original_response(embed=embed)



    @commands.slash_command()
    async def close_dm(
            self,
            inter: disnake.ApplicationCommandInteraction,
                       ):
        try:
            await inter.response.defer()
            author = inter.author
            with open('cogs/issues.json', 'r') as f:
                issues = json.load(f)
            channel_id = inter.channel.id
            author_id = issues[channel_id]['author']

            if author.id == [self.admin,self.head_admin,self.owner_id,author_id]:
                guild = inter.guild
                channel = guild.get_channel(channel_id)

                if issues[channel_id]:
                    if issues[channel_id]['author']:
                        await channel.set_permissions(target=author_id, read_messages=False, send_messages=False)
                        id_author = await guild.fetch_member(author_id)
                        await inter.edit_original_response(f'{id_author.display_name} has been removed and his support is over')
                        closer = await guild.fetch_member(author.id)
                        await id_author.send(f'Your support request has been terminated by {closer.display_name}')


        except Exception as e:
            embed = Embeds.error_embed(
                footer=self.footer,
                value=e
            )
            await inter.edit_original_response(embed=embed)


def setup(bot):
    bot.add_cog(dm(bot))
