import logging

from discord.ext import commands

from commands.raid_manager import raid_list
from instruments import check_input, database_process
from messages import command_names, help_text, messages, logger_msgs
from settings import settings
from settings.logger import log_template

module_logger = logging.getLogger('my_bot')


class RaidJoining(commands.Cog):
    database = database_process.DatabaseManager()
    raid_list = raid_list.RaidList()

    def __init__(self, bot):
        self.bot = bot

    async def raid_reaction_add(self, collection_msg, emoji, user):
        if str(emoji) != '❤' or user.id == settings.BOT_ID:
            return

        guild = collection_msg.guild
        channel = collection_msg.channel
        # Check registration
        nickname = self.database.user.find_user(str(user))
        if not nickname:
            await user.send(messages.no_registration)
            log_template.reaction(guild, channel, user, emoji, logger_msgs.no_registration)
            return

        current_raid = self.raid_list.find_raid_by_coll_id(collection_msg.id)

        # Check user exists in raid
        if nickname in current_raid:
            await user.send(messages.already_in_raid)
            log_template.reaction(guild, channel, user, emoji, logger_msgs.already_in_raid)
            return

        if current_raid.is_full:
            log_template.reaction(guild, channel, user, emoji, logger_msgs.raid_is_full)
            await user.send(messages.raid_not_joined)
            return

        if not self.raid_list.is_correct_join(nickname, current_raid.raid_time.time_leaving):
            log_template.reaction(guild, channel, user, emoji, logger_msgs.already_in_same_raid)
            await user.send(messages.already_joined)
            return

        msg_success = messages.raid_joined.format(
            captain_name=current_raid.captain_name, server=current_raid.server,
            time_leaving=current_raid.raid_time.time_leaving,
        )

        current_raid += nickname

        self.database.user.user_joined_raid(str(user))

        await user.send(msg_success)
        await current_raid.raid_msgs.update_coll_msg(self.bot)
        log_template.reaction(guild, channel, user, emoji,
                              logger_msgs.raid_joining.format(captain_name=current_raid.captain_name))

    async def raid_reaction_remove(self, collection_msg, emoji, user):
        if str(emoji) != '❤' or user.id == settings.BOT_ID:
            return

        current_raid = self.raid_list.find_raid_by_coll_id(collection_msg.id)

        nickname = self.database.user.find_user(str(user))
        if not nickname or nickname not in current_raid:
            return

        current_raid -= nickname
        self.database.user.user_leave_raid(str(user))

        await user.send(messages.raid_leave.format(captain_name=current_raid.captain_name))
        await current_raid.raid_msgs.update_coll_msg(self.bot)
        guild = collection_msg.guild
        channel = collection_msg.channel
        log_template.reaction(guild, channel, user, emoji,
                              logger_msgs.raid_leaving.format(captain_name=current_raid.captain_name))

    @commands.command(name=command_names.function_command.reserve, help=help_text.reserve)
    @commands.has_role('Капитан')
    async def reserve(self, ctx: commands.context.Context, name: str, captain_name='', time_leaving=''):
        # Checking correct input
        await check_input.validation(**locals())

        if not captain_name and not time_leaving:
            available_raids = self.raid_list.find_raids_by_guild(name, ctx.guild.id)

            if not available_raids:
                log_template.command_fail(ctx, logger_msgs.no_available_raids)
                await ctx.message.add_reaction('❌')
                return

            smaller_raid = min(available_raids)
            smaller_raid += name
            await smaller_raid.raid_msgs.update_coll_msg(self.bot)
            await ctx.message.add_reaction('✔')
            log_template.command_success(ctx)
            return

        curr_raid = self.raid_list.find_raid(ctx.guild.id, ctx.channel.id, captain_name, time_leaving)

        if not curr_raid:
            await ctx.message.add_reaction('❌')
            log_template.command_fail(ctx, logger_msgs.raid_not_found)
            return
        if curr_raid.is_full:
            await ctx.message.add_reaction('❌')
            log_template.command_fail(ctx, logger_msgs.raid_is_full)
            return
        if name in curr_raid:
            await ctx.message.add_reaction('❌')
            log_template.command_fail(ctx, logger_msgs.already_in_raid)
            return
        if self.raid_list.is_correct_join(name, time_leaving):
            await ctx.author.send(messages.already_joined)
            await ctx.message.add_reaction('❌')
            log_template.command_fail(ctx, logger_msgs.already_in_same_raid)
            return

        curr_raid += name
        await curr_raid.raid_msgs.update_coll_msg(self.bot)
        await ctx.message.add_reaction('✔')
        log_template.command_success(ctx)

    @commands.command(name=command_names.function_command.remove_res, help=help_text.remove_res)
    @commands.has_role('Капитан')
    async def remove_res(self, ctx: commands.context.Context, name: str):
        # Checking correct inputs arguments
        await check_input.validation(**locals())

        current_raid = self.raid_list.find_raid_by_nickname(name)

        if not current_raid:
            await ctx.message.add_reaction('❌')
            log_template.command_fail(ctx, logger_msgs.nope_in_raids)
        else:
            current_raid -= name
            await current_raid.raid_msgs.update_coll_msg(self.bot)
            await ctx.message.add_reaction('✔')
            log_template.command_success(ctx)


def setup(bot):
    bot.add_cog(RaidJoining(bot))
    log_template.cog_launched('RaidJoining')
