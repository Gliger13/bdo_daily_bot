import logging

import discord
from discord.ext import commands

from commands.raid_manager import raid_list
from instruments import check_input, database_process
from messages import command_names, help_text, messages, logger_msgs
from settings.logger import log_template

module_logger = logging.getLogger('my_bot')


class RaidOverview(commands.Cog):
    database = database_process.DatabaseManager()
    raid_list = raid_list.RaidList()

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name=command_names.function_command.show_raids, help=help_text.show_raids)
    async def show_raids(self, ctx: commands.context.Context, show_all=''):
        log_template.command_success(ctx)
        if not show_all:
            if self.raid_list:
                msg_of_raid = messages.active_raids_start
                for curr_raid in self.raid_list:
                    if ctx.guild.id == curr_raid.guild_id:
                        channel_name = str(self.bot.get_channel(curr_raid.channel_id))
                        msg_of_raid += messages.active_raid_all.format(
                            channel_name=channel_name, captain_name=curr_raid.captain_name,
                            server=curr_raid.server, time_leaving=curr_raid.raid_time.time_leaving,
                        )
                    await ctx.send(msg_of_raid)
            else:
                await ctx.send(messages.no_active_raids)
        elif show_all:
            if self.raid_list:
                msg_of_raid = messages.active_raids_start
                for curr_raid in self.raid_list:
                    guild_name = str(self.bot.get_guild(curr_raid.guild_id))
                    channel_name = str(self.bot.get_channel(curr_raid.channel_id))
                    msg_of_raid += messages.active_raid_hide.format(
                        guild_name=guild_name, channel_name=channel_name,
                        captain_name=curr_raid.captain_name, time_leaving=curr_raid.raid_time.time_leaving,
                    )
                await ctx.send(msg_of_raid)
            else:
                await ctx.send(messages.no_active_raids)

    @commands.command(name=command_names.function_command.show_text_raids, help=help_text.show_text_raids)
    @commands.has_role('Капитан')
    async def show_text_raids(self, ctx: commands.context.Context, captain_name, time_leaving=''):
        # Checking correct inputs arguments
        await check_input.validation(**locals())

        curr_raid = self.raid_list.find_raid(
            ctx.guild.id, ctx.channel.id, captain_name, time_leaving,
            ignore_channels=True
        )
        if curr_raid:
            if not curr_raid.table:
                curr_raid.table_path()
            text = curr_raid.table.create_text_table()
            title = text.split('\n')[0]
            embed = discord.Embed(
                title=title,
                colour=discord.Colour.blue(),
                description=text[len(title) + 1:]
            )
            await ctx.send(curr_raid.table.create_text_table())
            await ctx.message.add_reaction('✔')
            log_template.command_success(ctx)
        else:
            await ctx.message.add_reaction('❌')
            log_template.command_fail(ctx, logger_msgs.raid_not_found)

    @commands.command(name=command_names.function_command.show, help=help_text.show)
    @commands.has_role('Капитан')
    async def show(self, ctx: commands.context.Context, captain_name, time_leaving=''):
        # Checking correct inputs arguments
        await check_input.validation(**locals())
        curr_raid = self.raid_list.find_raid(
            ctx.guild.id, ctx.channel.id, captain_name, time_leaving,
            ignore_channels=True
        )
        if curr_raid:
            path = curr_raid.table_path()
            curr_raid.save_raid()
            await ctx.send(file=discord.File(path))
            await ctx.message.add_reaction('✔')
            log_template.command_success(ctx)
        else:
            await ctx.message.add_reaction('❌')
            log_template.command_fail(ctx, logger_msgs.raid_not_found)


def setup(bot):
    bot.add_cog(RaidOverview(bot))
    log_template.cog_launched('RaidOverview')
