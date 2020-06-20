import asyncio
import logging
import time

import discord
from discord.ext import commands

from commands.raid_manager import common
from instruments import check_input, raid, messages, database_process, tools
from instruments.raid import Raid

module_logger = logging.getLogger('my_bot')


class RaidCreation(commands.Cog):
    database = database_process.Database()
    raid_list = common.Raids.active_raids

    def __init__(self, bot):
        self.bot = bot

    async def notify_about_leaving(self, current_raid: Raid):
        secs_sleep = current_raid.raid_time.secs_to_notify()
        if not secs_sleep:
            return

        sleep_task = asyncio.create_task(asyncio.sleep(secs_sleep))
        current_raid.raid_time.notification_task = sleep_task
        await sleep_task

        member_msg = (
            f"До отплытия капитана осталось **7 минут**!\n"
            f"У тебя есть ещё время подготовиться, если ещё не готов."
        )
        users_list = self.database.get_users_id(list(current_raid.member_dict.keys()))
        for member in users_list:
            if member:
                user = self.bot.get_user(member.get('discord_id'))
                await user.send(member_msg)

        captain_msg = (
            f"Капитан, у вас отплытие через **7 минут**!\n"
        )

        captain_id = self.database.user_post_by_name(current_raid.captain_name).get('discord_id')
        captain = self.bot.get_user(captain_id)
        await captain.send(captain_msg)

    @commands.command(name='удали_рейд', help=messages.help_msg_remove_raid)
    @commands.has_role('Капитан')
    async def remove_raid(self, ctx: commands.context.Context, captain_name, time_leaving=''):
        # Checking correct inputs arguments
        await check_input.validation(**locals())

        curr_raid = common.find_raid(ctx.guild.id, ctx.channel.id, captain_name, time_leaving)
        if curr_raid:
            curr_raid.is_delete_raid = True
            if curr_raid.raid_time.notification_task:
                curr_raid.raid_time.notification_task.cancel()
            if curr_raid.collection_task:
                curr_raid.collection_task.cancel()
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
        if curr_raid and not curr_raid.is_delete_raid:
            # Send msg about collection and save data
            collection_msg = (f"Капитан **{curr_raid.captain_name}** выплывает на морские ежедневки с Око Окиллы в "
                              f"**{curr_raid.raid_time.time_leaving}** на канале **{curr_raid.server}**.\n"
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
            curr_raid.raid_time.validate_time()
            for tasks in curr_raid.task_list:
                tasks.cancel()

            raid_time = zip(curr_raid.raid_time.time_to_display, curr_raid.raid_time.secs_to_display)
            for index, (time_display, sec_left) in enumerate(raid_time):
                # Update text msg of start collection Raid
                edited_text = f'Обновлённая таблица появится в {time_display}.'
                old_text = curr_raid.collection_msg.content
                start_index = old_text.find('Обновлённая')
                new_text = old_text[:start_index] + edited_text
                await curr_raid.collection_msg.edit(content=new_text)

                curr_raid.save_raid()
                module_logger.info(f'Сохранение рейда {curr_raid.captain_name}')

                # Notify user if possible
                await self.notify_about_leaving(curr_raid)
                sleep_task = asyncio.create_task(asyncio.sleep(sec_left))
                curr_raid.task_list.append(sleep_task)
                await sleep_task
                for tasks in curr_raid.task_list:
                    tasks.cancel()
                await curr_raid.table_msg.delete()
                curr_raid.table_msg = await ctx.send(file=discord.File(curr_raid.table_path()))
                curr_raid.raid_time.remove_previous_time()

            self.database.update_captain(str(ctx.author), curr_raid)

            await ctx.send(f"Рейд на {curr_raid.server} с капитаном {curr_raid.captain_name} уже уплыли на ежедневки")
            await self.remove_raid(ctx, captain_name, time_leaving)
        else:
            await ctx.message.add_reaction('❌')

    @commands.command(name='капитан', help=messages.help_msg_captain)
    @commands.has_role('Капитан')
    async def captain(self, ctx: commands.context.Context, captain_name: str, server: str,
                      time_leaving: str, time_reservation_open='', reservation_count=0):
        # Checking correct inputs arguments
        await check_input.validation(**locals())
        # Check captain exists
        captain_post = self.database.find_captain_post(str(ctx.author))
        if not captain_post:
            self.database.create_captain(str(ctx.author))

        if not time_reservation_open:
            current_hour, current_minute = map(int, time.ctime()[11:16].split(':'))
            if current_minute + 1 < 60:
                current_minute += 1
            else:
                current_minute -= 59
                current_hour += 1 if current_hour < 24 else -23
            time_reservation_open = ':'.join((str(current_hour), str(current_minute)))
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
        new_raid.guild = ctx.guild

        time_left_sec = tools.get_sec_left(time_reservation_open)
        hour, minutes = time_reservation_open.split(':')
        time_open = f"{hour}:{minutes}" if len(minutes) == 2 else f"{hour}:0{minutes}"
        await ctx.send(f"Новый рейд создан! Теперь участники могут записатся к тебе!\n"
                       f"Бронирование мест начнется в **{time_open}**")
        await ctx.message.add_reaction('✔')
        module_logger.info(f'{ctx.author} удачно использовал команду {ctx.message.content}')

        # Create sleep task for collection command
        sleep_task = asyncio.create_task(asyncio.sleep(time_left_sec))
        new_raid.collection_task = sleep_task
        await sleep_task
        await self.collection(ctx, captain_name, time_leaving)

    @commands.command(name='кэп', help=messages.help_msg_captain)
    @commands.has_role('Капитан')
    async def cap(self, ctx: commands.context.Context):
        NUMBER_REACTIONS = {
            '1️⃣': 1, '2️⃣': 2, '3️⃣': 3,
            1: '1️⃣', 2: '2️⃣', 3: '3️⃣'
        }

        user = str(ctx.author)
        captain_post = self.database.find_captain_post(user)
        if not captain_post:
            await ctx.message.add_reaction('❌')
            await ctx.author.send(
                f"Привет, я тебя ещё не знаю! Рэйдов ты не создавал ещё. Воспользуйся командой `!!капитан`"
            )
            module_logger.info(f'{ctx.author} неудачно использовал команду {ctx.message.content}. Нету такого капитана')
            return
        last_raids = captain_post.get('last_raids')
        raids_msg = f"Какой из рейдов мне создать, капитан **{captain_post['captain_name']}**?\n"
        for index, last_raid in enumerate(last_raids):
            raids_msg += (
                f"{index + 1}) На сервере **{last_raid['server']}**, который отплывает в"
                f" **{last_raid['time_leaving']}**"
            )
            if last_raid.get('time_reservation_open'):
                raids_msg += f", время начала сбора в **{last_raid['time_reservation_open']}**"
            if last_raid.get('reservation_count') and not last_raid['reservation_count'] == 1:
                raids_msg += f", количество забронированных мест **{last_raid['reservation_count']}**"
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
            module_logger.info(f'{ctx.author} неудачно использовал команду {ctx.message.content}. Время на ответ вышло')
            await ctx.message.add_reaction('❌')
        else:
            user_choice = NUMBER_REACTIONS[str(reaction.emoji)]
            user_raid = last_raids[user_choice - 1]

            module_logger.info(f'{ctx.author} удачно использовал команду {ctx.message.content}')
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
    module_logger.debug(f'Успешный запуск bot.raid_manager.creation')
