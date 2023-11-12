import datetime
import disnake
import traceback


class Embeds:

    @staticmethod
    def embed_builder(title, description=None, author=None, footer='Maintained by charis_k', thumbnail=None,
                      maintain_bot=False,
                      your_name=None):
        embed = disnake.Embed(
            title=title,
            description=description,
            color=0x008000,
            timestamp=datetime.datetime.now()
        )
        try:
            if author is not None:
                if maintain_bot:
                    bot_name = ""
                    embed.set_author(
                        name=f"Queried by {author.display_name} - Maintained by {bot_name}",
                        icon_url=author.avatar.url if author.avatar else None
                    )
                else:
                    if your_name:
                        embed.set_author(
                            name=f"Queried by {author.display_name} - Maintained by {your_name}",
                            icon_url=author.avatar.url if author.avatar else None
                        )
                    else:
                        embed.set_author(
                            name=f"Queried by {author.display_name} ",
                            icon_url=author.avatar.url if author.avatar else None
                        )

            if footer is not None:
                embed.set_footer(
                    icon_url="https://cdn.discordapp.com/attachments/1131117599321768037/1166897760398745620/Jeff_bot_logo.jpg?ex=655e9e39&is=654c2939&hm=bc4734926ce2c950cfb126a961d5fe11f0c1811dbe73addf3cbd07791be91b90&",
                    text=footer
                )
            else:
                embed.set_footer(
                    icon_url="https://cdn.discordapp.com/attachments/1131117599321768037/1166897760398745620/Jeff_bot_logo.jpg?ex=655e9e39&is=654c2939&hm=bc4734926ce2c950cfb126a961d5fe11f0c1811dbe73addf3cbd07791be91b90&",
                    text="Jeff_"
                )

            if thumbnail is not None:
                embed.set_thumbnail(url=thumbnail)

                embed.set_image(
                    url="https://cdn.discordapp.com/attachments/1050945545037951048/1099030835220467872/linebreak.png")

            return embed
        except Exception as e:
            raise e


    @staticmethod
    def error_embed(value, type=None, footer=None, ):
        try:
            if type != "userError":
                traceback.print_exc()

            embed = Embeds.embed_builder(title="`Error`", footer=footer)

            embed.add_field(name="Something went wrong", value=value, inline=True)

            return embed
        except Exception as e:
            raise e
