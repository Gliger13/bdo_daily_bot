import logging

from discord.ext import commands

from commands.raid_manager import raid_list
from instruments import check_input, database_process
from messages import command_names, help_text, messages
from settings import settings

module_logger = logging.getLogger('my_bot')


class RaidJoining(commands.Cog):
    database = database_process.DatabaseManager()
    raid_list = raid_list.RaidList()

    def __init__(self, bot):
        self.bot = bot

    async def raid_reaction_add(self, collection_msg, emoji, user):
        if str(emoji) != '❤' or user.id == settings.BOT_ID:
            return

        # Check registration
        nickname = self.database.user.find_user(str(user))
        if not nickname:
            module_logger.info(f'{user} не попал в рейд. Нет регистрации')
            await user.send(messages.no_registration)
            return

        current_raid = self.raid_list.find_raid_by_coll_id(collection_msg.id)

        # Check user exists in raid
        if nickname in current_raid:
            await user.send(messages.already_in_raid)
            module_logger.info(f'{user} не смог попасть в рейд к кэпу. Уже есть в рейде')
            return

        if current_raid.is_full:
            module_logger.info(f'{user} не попал в рейд к кэпу {current_raid.captain_name}. Нет мест')
            await user.send(messages.raid_not_joined)
            return

        msg_success = messages.raid_joined.format(
            captain_name=current_raid.captain_name, server=current_raid.server,
            time_leaving=current_raid.raid_time.time_leaving,
        )

        current_raid += nickname

        self.database.user.user_joined_raid(str(user))

        module_logger.info(f'{user} попал в рейд к кэпу {current_raid.captain_name}')
        await user.send(msg_success)
        await current_raid.raid_msgs.update_coll_msg(self.bot)

    async def raid_reaction_remove(self, collection_msg, emoji, user):
        if str(emoji) != '❤' or user.id == settings.BOT_ID:
            return

        current_raid = self.raid_list.find_raid_by_coll_id(collection_msg.id)

        nickname = self.database.user.find_user(str(user))
        if not nickname or nickname not in current_raid:
            return

        current_raid -= nickname
        self.database.user.user_leave_raid(str(user))
        module_logger.info(f'{user} убрал себя из рейда кэпа {current_raid.captain_name}')
        await user.send(messages.raid_leave.format(captain_name=current_raid.captain_name))
        await current_raid.raid_msgs.update_coll_msg(self.bot)

    @commands.command(name=command_names.function_command.reserve, help=help_text.reserve)
    @commands.has_role('Капитан')
    async def reserve(self, ctx: commands.context.Context, name: str, captain_name='', time_leaving=''):
        # Checking correct input
        await check_input.validation(**locals())

        curr_raid = self.raid_list.find_raid(ctx.guild.id, ctx.channel.id, captain_name, time_leaving)
        if curr_raid and not curr_raid.places_left == 0:
            if curr_raid.member_dict.get(name):
                module_logger.info(f'{ctx.author} неудачно использовал команду {ctx.message.content}. Есть в рейде')
                await ctx.message.add_reaction('❌')
                return
            curr_raid += name
            module_logger.info(f'{ctx.author} успешно использовал команду {ctx.message.content}')
            await curr_raid.raid_msgs.update_coll_msg(self.bot)
            await ctx.message.add_reaction('✔')
        else:
            guild_raid_list = []
            for curr_raid in self.raid_list:
                if curr_raid.guild_id == ctx.message.guild.id and not curr_raid.member_dict.get(name):
                    guild_raid_list.append(curr_raid)
                    break
            if not guild_raid_list:  # If list empty
                module_logger.info(f'{ctx.author} неудачно использовал команду {ctx.message.content}. Нет рейдов')
                await ctx.message.add_reaction('❌')
                return
            smaller_raid = min(guild_raid_list)
            smaller_raid += name
            module_logger.info(f'{ctx.author} успешно использовал команду {ctx.message.content}')
            await ctx.message.add_reaction('✔')

    @commands.command(name=command_names.function_command.remove_res, help=help_text.remove_res)
    @commands.has_role('Капитан')
    async def remove_res(self, ctx: commands.context.Context, name: str):
        # Checking correct inputs arguments
        await check_input.validation(**locals())

        for finding_raid in self.raid_list:
            finding_raid -= name
            if finding_raid:
                module_logger.info(f'{ctx.author} успешно использовал команду {ctx.message.content}')
                await finding_raid.raid_msgs.update_coll_msg(self.bot)
                await ctx.message.add_reaction('✔')
                break
        else:
            module_logger.info(f'{ctx.author} неудачно использовал команду {ctx.message.content}. Нету в рейдах')
            await ctx.message.add_reaction('❌')


def setup(bot):
    bot.add_cog(RaidJoining(bot))
    module_logger.debug(f'Успешный запуск bot.raid_manager.joining')
