import logging

from discord.ext import commands

from commands.raid_manager import common
from instruments import messages, help_messages, check_input, database_process
from settings import settings

module_logger = logging.getLogger('my_bot')


class RaidJoining(commands.Cog):
    database = database_process.DatabaseManager()
    raid_list = common.Raids.active_raids

    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def update_info(curr_raid):
        old_text = curr_raid.collection_msg.content
        edited_text = f"Мест осталось {curr_raid.places_left}.\n"
        start_index = old_text.find('Мест осталось')
        end_index = old_text.find('Обновлённая')
        new_text_msg = old_text[:start_index] + edited_text + old_text[end_index:]
        await curr_raid.collection_msg.edit(content=new_text_msg)

    async def raid_reaction_add(self, collection_msg, emoji, user):
        if str(emoji) == '❤' and not user.id == settings.BOT_ID:  # Ignore bot action
            for curr_raid in self.raid_list:
                if (curr_raid.collection_msg and curr_raid.collection_msg.id == collection_msg.id and
                        curr_raid.guild == collection_msg.guild):
                    nickname = self.database.user.find_user(str(user))
                    if nickname:  # if find user in data base
                        if curr_raid.member_dict.get(nickname):
                            await user.send(messages.msg_fail1)
                            module_logger.info(f'{user} не смог попасть в рейд к кэпу. Уже есть в рейде')
                            break
                        else:
                            if curr_raid.places_left != 0:
                                msg_success = (
                                    f"**Привет!**\n"
                                    f"Ты попал на морские ежедневки к капитану **{curr_raid.captain_name}**"
                                    f" на сервере **{curr_raid.server}**.\n"
                                    f"Отплытие с Ока Окиллы в **{curr_raid.raid_time.time_leaving}**.\n"
                                    f"Об сборе рейда обычно пишут за 5 - 10 минут "
                                    f"до отплытия. Если информации нету, то пиши на"
                                    f" фамилию капитана **{curr_raid.captain_name}**.")
                                curr_raid += str(nickname)
                                self.database.user.user_joined_raid(str(user))
                                module_logger.info(f'{user} попал в рейд к кэпу {curr_raid.captain_name}')
                                await user.send(msg_success)
                                await RaidJoining.update_info(curr_raid)
                                break
                            else:
                                msg_no_space = "Ты не попал в рейд. Мест не осталось :crying_cat_face:"
                                module_logger.info(f'{user} не попал в рейд к кэпу {curr_raid.captain_name}. Нет мест')
                                await user.send(msg_no_space)
                                break
                    else:
                        module_logger.info(f'{user} не попал в рейд. Нет регистрации')
                        await user.send(messages.msg_fail2)
                        break

    async def raid_reaction_remove(self, collection_msg, emoji, user):
        if str(emoji) == '❤':
            for curr_raid in self.raid_list:
                if (curr_raid.collection_msg and curr_raid.collection_msg.id == collection_msg.id
                        and curr_raid.guild == collection_msg.guild):
                    nickname = self.database.user.find_user(str(user))
                    if nickname:
                        if curr_raid.member_dict.get(nickname):
                            msg_remove = (
                                f"Я тебя удалил из списка на ежедневки с капитаном **{curr_raid.captain_name}**"
                            )
                            curr_raid -= str(nickname)
                            self.database.user.user_leave_raid(str(user))
                            module_logger.info(f'{user} убрал себя из рейда кэпа {curr_raid.captain_name}')
                            await user.send(msg_remove)
                            await RaidJoining.update_info(curr_raid)
                            break

    @commands.command(name='бронь', help=help_messages.reserve)
    @commands.has_role('Капитан')
    async def reserve(self, ctx: commands.context.Context, name: str, captain_name='', time_leaving=''):
        # Checking correct input
        await check_input.validation(**locals())

        curr_raid = common.find_raid(ctx.guild.id, ctx.channel.id, captain_name, time_leaving)
        if curr_raid and not curr_raid.places_left == 0:
            if curr_raid.member_dict.get(name):
                module_logger.info(f'{ctx.author} неудачно использовал команду {ctx.message.content}. Есть в рейде')
                await ctx.message.add_reaction('❌')
                return
            curr_raid += name
            module_logger.info(f'{ctx.author} успешно использовал команду {ctx.message.content}')
            await RaidJoining.update_info(curr_raid)
            await ctx.message.add_reaction('✔')
        else:
            guild_raid_list = []
            for curr_raid in self.raid_list:
                if curr_raid.guild == ctx.message.guild and not curr_raid.member_dict.get(name):
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

    @commands.command(name='удали_бронь', help=help_messages.remove_res)
    @commands.has_role('Капитан')
    async def remove_res(self, ctx: commands.context.Context, name: str):
        # Checking correct inputs arguments
        await check_input.validation(**locals())

        for finding_raid in self.raid_list:
            finding_raid -= name
            if finding_raid:
                module_logger.info(f'{ctx.author} успешно использовал команду {ctx.message.content}')
                await RaidJoining.update_info(finding_raid)
                await ctx.message.add_reaction('✔')
                break
        else:
            module_logger.info(f'{ctx.author} неудачно использовал команду {ctx.message.content}. Нету в рейдах')
            await ctx.message.add_reaction('❌')


def setup(bot):
    bot.add_cog(RaidJoining(bot))
    module_logger.debug(f'Успешный запуск bot.raid_manager.joining')
