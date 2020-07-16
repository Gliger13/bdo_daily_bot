import logging

import discord
from discord.ext import commands

from instruments import database_process
from messages import command_names, help_text, messages

module_logger = logging.getLogger('my_bot')


class Statistics(commands.Cog):
    database = database_process.DatabaseManager()

    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def user_stat_msg(user, user_info: dict, captain_info: dict):
        text_message = messages.no_data
        if user_info:
            if captain_info and captain_info.get('raids_created'):
                text_message = messages.captain_title
            else:
                text_message = messages.member_title

            text_message += (
                f"**{user_info.get('nickname')}**.\n"
            )

            if user_info.get('entries'):
                text_message += messages.raids_joined.format(
                    entries=user_info.get('entries')
                )
            else:
                text_message += messages.no_raids_joined
            if captain_info and captain_info.get('raids_created'):
                raids_created = captain_info.get('raids_created')
                drove_people = captain_info.get('drove_people')
                if raids_created < 5:
                    text_message += messages.drove_raids_l5.format(
                        raids_created=raids_created
                    )
                else:
                    text_message += messages.drove_raids_g5.format(
                        raids_created=raids_created
                    )
                if drove_people < 5:
                    text_message += messages.drove_people_l5.format(
                        drove_people=captain_info.get('drove_people')
                    )
                else:
                    text_message += messages.drove_people_g5.format(
                        drove_people=captain_info.get('drove_people')
                    )
                text_message += messages.last_time_drove.format(
                    last_created=captain_info.get('last_created')
                )

        embed = discord.Embed(
            title=messages.statistics_user_title,
            colour=discord.Colour.blue(),
            description=text_message
        )
        if user:
            embed.set_author(
                name=str(user),
                icon_url=user.avatar_url,
            )
        return embed

    @commands.command(name=command_names.function_command.user_statistics, help=help_text.user_statistics)
    async def user_statistics(self, ctx: commands.context.Context, nickname=''):
        user = None
        if nickname:
            user_info = self.database.user.find_user_post_by_name(nickname)
            if user_info:
                captain_info = self.database.captain.find_captain_post(user_info['discord_user'])
                user = self.bot.get_user(user_info['discord_id'])
            else:
                captain_info = None
        else:
            user = ctx.author
            user_info = self.database.user.find_user_post(str(user))
            captain_info = self.database.captain.find_captain_post(str(user))

        embed = self.user_stat_msg(user, user_info, captain_info)
        await ctx.send(embed=embed)
        module_logger.info(f'{ctx.author} удачно использовал команду {ctx.message.content}')

    @commands.command(name=command_names.function_command.guild_statistics, help=help_text.guild_statistics)
    @commands.has_permissions(administrator=True, manage_messages=True)
    async def guild_statistics(self, ctx: commands.context.Context):
        guild = ctx.guild
        user = ctx.author
        guild_info = self.database.settings.find_settings_post(guild.id)
        text_message = messages.no_data
        if guild_info and guild_info.get('can_remove_in_channels'):
            text_message = messages.can_remove_msgs_in
            for channel_id, channel in guild_info.get('can_remove_in_channels').items():
                text_message += f" - **{channel}**\n"

        embed = discord.Embed(
            title=messages.statistics_guild_title,
            colour=discord.Colour.blue(),
            description=text_message
        )

        embed.set_author(
            name=str(guild),
            icon_url=user.guild.icon_url,
        )
        await ctx.send(embed=embed)
        module_logger.info(f'{ctx.author} удачно использовал команду {ctx.message.content}')


def setup(bot):
    bot.add_cog(Statistics(bot))
    module_logger.debug(f'Успешный запуск bot.statistics')
