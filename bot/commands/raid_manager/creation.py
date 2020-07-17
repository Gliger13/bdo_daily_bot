import asyncio
import logging

from discord.ext import commands

from commands.raid_manager import raid_list
from instruments import check_input, raid, database_process, tools
from instruments.raid import Raid
from messages import command_names, help_text, messages, logger_msgs
from settings.logger import log_template

module_logger = logging.getLogger('my_bot')


class RaidCreation(commands.Cog):
    database = database_process.DatabaseManager()
    raid_list = raid_list.RaidList()

    def __init__(self, bot):
        self.bot = bot

    def captain_raids(self, captain_name: str) -> list or None:
        current_raids = []
        for some_raid in self.raid_list:
            if some_raid.captain_name == captain_name:
                current_raids.append(some_raid)
        return current_raids

    def captain_raids_str(self, captain_name: str) -> str or None:
        """
        Return str short raid description of captain
        """
        current_raids = self.captain_raids(captain_name)

        if current_raids:
            msg = messages.yours_current_raids_start
            for captain_raid in current_raids:
                guild_name = str(self.bot.get_guild(captain_raid.guild_id))
                channel_name = str(self.bot.get_channel(captain_raid.channel_id))
                msg += (
                    f"**{guild_name}**/**{channel_name}**/"
                    f"**{captain_raid.server}**/**{captain_raid.raid_time.time_leaving}**\n"
                )
            return msg
        else:
            return

    async def notify_about_leaving(self, current_raid: Raid):
        secs_sleep = current_raid.raid_time.secs_to_notify()
        if not secs_sleep:
            return
        current_raid.raid_time.is_notified = True
        sleep_task = asyncio.create_task(asyncio.sleep(secs_sleep))
        current_raid.raid_time.notification_task = sleep_task
        await sleep_task

        users_list = self.database.user.get_users_id(list(current_raid.member_dict.keys()))
        amount = 0
        for member in users_list:
            if member:
                user = self.bot.get_user(member.get('discord_id'))
                await user.send(messages.member_notification)
                amount += 1

        captain_id = self.database.user.user_post_by_name(current_raid.captain_name).get('discord_id')
        captain = self.bot.get_user(captain_id)
        await captain.send(messages.captain_notification)

        log_template.notify_success(current_raid.raid_time.time_leaving, amount + 1)

    @commands.command(name=command_names.function_command.remove_raid, help=help_text.remove_raid)
    @commands.has_role('Капитан')
    async def remove_raid(self, ctx: commands.context.Context, captain_name, time_leaving=''):
        # Checking correct inputs arguments
        await check_input.validation(**locals())

        curr_raid = self.raid_list.find_raid(ctx.guild.id, ctx.channel.id, captain_name, time_leaving)
        if curr_raid:
            curr_raid.end_work()
            self.raid_list.remove(curr_raid)

            await ctx.message.add_reaction('✔')
            log_template.command_success(ctx)
        else:
            await ctx.message.add_reaction('❌')
            log_template.command_fail(ctx, logger_msgs.raid_not_found)

    @commands.command(name=command_names.function_command.collection, help=help_text.collection)
    @commands.has_role('Капитан')
    async def collection(self, ctx: commands.context.Context, captain_name, time_leaving=''):
        # Checking correct inputs arguments
        await check_input.validation(**locals())

        curr_raid = self.raid_list.find_raid(
            ctx.guild.id, ctx.channel.id, captain_name, time_leaving, ignore_channels=True
        )

        if not curr_raid:
            await ctx.message.add_reaction('❌')
            log_template.command_fail(ctx, logger_msgs.raid_not_found)
            return

        if curr_raid.is_deleted_raid:
            return

        if curr_raid.waiting_collection_task:
            curr_raid.waiting_collection_task.cancel()

        # Send message about collection
        collection_msg = await curr_raid.raid_msgs.send_coll_msg(ctx)
        await collection_msg.add_reaction('❤')

        log_template.command_success(ctx)

        curr_raid.raid_time.validate_time()

        # Notify user if possible before leaving
        asyncio.ensure_future(self.notify_about_leaving(curr_raid))

        raid_time = curr_raid.raid_time.time_to_display.copy()
        for index, time_display in enumerate(raid_time):
            curr_raid.save_raid()

            # Update text msg of start collection Raid
            await curr_raid.raid_msgs.update_coll_msg(self.bot)

            # Wait next time to display raid table
            secs_left = curr_raid.raid_time.secs_left_to_display()
            curr_raid.coll_sleep_task = asyncio.create_task(asyncio.sleep(secs_left))
            await curr_raid.coll_sleep_task
            curr_raid.raid_time.time_passed()

            # Resend new message with raid table if not first time else just send table
            await curr_raid.raid_msgs.update_table_msg(self.bot, ctx)

        self.database.captain.update_captain(str(ctx.author), curr_raid)

        await ctx.send(messages.collection_end.format(server=curr_raid.server, captain_name=curr_raid.captain_name))
        await self.remove_raid(ctx, captain_name, time_leaving)

    def check_captain_registration(self, user, captain_name: str):
        nickname = self.database.user.find_user(str(user))
        if nickname == captain_name:
            return
        else:
            self.database.user.rereg_user(user.id, str(user), captain_name)

    async def check_raid_exists(self, ctx, captain_name, time_leaving=''):
        # Check captain exists
        captain_post = self.database.captain.find_captain_post(str(ctx.author))
        if not captain_post:
            self.database.captain.create_captain(str(ctx.author))

        # Check raid exists of this captain
        captain_raids = self.captain_raids(captain_name)
        if not captain_raids:
            return
        # If raid with this credentials absolutely matched
        for captain_raid in captain_raids:
            if captain_raid.raid_time.time_leaving == time_leaving:
                await ctx.author.send(messages.raid_exist_error)
                await ctx.message.add_reaction('❌')
                log_template.command_fail(ctx, logger_msgs.raid_exist)
                raise commands.errors.UserInputError('Такой рейд уже существует.')

        active_raids = self.captain_raids_str(captain_name)
        message = await ctx.author.send(messages.raid_exist_warning + active_raids)
        await message.add_reaction('✔')
        await message.add_reaction('❌')

        def check(reaction, user):
            return user.id == ctx.message.author.id and (str(reaction.emoji) == '✔' or str(reaction.emoji) == '❌')

        # Wait answer of user
        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=300.0, check=check)
        except asyncio.TimeoutError:
            log_template.command_fail(ctx, logger_msgs.user_not_response)
            raise commands.errors.UserInputError('Капитан не ответил на вопрос о создании рейда')
        else:
            emoji = str(reaction.emoji)
            log_template.user_answer(ctx, emoji)
            if emoji == '❌':
                raise commands.errors.UserInputError('Капитан отказался создавать новый рейд')

    @commands.command(name=command_names.function_command.captain, help=help_text.captain)
    @commands.has_role('Капитан')
    async def captain(self, ctx: commands.context.Context,
                      captain_name: str, server: str, time_leaving: str, time_reservation_open='', reservation_count=0):
        await check_input.validation(**locals())
        await self.check_raid_exists(ctx, captain_name, time_leaving)
        self.check_captain_registration(ctx.author, captain_name)

        if not time_reservation_open:
            time_reservation_open = tools.now_time_plus_minute()

        new_raid = raid.Raid(
            captain_name,
            server,
            time_leaving,
            time_reservation_open,
            ctx.guild.id,
            ctx.channel.id,
            reservation_count
        )
        self.raid_list.append(new_raid)

        await ctx.send(messages.raid_created.format(time_reservation_open=time_reservation_open))
        await ctx.message.add_reaction('✔')
        log_template.command_success(ctx)

        # Wait time reservation open
        time_left_sec = tools.get_sec_left(time_reservation_open)
        sleep_task = asyncio.create_task(asyncio.sleep(time_left_sec))
        new_raid.waiting_collection_task = sleep_task
        await sleep_task
        # Start raid collection
        collection_task = asyncio.create_task(self.collection(ctx, captain_name, time_leaving))
        new_raid.collection_task = sleep_task
        await collection_task

    @commands.command(name=command_names.function_command.cap, help=help_text.cap)
    @commands.has_role('Капитан')
    async def cap(self, ctx: commands.context.Context):
        NUMBER_REACTIONS = {
            '1️⃣': 1, '2️⃣': 2, '3️⃣': 3,
            1: '1️⃣', 2: '2️⃣', 3: '3️⃣'
        }

        user = str(ctx.author)
        captain_post = self.database.captain.find_captain_post(user)

        if not captain_post:
            await ctx.message.add_reaction('❌')
            await ctx.author.send(messages.new_captain)
            log_template.command_fail(ctx, logger_msgs.captain_not_exist)
            return
        last_raids = captain_post.get('last_raids')
        raids_msg = messages.raid_create_choice_start.format(captain_name=captain_post['captain_name'])

        for index, last_raid in enumerate(last_raids):
            raids_msg += messages.raid_create_choice_server_time.format(
                index=index + 1, server=last_raid['server'], time_leaving=last_raid['time_leaving']
            )
            if last_raid.get('time_reservation_open'):
                raids_msg += messages.raid_create_choice_res_open.format(
                    time_reservation_open=last_raid['time_reservation_open']
                )
            if last_raid.get('reservation_count') and not last_raid['reservation_count'] == 1:
                raids_msg += messages.raid_create_choice_count.format(reservtaion_count=last_raid['reservation_count'])
            raids_msg += '.\n'

        msg = await ctx.send(raids_msg)
        for number in range(len(last_raids)):
            await msg.add_reaction(NUMBER_REACTIONS[number + 1])

        def check(reaction, user):
            return (
                    user == ctx.message.author and
                    (
                            str(reaction.emoji) == '1️⃣' or str(reaction.emoji) == '2️⃣' or str(reaction.emoji) == '3️⃣'
                    )
            )

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=600.0, check=check)
        except asyncio.TimeoutError:
            log_template.command_fail(ctx, logger_msgs.user_not_response)
            await ctx.message.add_reaction('❌')
        else:
            emoji = str(reaction.emoji)
            log_template.user_answer(ctx, emoji)
            user_choice = NUMBER_REACTIONS[emoji]

            user_raid = last_raids[user_choice - 1]
            await self.check_raid_exists(ctx, captain_post.get('captain_name'), user_raid.get('time_leaving'))
            await self.captain(
                ctx,
                captain_post.get('captain_name'),
                user_raid.get('server'),
                user_raid.get('time_leaving'),
                user_raid.get('time_reservation_open'),
                user_raid.get('reservation_count'),
            )


def setup(bot):
    bot.add_cog(RaidCreation(bot))
    log_template.cog_launched('RaidCreation')
