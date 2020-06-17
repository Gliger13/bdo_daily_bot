import asyncio
import logging
import time

import discord
from discord.ext import commands

from commands.raid_manager import common
from instruments import tools as instr, raid, messages, check_input, database_process
from settings import settings

module_logger = logging.getLogger('my_bot')


class RaidManager(commands.Cog):
    database = database_process.Database()
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

    async def raid_reaction_add(self, reaction, user):
        collection_msg = reaction.message
        if reaction.emoji == '❤' and not user.id == settings.BOT_ID:  # Ignore bot action
            for curr_raid in self.raid_list:
                if (curr_raid.collection_msg and curr_raid.collection_msg.id == collection_msg.id and
                        curr_raid.guild == collection_msg.guild):
                    nickname = self.database.find_user(str(user))
                    if nickname:  # if find user in data base
                        if curr_raid.member_dict.get(nickname):
                            await user.send(messages.msg_fail1)
                            module_logger.info(f'{user} не смог попасть в рейд к кэпу. Уже есть в рейде')
                            break
                        else:
                            if curr_raid.places_left != 0:
                                msg_success = (
                                    f"**Привет!**\nТы попал на морские ежедневки к капитану **{curr_raid.captain_name}**"
                                    f" на сервере **{curr_raid.server}**.\nОтплытие с Ока Окиллы"
                                    f" в **{curr_raid.time_leaving}**.\nОб сборе рейда обычно пишут за 5 - 10 минут "
                                    f"до отплытия. Если информации нету, то пиши на"
                                    f" фамилию капитана **{curr_raid.captain_name}**.")
                                curr_raid += str(nickname)
                                self.database.user_joined_raid(str(user))
                                module_logger.info(f'{user} попал в рейд к кэпу {curr_raid.captain_name}')
                                await user.send(msg_success)
                                await RaidManager.update_info(curr_raid)
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

    async def raid_reaction_remove(self, reaction, user):
        collection_msg = reaction.message
        if reaction.emoji == '❤':
            for curr_raid in self.raid_list:
                if (curr_raid.collection_msg and curr_raid.collection_msg.id == collection_msg.id
                        and curr_raid.guild == collection_msg.guild):
                    nickname = self.database.find_user(str(user))
                    if nickname:
                        if curr_raid.member_dict.get(nickname):
                            msg_remove = f"Я тебя удалил из списка на ежедневки с капитаном **{curr_raid.captain_name}**"
                            curr_raid -= str(nickname)
                            self.database.user_leave_raid(str(user))
                            module_logger.info(f'{user} убрал себя из рейда кэпа {curr_raid.captain_name}')
                            await user.send(msg_remove)
                            await RaidManager.update_info(curr_raid)
                            break

    @commands.command(name='бронь', help=messages.help_msg_reserve)
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
            await RaidManager.update_info(curr_raid)
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

    @commands.command(name='удали_бронь', help=messages.help_msg_remove_res)
    @commands.has_role('Капитан')
    async def remove_res(self, ctx: commands.context.Context, name: str):
        # Checking correct inputs arguments
        await check_input.validation(**locals())

        for finding_raid in self.raid_list:
            finding_raid -= name
            if finding_raid:
                module_logger.info(f'{ctx.author} успешно использовал команду {ctx.message.content}')
                await RaidManager.update_info(finding_raid)
                await ctx.message.add_reaction('✔')
                break
        else:
            module_logger.info(f'{ctx.author} неудачно использовал команду {ctx.message.content}. Нету в рейдах')
            await ctx.message.add_reaction('❌')

    @commands.command(name='покажи_рейды', help=messages.help_msg_show_raids)
    async def show_raids(self, ctx: commands.context.Context):
        module_logger.info(f'{ctx.author} использовал команду {ctx.message.content}')
        if self.raid_list:
            msg_of_raid = "В данный момент собирают рейды:\n"
            for curr_raid in self.raid_list:
                msg_of_raid += (f" - Капитан **{curr_raid.captain_name}** на канале **{curr_raid.server}**"
                                f" выплывает в **{curr_raid.time_leaving}**.\n")
            await ctx.send(msg_of_raid)
        else:
            msg_no_raids = "В данный момент никто не собирает рейд, или собирают, но не через меня :cry:"
            await ctx.send(msg_no_raids)

    @commands.command(name='покажи_состав', help=messages.help_msg_load_raid)
    @commands.has_role('Капитан')
    async def show_text_raids(self, ctx: commands.context.Context, captain_name, time_leaving=''):
        # Checking correct inputs arguments
        await check_input.validation(**locals())

        curr_raid = common.find_raid(ctx.guild.id, ctx.channel.id, captain_name, time_leaving, ignore_channels=True)
        if curr_raid:
            await ctx.send(curr_raid.table.create_text_table())
            await ctx.message.add_reaction('✔')
            module_logger.info(f'{ctx.author} успешно использовал команду {ctx.message.content}')
        else:
            await ctx.message.add_reaction('❌')
            module_logger.info(f'{ctx.author} неудачно использовал команду {ctx.message.content}')

    @commands.command(name='покажи', help=messages.help_msg_show)
    @commands.has_role('Капитан')
    async def show(self, ctx: commands.context.Context, captain_name, time_leaving=''):
        # Checking correct inputs arguments
        await check_input.validation(**locals())
        curr_raid = common.find_raid(ctx.guild.id, ctx.channel.id, captain_name, time_leaving, ignore_channels=True)
        if curr_raid:
            path = curr_raid.table_path()
            curr_raid.save_raid()
            await ctx.send(file=discord.File(path))
            await ctx.message.add_reaction('✔')
            module_logger.info(f'{ctx.author} успешно использовал команду {ctx.message.content}')
        else:
            await ctx.message.add_reaction('❌')
            module_logger.info(f'{ctx.author} неудачно использовал команду {ctx.message.content}')

    @commands.command(name='удали_рейд', help=messages.help_msg_remove_raid)
    @commands.has_role('Капитан')
    async def remove_raid(self, ctx: commands.context.Context, captain_name, time_leaving=''):
        # Checking correct inputs arguments
        await check_input.validation(**locals())

        curr_raid = common.find_raid(ctx.guild.id, ctx.channel.id, captain_name, time_leaving)
        if curr_raid:
            curr_raid.is_delete_raid = True
            for task in curr_raid.task_list:
                task.cancel()
            self.raid_list.remove(curr_raid)
            module_logger.info(f'{ctx.author} успешно использовал команду {ctx.message.content}')
            await ctx.message.add_reaction('✔')
        else:
            module_logger.info(f'{ctx.author} неудачно использовал команду {ctx.message.content}')
            await ctx.message.add_reaction('❌')

    @commands.command(name='сбор', help=messages.help_msg_collection)
    @commands.has_role('Капитан')
    async def collection(self, ctx: commands.context.Context, captain_name, time_leaving=''):
        # Checking correct inputs arguments
        await check_input.validation(**locals())

        curr_raid = common.find_raid(ctx.guild.id, ctx.channel.id, captain_name, time_leaving, ignore_channels=True)
        if curr_raid:
            collection_msg = (f"Капитан **{curr_raid.captain_name}** выплывает на морские ежедневки с Око Окиллы в "
                              f"**{curr_raid.time_leaving}** на канале **{curr_raid.server}**.\n"
                              f"Желающие присоединиться к кэпу должны нажать на :heart:.\n"
                              f"И обязательно, посмотрите сообщение,"
                              f"которое я вам выслал в личные сообщения, может быть вы не попали в рейд.\n"
                              f"Мест осталось {curr_raid.places_left}.\n"
                              f"Обновлённая таблица появится скоро")
            curr_raid.guild = ctx.message.guild
            curr_raid.collection_msg = await ctx.send(collection_msg)
            await curr_raid.collection_msg.add_reaction('❤')
            # Show raid_table in time
            curr_raid.table_msg = await ctx.send('Тут будет таблица')
            if not curr_raid.time_to_display:
                curr_raid.time_left_to_display()
            else:
                curr_raid.make_valid_time()
                for tasks in curr_raid.task_list:
                    tasks.cancel()
            for index, (sec_left, time_display) in enumerate(curr_raid.time_to_display):
                if not sec_left and not time_display:
                    continue
                # Update text msg of start collection Raid
                edited_text = f'Обновлённая таблица появится в {time_display}.'
                old_text = curr_raid.collection_msg.content
                start_index = old_text.find('Обновлённая')
                new_text = old_text[:start_index] + edited_text
                await curr_raid.collection_msg.edit(content=new_text)

                curr_raid.save_raid()
                module_logger.info(f'Сохранение рейда {curr_raid.captain_name}')
                sleep_task = asyncio.create_task(asyncio.sleep(sec_left))
                curr_raid.task_list.append(sleep_task)
                await sleep_task
                for tasks in curr_raid.task_list:
                    tasks.cancel()
                await curr_raid.table_msg.delete()
                curr_raid.table_msg = await ctx.send(file=discord.File(curr_raid.table_path()))
                curr_raid.time_to_display[index] = ('', '')
            await ctx.send(f"Рейд на {curr_raid.server} с капитаном {curr_raid.captain_name} уже уплыли на ежедневки")
            await self.remove_raid(ctx, captain_name, time_leaving)
        else:
            await ctx.message.add_reaction('❌')

    @commands.command(name='капитан', help=messages.help_msg_captain)
    @commands.has_role('Капитан')
    async def captain(self, ctx: commands.context.Context, captain_name: str, server: str, time_leaving: str, time_reservation_open='',
                      reservation_count=0):
        # Checking correct inputs arguments
        await check_input.validation(**locals())

        if not time_reservation_open:
            current_hour, current_minute = map(int, time.ctime()[11:16].split(':'))
            if current_minute + 1 < 60:
                current_minute += 1
            else:
                current_minute -= 59
                current_hour += 1 if current_hour < 24 else -23
            time_reservation_open = ':'.join((str(current_hour), str(current_minute)))
        new_raid = raid.Raid(ctx, captain_name, server, time_leaving, time_reservation_open, reservation_count)
        self.raid_list.append(new_raid)
        new_raid.guild = ctx.guild

        time_left_sec = instr.get_sec_left(time_reservation_open)
        hour, minutes = time_reservation_open.split(':')
        time_open = f"{hour}:{minutes}" if len(minutes) == 2 else f"{hour}:0{minutes}"
        await ctx.send(f"Новый рейд создан! Теперь участники могут записатся к тебе!\n"
                       f"Бронирование мест начнется в **{time_open}**")
        await ctx.message.add_reaction('✔')
        module_logger.info(f'{ctx.author} удачно использовал команду {ctx.message.content}')
        await asyncio.sleep(time_left_sec)
        await self.collection(ctx, captain_name, time_leaving)


def setup(bot):
    bot.add_cog(RaidManager(bot))
    module_logger.debug(f'Успешный запуск bot.raid_manager.manager')
