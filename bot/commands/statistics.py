import logging

import discord
from discord.ext import commands

from instruments import database_process

module_logger = logging.getLogger('my_bot')


class RaidSaveLoad(commands.Cog):
    database = database_process.Database()

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='стат')
    async def get_user_statistics(self, ctx: commands.context.Context):
        user = ctx.author
        user_info = self.database.find_user_post(str(user))
        captain_info = self.database.find_captain_post(str(user))
        if not user_info and not captain_info:
            text_message = f"Нету данных"
        if user_info:
            if captain_info and captain_info.get('raids_created'):
                text_message = (
                    f"Капитан "
                )
            else:
                text_message = (
                    f"Моряк "
                )
            text_message += (
                f"**{user_info.get('nickname')}**.\n"
            )
            if user_info.get('entries'):
                text_message += (
                    f"Посетил рейдов: **{user_info.get('entries')}**.\n"
                )
            else:
                text_message += (
                    f"Не плавал как пассажир.\n"
                )
            if captain_info and captain_info.get('raids_created'):
                raids_created = captain_info.get('raids_created')
                drove_people = captain_info.get('drove_people')
                if raids_created < 5:
                    text_message += (
                        f"Отвёз **{raids_created}** рейда.\n"
                    )
                else:
                    text_message += (
                        f"Отвёз **{raids_created}** рейдов.\n"
                    )
                if drove_people < 5:
                    text_message += (
                        f"Всего **{captain_info.get('drove_people')}** человека отвёз.\n"
                    )
                else:
                    text_message += (
                        f"Всего **{captain_info.get('drove_people')}** человек отвёз.\n"
                    )
                text_message += (
                    f"Последний отвезённый рейд был **{captain_info.get('last_created')}**.\n"
                )

        embed = discord.Embed(
            title='Статистика',
            colour=discord.Colour.blue(),
            description=text_message
        )

        embed.set_author(
            name=str(user),
            icon_url=user.avatar_url,
        )
        await user.send(embed=embed)
        module_logger.info(f'{ctx.author} удачно использовал команду {ctx.message.content}')


def setup(bot):
    bot.add_cog(RaidSaveLoad(bot))
    module_logger.debug(f'Успешный запуск bot.statistics')
