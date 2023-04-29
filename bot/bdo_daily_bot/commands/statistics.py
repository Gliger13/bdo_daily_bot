"""
Module contain discord cog with name `Statistics`. Provide discord command to get
user and guild statistics from the database.
"""
import discord
from discord import Embed
from discord import User
from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext.commands import Context

from bdo_daily_bot.core.commands_reporter.reporter import Reporter
from bdo_daily_bot.core.database.manager import DatabaseManager
from bdo_daily_bot.core.logger import log_template
from bdo_daily_bot.messages import command_names
from bdo_daily_bot.messages import help_text
from bdo_daily_bot.messages import messages


class Statistics(commands.Cog):
    """
    Cog that provides all collected statistics
    """

    database = DatabaseManager()

    def __init__(self, bot: Bot):
        """
        :param bot: discord bot for executing the cog commands
        """
        self.bot = bot
        self.reporter = Reporter()

    @staticmethod
    def user_stat_msg(user: User, user_info: dict, captain_info: dict) -> Embed:
        """
        Transform given user information in the discord embed

        :param user: discord user of given information
        :param user_info: information from the user collection
        :param captain_info: information from the captain collection
        :return: discord embed with all user information
        """
        text_message = messages.no_data
        if user_info:
            # Choose a title whichever user drove or not people
            if captain_info and captain_info.get("raids_created"):
                text_message = messages.captain_title
            else:
                text_message = messages.member_title

            # Add the user game nickname
            text_message += f"**{user_info.get('nickname')}**.\n"

            # Add information about whether the user joined raids or not
            if user_info.get("entries"):
                text_message += messages.raids_joined.format(entries=user_info.get("entries"))
            else:
                text_message += messages.no_raids_joined

            # Add information about whether the user drove people or not.
            if captain_info and captain_info.get("raids_created"):
                raids_created = captain_info.get("raids_created")
                drove_people = captain_info.get("drove_people")
                if raids_created < 5:
                    text_message += messages.drove_raids_l5.format(raids_created=raids_created)
                else:
                    text_message += messages.drove_raids_g5.format(raids_created=raids_created)
                if drove_people < 5:
                    text_message += messages.drove_people_l5.format(drove_people=captain_info.get("drove_people"))
                else:
                    text_message += messages.drove_people_g5.format(drove_people=captain_info.get("drove_people"))
                text_message += messages.last_time_drove.format(last_created=captain_info.get("last_created"))

        embed = Embed(title=messages.statistics_user_title, colour=discord.Colour.blue(), description=text_message)
        # Add avatar
        if user:
            embed.set_author(
                name=str(user),
                icon_url=user.avatar_url,
            )
        return embed

    @commands.command(name=command_names.function_command.user_statistics, help=help_text.user_statistics)
    async def user_statistics(self, ctx: Context, nickname: str = ""):
        """
        Command to send user collected information as message in channel from context

        :param ctx: discord command context
        :param nickname: game nickname of the user to provide information
        """
        # Check specific user
        if nickname:
            # Try to find user in db
            user_info = await self.database.user.find_user_by_nickname(nickname)
            # If user exist try to find captain activity in db
            if user_info:
                captain_info = await self.database.captain.find_captain_post(user_info["discord_id"])
                user = self.bot.get_user(user_info["discord_id"])
            else:
                return
        else:
            # If specific user not exist get current user
            user = ctx.author
            user_info = await self.database.user.get_user_by_id(user.id)
            captain_info = await self.database.captain.find_captain_post(user.id)

        embed = self.user_stat_msg(user, user_info, captain_info)
        await ctx.send(embed=embed)
        await self.reporter.report_success_command(ctx)

    @commands.command(name=command_names.function_command.guild_statistics, help=help_text.guild_statistics)
    @commands.has_permissions(administrator=True, manage_messages=True)
    async def guild_statistics(self, ctx: Context):
        """
        Command to send guild collected information as message in current channel from context

        :param ctx: discord command context
        """
        guild = ctx.guild
        user = ctx.author
        guild_info = await self.database.settings.find_settings_post(guild.id)

        # Collect all information from db

        if guild_info:
            text_message = ""

            # Information about getting role from clicking reaction
            role_from_reaction = guild_info.get("role_from_reaction")
            if role_from_reaction:
                for message_id in role_from_reaction:
                    role_reaction_message = messages.can_get_role_from.format(message_id=message_id)
                    for emoji, role_id in role_from_reaction.get(str(message_id)).items():
                        role = discord.utils.get(guild.roles, id=role_id)
                        role_reaction_message += messages.reaction_role.format(role=role, emoji=emoji)
                    text_message += role_reaction_message

            # Information about ability to remove channels
            if guild_info and guild_info.get("can_remove_in_channels"):
                text_message += messages.can_remove_msgs_in
                for _, channel in guild_info.get("can_remove_in_channels").items():
                    text_message += f" - *#{channel}*\n"
        else:
            text_message = messages.no_data

        embed = discord.Embed(
            title=messages.statistics_guild_title, colour=discord.Colour.blue(), description=text_message
        )

        embed.set_author(
            name=str(guild),
            icon_url=user.guild.icon_url,
        )

        await ctx.send(embed=embed)
        await self.reporter.report_success_command(ctx)


def setup(bot: Bot):
    """
    Function to add statistics cog to the given bot

    :param bot: discord bot to add the cog
    """
    bot.add_cog(Statistics(bot))
    log_template.cog_launched("Statistics")
