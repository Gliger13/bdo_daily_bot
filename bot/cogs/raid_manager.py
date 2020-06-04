import asyncio
import json
import logging
import os
import time
import random
from cogs import fun

import discord
from discord.ext import commands
from pymongo import MongoClient

from instruments import tools as instr, raid, messages, check_input
from settings import settings

module_logger = logging.getLogger('my_bot')


class ManageRaid(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.raid_list = list()  # contains current raids
        self.msg_pvp_id = None

    # Initialization MongoDB
    module_logger.debug('Запуск базы данных')
    cluster = MongoClient(settings.string_DB)
    db = cluster['discord']
    coll_mem_surname = db["user_nicknames"]
    module_logger.debug('База данных успешно загружена')

    @staticmethod
    async def update_info(curr_raid):
        old_text = curr_raid.collection_msg.content
        edited_text = f"Мест осталось {curr_raid.places_left}.\n"
        start_index = old_text.find('Мест осталось')
        end_index = old_text.find('Обновлённая')
        new_text_msg = old_text[:start_index] + edited_text + old_text[end_index:]
        await curr_raid.collection_msg.edit(content=new_text_msg)

    def find_raid(self, captain_name: str, time_leaving: str) -> raid.Raid:
        if not captain_name:
            return
        captain_list = [some_raid.captain_name for some_raid in self.raid_list]
        is_unique_captains = True if len(captain_list) == len(set(captain_list)) else False
        if self.raid_list and is_unique_captains or self.raid_list and time_leaving:
            for finding_raid in self.raid_list:
                if (finding_raid.captain_name == captain_name and finding_raid.time_leaving == time_leaving
                        or finding_raid.captain_name == captain_name):
                    return finding_raid
        else:
            return

    @commands.command(name='pvp')
    @commands.has_role('Капитан')
    async def pvp(self, ctx):
        msg_pvp = await ctx.send('Если хочешь для себя открыть PVP контент, то нажми на ⚔️️')
        await msg_pvp.add_reaction('⚔️')
        self.msg_pvp_id = msg_pvp.id

    async def set_pvp_role(self, reaction, user):
        if reaction.message.id == self.msg_pvp_id:
            role = discord.utils.get(user.guild.roles, name="PVP")
            await user.add_roles(role)

    async def remove_pvp_role(self, reaction, user):
        if reaction.message.id == self.msg_pvp_id:
            role = discord.utils.get(user.guild.roles, name="PVP")
            await user.remove_roles(role)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        collection_msg = reaction.message
        if reaction.emoji == '⚔️' and not user.id == settings.bot_id:
            await self.set_pvp_role(reaction, user)
        if reaction.emoji == '❤' and not user.id == settings.bot_id:  # Ignore bot action
            for curr_raid in self.raid_list:
                if (curr_raid.collection_msg and curr_raid.collection_msg.id == collection_msg.id and
                        curr_raid.guild == collection_msg.guild):
                    post = ManageRaid.coll_mem_surname.find_one({"discord_user": str(user)})
                    if post:  # if find user in data base
                        nickname = post["nickname"]
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
                                ManageRaid.coll_mem_surname.find_one_and_update(
                                    {'discord_user': str(user)},
                                    {'$inc': {'entries': 1}}
                                )
                                module_logger.info(f'{user} попал в рейд к кэпу {curr_raid.captain_name}')
                                await user.send(msg_success)
                                await ManageRaid.update_info(curr_raid)
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

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        collection_msg = reaction.message
        if reaction.emoji == '⚔️' and not user.id == settings.bot_id:
            await self.remove_pvp_role(reaction, user)
        if reaction.emoji == '❤':
            for curr_raid in self.raid_list:
                if (curr_raid.collection_msg and curr_raid.collection_msg.id == collection_msg.id
                        and curr_raid.guild == collection_msg.guild):
                    finding_post = ManageRaid.coll_mem_surname.find_one({"discord_user": str(user)})
                    if finding_post:
                        nickname = finding_post["nickname"]
                        if curr_raid.member_dict.get(nickname):
                            msg_remove = f"Я тебя удалил из списка на ежедневки с капитаном **{curr_raid.captain_name}**"
                            curr_raid -= str(nickname)
                            ManageRaid.coll_mem_surname.find_one_and_update(
                                {'discord_user': str(user)},
                                {'$inc': {'entries': -1}}
                            )
                            module_logger.info(f'{user} убрал себя из рейда кэпа {curr_raid.captain_name}')
                            await user.send(msg_remove)
                            await ManageRaid.update_info(curr_raid)
                            break

    @commands.command(name='загрузи_рейд', help=messages.help_msg_load_raid)
    @commands.has_role('Капитан')
    async def load_raid(self, ctx, captain_name, time_leaving):
        # Checking correct input
        if (not await check_input.is_corr_name(ctx, captain_name) or
                not await check_input.is_corr_time(ctx, time_leaving)):
            return
        # Checking save file exists
        file_name = f"saves/{captain_name}_{'-'.join(time_leaving.split(':'))}.json"
        if not os.path.exists(file_name):
            await check_input.not_correct(ctx, 'Файл сохранения не найден')
            return

        # Open file and load information in new Raid
        with open(file_name, 'r', encoding='utf-8') as save_file:
            raid_information = json.load(save_file)
        old_raid = raid.Raid(
            raid_information['captain_name'],
            raid_information['server'],
            raid_information['time_leaving'],
            raid_information['time_reservation_open'],
            int(raid_information['reservation_count'])
        )
        old_raid.time_to_display = raid_information['time_to_display']
        old_raid.member_dict.update(raid_information['members_dict'])
        old_raid.members_count = raid_information['members_count']
        self.raid_list.append(old_raid)
        module_logger.info(f'{ctx.author} успешно использовал команду {ctx.message.content}')
        await ctx.message.add_reaction('✔')

    @commands.command(name='рег', help=messages.help_msg_reg)
    async def reg(self, ctx, name: str):
        # Checking correct input
        if not await check_input.is_corr_name(ctx, name):
            return
        # Try to find user in BD
        old_post = ManageRaid.coll_mem_surname.find_one({"discord_user": str(ctx.author)})
        if not old_post:  # If not find...
            post = {'discord_user': str(ctx.author), 'nickname': str(name), 'entries': 0}
            ManageRaid.coll_mem_surname.insert_one(post)
            module_logger.info(f'{ctx.author} успешно использовал команду {ctx.message.content}')
            await ctx.message.add_reaction('✔')
        else:
            module_logger.info(f'{ctx.author} неудачно использовал команду {ctx.message.content}. Уже есть в БД')
            await ctx.author.send("Ты уже зарегистрировался, хватит использовать эту команду."
                                  " Сейчас тапком в тебя кину! :sandal:. Иди и нажми на милое сердечко :heart:!")
            await ctx.message.add_reaction('❌')

    @commands.command(name='перерег', help=messages.help_msg_rereg)
    async def rereg(self, ctx, name: str):
        # Checking correct input
        if not await check_input.is_corr_name(ctx, name):
            return
        # Try to find user in BD
        old_post = ManageRaid.coll_mem_surname.find_one({"discord_user": str(ctx.author)})
        if old_post:  # If not find...
            post = {'discord_user': str(ctx.author), 'nickname': str(name), 'entries': int(old_post['entries'])}
            ManageRaid.coll_mem_surname.update(old_post, post)
            module_logger.info(f'{ctx.author} успешно использовал команду {ctx.message.content}')
            await ctx.message.add_reaction('✔')
        else:
            await self.reg(ctx, name)

    @commands.command(name='сохрани_рейды', help='сохраняет все рейды')
    async def save_raids(self, ctx):
        if self.raid_list:
            for some_raid in self.raid_list:
                some_raid.save_raid()
            module_logger.info(f'{ctx.author} успешно использовал команду {ctx.message.content}')
            await ctx.message.add_reaction('✔')
        else:
            module_logger.info(f'{ctx.author} неудачно использовал команду {ctx.message.content}. Не рейдов')
            await ctx.message.add_reaction('❌')

    @commands.command(name='сохрани_рейд', help='сохраняет рейд')
    async def save_raid(self, ctx, captain_name: str, time_leaving=''):
        # Checking correct input
        if (not await check_input.is_corr_name(ctx, captain_name) or
                time_leaving and not await check_input.is_corr_time(ctx, time_leaving)):
            return

        curr_raid = self.find_raid(captain_name, time_leaving)
        # if not find raid to save
        if not curr_raid:
            await check_input.not_correct(ctx, 'Не нашёл рейд для сохранение.')
            return

        curr_raid.save_raid()
        module_logger.info(f'{ctx.author} успешно использовал команду {ctx.message.content}')
        await ctx.message.add_reaction('✔')

    @commands.command(name='бронь', help=messages.help_msg_reserve)
    @commands.has_role('Капитан')
    async def reserve(self, ctx, name: str, captain_name='', time_leaving=''):
        # Checking correct input
        if (not await check_input.is_corr_name(ctx, name) or
                captain_name and not await check_input.is_corr_name(ctx, name) or
                time_leaving and not await check_input.is_corr_time(ctx, time_leaving)):
            return

        curr_raid = self.find_raid(captain_name, time_leaving)
        if curr_raid and not curr_raid.places_left == 0:
            if curr_raid.member_dict.get(name):
                module_logger.info(f'{ctx.author} неудачно использовал команду {ctx.message.content}. Есть в рейде')
                await ctx.message.add_reaction('❌')
                return
            curr_raid += name
            module_logger.info(f'{ctx.author} успешно использовал команду {ctx.message.content}')
            await ManageRaid.update_info(curr_raid)
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
    async def remove_res(self, ctx, name: str):
        # Checking correct inputs arguments
        if not await check_input.is_corr_name(ctx, name):
            return

        for finding_raid in self.raid_list:
            finding_raid -= name
            if finding_raid:
                module_logger.info(f'{ctx.author} успешно использовал команду {ctx.message.content}')
                await ManageRaid.update_info(finding_raid)
                await ctx.message.add_reaction('✔')
                break
        else:
            module_logger.info(f'{ctx.author} неудачно использовал команду {ctx.message.content}. Нету в рейдах')
            await ctx.message.add_reaction('❌')

    @commands.command(name='покажи_рейды', help=messages.help_msg_show_raids)
    async def show_raids(self, ctx):
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
    async def show_text_raids(self, ctx, captain_name, time_leaving=''):
        # Checking correct inputs arguments
        if (not await check_input.is_corr_name(ctx, captain_name) or
                time_leaving and not await check_input.is_corr_time(ctx, time_leaving)):
            return

        curr_raid = self.find_raid(captain_name, time_leaving)
        if curr_raid:
            await ctx.send(curr_raid.create_text_table())
            await ctx.message.add_reaction('✔')
            module_logger.info(f'{ctx.author} успешно использовал команду {ctx.message.content}')
        else:
            await ctx.message.add_reaction('❌')
            module_logger.info(f'{ctx.author} неудачно использовал команду {ctx.message.content}')


    @commands.command(name='покажи', help=messages.help_msg_show)
    @commands.has_role('Капитан')
    async def show(self, ctx, captain_name, time_leaving=''):
        # Checking correct inputs arguments
        if (not await check_input.is_corr_name(ctx, captain_name) or
                time_leaving and not await check_input.is_corr_time(ctx, time_leaving)):
            return

        curr_raid = self.find_raid(captain_name, time_leaving)
        if curr_raid:
            link = curr_raid.create_table()
            curr_raid.save_raid()
            await ctx.send(file=discord.File(link))
            await ctx.message.add_reaction('✔')
            module_logger.info(f'{ctx.author} успешно использовал команду {ctx.message.content}')
        else:
            await ctx.message.add_reaction('❌')
            module_logger.info(f'{ctx.author} неудачно использовал команду {ctx.message.content}')

    @commands.command(name='удали_рейд', help=messages.help_msg_remove_raid)
    @commands.has_role('Капитан')
    async def remove_raid(self, ctx, captain_name, time_leaving=''):
        # Checking correct inputs arguments
        if (not await check_input.is_corr_name(ctx, captain_name) or
                time_leaving and not await check_input.is_corr_time(ctx, time_leaving)):
            return

        curr_raid = self.find_raid(captain_name, time_leaving)
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
    async def collection(self, ctx, captain_name, time_leaving=''):
        # Checking correct inputs arguments
        if (not await check_input.is_corr_name(ctx, captain_name) or
                time_leaving and not await check_input.is_corr_time(ctx, time_leaving)):
            return

        curr_raid = self.find_raid(captain_name, time_leaving)
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
                curr_raid.table_msg = await ctx.send(file=discord.File(curr_raid.create_table()))
                curr_raid.time_to_display[index] = ('', '')
            await ctx.send(f"Рейд на {curr_raid.server} с капитаном {curr_raid.captain_name} уже уплыли на ежедневки")
            await self.remove_raid(ctx, captain_name, time_leaving)
        else:
            await ctx.message.add_reaction('❌')

    @commands.command(name='капитан', help=messages.help_msg_captain)
    @commands.has_role('Капитан')
    async def captain(self, ctx, captain_name: str, server: str, time_leaving: str, time_reservation_open='',
                      reservation_count=0):
        # Checking correct inputs arguments
        if (not await check_input.is_corr_name(ctx, captain_name) or
                not await check_input.is_corr_server(ctx, server) or
                not await check_input.is_corr_time(ctx, time_leaving) or
                time_reservation_open and not await check_input.is_corr_time(ctx, time_reservation_open)):
            return
        try:
            int(reservation_count)
        except ValueError:
            await ctx.author.send(f'Команда `{ctx.message.content}` была неправильно введена. Неверное число брони')
            await ctx.message.add_reaction('❔')
            return

        if not time_reservation_open:
            current_hour, current_minute = map(int, time.ctime()[11:16].split(':'))
            if current_minute + 1 < 60:
                current_minute += 1
            else:
                current_minute -= 59
                current_hour += 1 if current_hour < 24 else -23
            time_reservation_open = ':'.join((str(current_hour), str(current_minute)))
        new_raid = raid.Raid(captain_name, server, time_leaving, time_reservation_open, reservation_count)
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
    bot.add_cog(ManageRaid(bot))
    module_logger.debug(f'Успешный запуск bot.raid_manager')

