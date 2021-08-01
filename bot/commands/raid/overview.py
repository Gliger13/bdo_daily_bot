"""
Module contain discord cog with name `RaidOverview`. Provide commands to
overview raids information
"""
import discord
from discord.ext import commands
from discord.ext.commands import Bot, Context

from core.commands_reporter.command_failure_reasons import CommandFailureReasons
from core.commands_reporter.reporter import Reporter
from core.database.manager import DatabaseManager
from core.logger import log_template
from core.tools import check_input
from messages import command_names, help_text, messages


class RaidOverview(commands.Cog):
    """
    Cog of raid manager that responsible for raid overviewing.
    """
    database = DatabaseManager()

    def __init__(self, bot: Bot):
        """
        :param bot: discord bot for executing the cog commands
        """
        self.bot = bot
        self.reporter = Reporter()

    @commands.command(name=command_names.function_command.show_raids, help=help_text.show_raids)
    async def show_raids(self, ctx: Context, show_all: str = ''):
        """
        Command to send information about guild active raid


        :param ctx: discord command context
        :param show_all: If not None show all active raids witch was created by the bot
        """
        await ctx.channel.send("Command not working")
        # if not show_all:
        #     # Check raids exist
        #     if not self.raid_list:
        #         await self.reporter.report_unsuccessful_command(ctx, CommandFailureReasons.NO_ACTIVE_RAIDS)
        #         return
        #
        #     available_raids = [some_raid for some_raid in self.raid_list if ctx.guild.id in some_raid.raid_coll_msgs]
        #     if not available_raids:
        #         await self.reporter.report_unsuccessful_command(ctx, CommandFailureReasons.NO_ACTIVE_RAIDS)
        #         return
        #
        #     # Generate information about active raids and send
        #     msg_of_raid = messages.active_raids_start
        #     for curr_raid in self.raid_list:
        #         if ctx.guild.id not in curr_raid.raid_coll_msgs:
        #             continue
        #         channel = self.bot.get_channel(curr_raid.raid_coll_msgs[ctx.guild.id].channel_id)
        #         msg_of_raid += messages.active_raid_all.format(
        #             channel_name=channel.mention, captain_name=curr_raid.captain.nickname,
        #             server=curr_raid.server, time_leaving=curr_raid.raid_time.time_leaving,
        #         ) + '\n'
        #     await ctx.send(msg_of_raid)
        #     await self.reporter.report_success_command(ctx)
        #
        # else:
        #     # Check raids exist
        #     if not self.raid_list:
        #         await self.reporter.report_unsuccessful_command(ctx, CommandFailureReasons.NO_ACTIVE_RAIDS)
        #         return
        #
        #     # Generate information about active raids and send
        #     msg_of_raid = messages.active_raids_start
        #     for curr_raid in self.raid_list:
        #         for raid_coll_msg in curr_raid.raid_coll_msgs.values():
        #             guild_name = str(self.bot.get_guild(raid_coll_msg.guild_id))
        #             channel_name = str(self.bot.get_channel(raid_coll_msg.channel_id))
        #             msg_of_raid += messages.active_raid_hide.format(
        #                 guild_name=guild_name, channel_name=channel_name,
        #                 captain_name=curr_raid.captain.nickname, time_leaving=curr_raid.raid_time.time_leaving,
        #             ) + '\n'
        #     await ctx.send(msg_of_raid)
        #     await self.reporter.report_success_command(ctx)

    @commands.command(name=command_names.function_command.show_text_raids, help=help_text.show_text_raids)
    @commands.guild_only()
    @commands.has_role('Капитан')
    async def show_text_raids(self, ctx: Context, captain_name: str, time_leaving: str = ''):
        """
        Command to send raids members nicknames as message

        :param ctx: discord command context
        :param captain_name: captain name of the raid to show
        :param time_leaving: time leaving of the raid to show
        """
        await check_input.validation(**locals())
        await ctx.channel.send("Command not working")
        # curr_raid = self.raid_list.find_raid(
        #     ctx.guild.id, ctx.channel.id, captain_name, time_leaving,
        #     ignore_channels=True
        # )
        #
        # if curr_raid:
        #     # If it's first display
        #     if not curr_raid.table:
        #         curr_raid.table_path()
        #
        #     # Generate text member list
        #     text = curr_raid.table.create_text_table()
        #     title = text.split('\n')[0]
        #     embed = discord.Embed(
        #         title=title,
        #         colour=discord.Colour.blue(),
        #         description=text[len(title) + 1:]
        #     )
        #
        #     await ctx.send(curr_raid.table.create_text_table())
        #     await self.reporter.report_success_command(ctx)
        # else:
        #     await self.reporter.report_unsuccessful_command(ctx, CommandFailureReasons.RAID_NOT_FOUND)

    @commands.command(name=command_names.function_command.show, help=help_text.show)
    @commands.guild_only()
    @commands.has_role('Капитан')
    async def show(self, ctx: Context, captain_name: str = '', time_leaving: str = ''):
        """
        Command to send raid members nicknames as image

        :param ctx: discord command context
        :param captain_name: captain name of the raid to show
        :param time_leaving: time leaving of the raid to show
        """
        await check_input.validation(**locals())
        await ctx.channel.send("Command not working")
        # # Get the name of the captain from db if not specified
        # if not captain_name:
        #     captain_document = await self.database.user.get_user_by_id(ctx.author.id)
        #     if captain_document:
        #         captain_name = captain_document.get('nickname')
        #     else:
        #         return
        #
        # curr_raid = self.raid_list.find_raid(
        #     ctx.guild.id, ctx.channel.id, captain_name, time_leaving,
        #     ignore_channels=True
        # )
        #
        # if curr_raid:
        #     path = curr_raid.table_path()
        #     curr_raid.save_raid()
        #     await ctx.send(file=discord.File(path))
        #
        #     await self.reporter.report_success_command(ctx)
        # else:
        #     await self.reporter.report_unsuccessful_command(ctx, CommandFailureReasons.RAID_NOT_FOUND)


def setup(bot: Bot):
    """
    Function to add raid overview cog to the given bot

    :param bot: discord bot to add the cog
    """
    bot.add_cog(RaidOverview(bot))
    log_template.cog_launched('RaidOverview')
