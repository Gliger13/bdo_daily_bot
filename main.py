import asyncio
import time

import discord
from discord.ext import commands
from pymongo import MongoClient

import instruments as instr
import messages
import raid

# Initialization MongoDB
cluster = MongoClient(<string of DB>)
db = cluster['discord']
coll_mem_surname = db["user_nicknames"]

token = <Discord bot token here>
bot = commands.Bot(command_prefix='!!')
bot.remove_command('help')  # To make custom help

# contains current raids
raid_list = list()


@bot.event
async def on_ready():
    print(f"{time.ctime()[-13:]}\tК рабскому труду готов!")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.message.add_reaction('⛔')
    elif isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.message.add_reaction('❔')
    elif isinstance(error, commands.errors.CommandNotFound):
        await ctx.message.add_reaction('❓')
    else:
        print(error)


@bot.command(name='test', help='Команда для разработчика. Смысла не несёт')
async def test(ctx):
    bot_msg = await ctx.send('Тестируй меня полностью')
    instr.print_log(ctx.author, ctx.message.content, True)
    await asyncio.sleep(10)
    await bot_msg.edit(content="Изменил полностью тебя")


async def update_info(curr_raid):
    info_msg = curr_raid.info_msg.content.split('\n')
    edited_msg = f"Мест осталось {curr_raid.places_left}.\n" + info_msg[1]
    await curr_raid.info_msg.edit(content=edited_msg)


def find_raid(captain_name: str, time_leaving: str) -> raid.Raid:
    if not captain_name:
        return None
    captain_list = [some_raid.captain_name for some_raid in raid_list]
    is_unique_captains = True if len(captain_list) == len(set(captain_list)) else False
    if raid_list and is_unique_captains or raid_list and time_leaving:
        for finding_raid in raid_list:
            if (finding_raid.captain_name == captain_name and finding_raid.time_leaving == time_leaving
                    or finding_raid.captain_name == captain_name):
                return finding_raid
    else:
        return None

# Custom help
@bot.command(name='help')
async def help(ctx, command=''):
    embed_obj = discord.Embed(colour=discord.Colour.blue())
    embed_obj.set_author(name='Помощь')
    commands_list = [command for command in bot.commands]
    if not command:
        # wrap text _ with * to ignore italicization
        commands_list_str = '*\n*'.join([command.qualified_name for command in commands_list])
        commands_list_str = '*' + commands_list_str + '*'
        embed_obj.add_field(
            name='Список команд',
            value=commands_list_str,
            inline=False
        )
        embed_obj.add_field(
            name='Дополнительная помощь',
            value="Чтобы получить подробную информацию об команде напиши '!!help <команда>",
            inline=False
        )
        embed_obj.add_field(
            name='Смайлики',
            value="Если ты поставил или убрал :heart: бот обязан тебе написать в лс\n"
                  "Если под твоей командой есть ✔ - значит бот как-то выполнил её\n"
                  "Если ❌ - ты сделал что-то не так\n"
                  "Если ⛔ - у тебя нет прав\n"
                  "Если ❓ - неизвестная команда\n"
                  "Если ❔ - много или мало аргументов команды\n"
                  "Если ничего не появилось, то поздравляю, ты сломал бота или он не работает",
            inline=False
        )
        await ctx.send(embed=embed_obj)
        await ctx.message.add_reaction('✔')
    else:
        for comm in commands_list:
            if comm.qualified_name == command:
                embed_obj.add_field(
                    name='Помощь по команде:',
                    value='*' + command + '*',
                    inline=False
                )
                embed_obj.add_field(
                    name='Описание',
                    value=comm.help,
                    inline=False
                )
                await ctx.send(embed=embed_obj)
                await ctx.message.add_reaction('✔')
                break
        else:
            await ctx.message.add_reaction('❌')


@bot.event
async def on_reaction_add(reaction, user):
    collection_msg = reaction.message
    if reaction.emoji == '❤' and not user.id == 680516252267184285:  # Ignore bot action
        for curr_raid in raid_list:
            if (curr_raid.collection_msg and curr_raid.collection_msg.id == collection_msg.id and
                    curr_raid.guild == collection_msg.guild):
                nickname = coll_mem_surname.find_one({"discord_user": str(user)})
                if nickname:
                    nickname = nickname["nickname"]
                    if curr_raid.member_dict.get(nickname):
                        await user.send(messages.msg_fail1)
                        instr.print_log(user, 'попасть в рейд через реакцию. Уже есть в списке', False)
                        break
                    else:
                        if curr_raid.places_left != 0:
                            msg_success = (f"Привет!\nТы попал на морские ежедневки к капитану {curr_raid.captain_name}"
                                           f" на сервере {curr_raid.server}.\nОтплытие с Ока Окиллы"
                                           f" в {curr_raid.time_leaving}.\nОб сборе рейда обычно пишут за 5 - 10 минут "
                                           f"до отплытия. Если информации нету, то пиши на"
                                           f" фамилию капитана {curr_raid.captain_name}.")
                            curr_raid += str(nickname)
                            coll_mem_surname.find_one_and_update({'discord_user': str(user)}, {'$inc': {'entries': 1}})
                            await user.send(msg_success)
                            await update_info(curr_raid)
                            instr.print_log(user, 'попасть в рейд через реакцию', True)
                            break
                        else:
                            msg_no_space = "Ты не попал в рейд. Мест не осталось :crying_cat_face:"
                            await user.send(msg_no_space)
                            instr.print_log(user, 'попасть в рейд через реакцию. Нет мест.', False)
                            break
                else:
                    await user.send(messages.msg_fail2)
                    instr.print_log(user, 'попасть в рейд через реакцию. Нет регистрации.', False)
                    break


@bot.event
async def on_reaction_remove(reaction, user):
    collection_msg = reaction.message
    if reaction.emoji == '❤':
        for curr_raid in raid_list:
            if curr_raid.collection_msg.id == collection_msg.id and curr_raid.guild == collection_msg.guild:
                nickname = coll_mem_surname.find_one({"discord_user": str(user)})
                if nickname:
                    nickname = nickname["nickname"]
                    if curr_raid.member_dict.get(nickname):
                        msg_remove = f"Я тебя удалил из списка на ежедневки с капитаном {curr_raid.captain_name}"
                        curr_raid -= str(nickname)
                        coll_mem_surname.find_one_and_update({'discord_user': str(user)}, {'$inc': {'entries': -1}})
                        await user.send(msg_remove)
                        await update_info(curr_raid)
                        instr.print_log(user, 'убрать себя из рейда через реакцию', True)
                        break


@bot.command(name='осуди_его!', help='Бот начинает осуждать человека.')
@commands.has_role('Капитан')
async def msg_lol(ctx):
    bot_msg = await ctx.send("Я осуждаю его!")
    instr.print_log(ctx.author, ctx.message.content, True)
    await asyncio.sleep(10)
    await bot_msg.edit(content='Фу таким быть')
    await asyncio.sleep(10)
    await bot_msg.edit(content='Я осуждаю его')
    await asyncio.sleep(10)
    await bot_msg.edit(content='Я печенька')
    await asyncio.sleep(10)
    await bot_msg.edit(content='Я осуждаю его')


@bot.command(name='очисти_чат', help=messages.help_msg_rem_msgs)
@commands.has_role('Капитан')
async def rem_msgs(ctx, amount=100):
    channel = ctx.message.channel
    if channel.id == 677857180833021953 or channel.id == 676882231825924125 or channel.id == 686971780325572649:
        messages = []
        async for msg in channel.history(limit=int(amount)):
            if msg.id != 677857214282727459 and msg.id != 676883151565619242 and msg.id != 686978560795344909:
                messages.append(msg)
        await channel.delete_messages(messages)
        instr.print_log(ctx.author, ctx.message.content, True)
    else:
        await ctx.message.add_reaction('❌')
        instr.print_log(ctx.author, ctx.message.content, False)

# Just a massive DM message invite registration
@bot.command(name='начать_регистрацию', help=messages.help_msg_dm_invite_reg)
@commands.has_role('Капитан')
async def dm_invite_reg(ctx):
    msg_reg_invite = """Привет! Я БартерБот из сервера Бартерята. Я не работаю 24/7, хозяин добрый.  
                     Так что я отвечаю на твои команды только тогда, когда я онлайн. 
                     Если хочешь через один тык на смайлики под сообщением о сборе
                     забронировать место в рейде, то тебе нужно написать мне в личку, сюда, команду
                      '!!рег [ФАМИЛИЯ]', где вместо [ФАМИЛИЯ] нужно вписать свою игровую фамилию из BDO.
                     Например '!!рег Mandeson'. Если ты уже один раз это сделал, то больше не нужно.
                     Удачи в твоих морских путешествиях :)"""
    await ctx.author.send(msg_reg_invite)
    await ctx.message.add_reaction('✔')
    instr.print_log(ctx.author, ctx.message.content, True)


@bot.command(name='загрузи_рейд', help=messages.help_msg_load_raid)
@commands.has_role('Капитан')
async def load_raid(ctx, captain_name, time_leaving):
    try:
        file_name = f"./saves/{captain_name}_{'-'.join(time_leaving.split(':'))}.txt"
        file = open(file_name, 'r')
        file_iter = iter(file)
        line = next(file_iter)[:-1]
        (captain_name, server, time_leaving, time_reservation_open,
         reservation_count) = line.split(',')
        line = next(file_iter)[:-1]
        nicknames = line.split(' ')
        old_raid = raid.Raid(captain_name, server, time_leaving, time_reservation_open, int(reservation_count) - 2)
        for name in nicknames:
            old_raid += str(name)
        old_raid.update_info()
        raid_list.append(old_raid)
        await ctx.message.add_reaction('✔')
        instr.print_log(ctx.author, ctx.message.content, True)
    except FileNotFoundError:
        await ctx.message.add_reaction('❌')
        instr.print_log(ctx.author, ctx.message.content, False)
    finally:
        file.close()


@bot.command(name='рег', help=messages.help_msg_reg)
async def reg(ctx, name: str):
    # Try to find user in BD
    nickname = coll_mem_surname.find_one({"discord_user": str(ctx.author)})
    if not nickname:  # If not find...
        post = {'discord_user': str(ctx.author), 'nickname': str(name), 'entries': 0}
        coll_mem_surname.insert_one(post)
        instr.print_log(ctx.author, ctx.message.content, True)
        await ctx.message.add_reaction('✔')
    else:
        await ctx.author.send("Ты уже зарегистрировался, хватит использовать эту команду."
                              " Сейчас тапком в тебя кину! :sandal: ")
        await ctx.message.add_reaction('❌')


@bot.command(name='сохрани_рейд', help='сохраняет рейд')
async def save_raid(ctx, captain_name: str, time_leaving=''):
    curr_raid = find_raid(captain_name, time_leaving)
    curr_raid.save_raid()
    await ctx.message.add_reaction('✔')


@bot.command(name='бронь', help=messages.help_msg_reserve)
@commands.has_role('Капитан')
async def reserve(ctx, name: str, captain_name='', time_leaving=''):
    curr_raid = find_raid(captain_name, time_leaving)
    if curr_raid:
        if curr_raid.member_dict.get(name):
            instr.print_log(ctx.author, ctx.message.content, False)
            await ctx.message.add_reaction('❌')
            return
        curr_raid += name
        instr.print_log(ctx.author, ctx.message.content, True)
        await ctx.message.add_reaction('✔')
        await update_info(curr_raid)
    else:
        guild_raid_list = []
        for curr_raid in raid_list:
            if curr_raid.guild == ctx.message.guild and not curr_raid.member_dict.get(name):
                guild_raid_list.append(curr_raid)
                break
        if not guild_raid_list:  # If list empty
            instr.print_log(ctx.author, ctx.message.content, False)
            await ctx.message.add_reaction('❌')
            return
        smaller_raid = min(guild_raid_list)
        smaller_raid += name
        instr.print_log(ctx.author, ctx.message.content, True)
        await ctx.message.add_reaction('✔')


@bot.command(name='удали_бронь', help=messages.help_msg_remove_res)
@commands.has_role('Капитан')
async def remove_res(ctx, name: str):
    for finding_raid in raid_list:
        finding_raid -= name
        if finding_raid:
            await update_info(finding_raid)
            await ctx.message.add_reaction('✔')
            instr.print_log(ctx.author, ctx.message.content, True)
            break
    else:
        await ctx.message.add_reaction('❌')
        instr.print_log(ctx.author, ctx.message.content, False)


@bot.command(name='покажи_рейды', help=messages.help_msg_show_raids)
async def show_raids(ctx):
    instr.print_log(ctx.author, ctx.message.content, True)
    if raid_list:
        msg_of_raid = "В данный момент собирают рейды:\n"
        for curr_raid in raid_list:
            msg_of_raid += (f"Капитан {curr_raid.captain_name} на канале {curr_raid.server}"
                            f" выплывает в {curr_raid.time_leaving}.")
        await ctx.send(msg_of_raid)
    else:
        msg_no_raids = "В данный момент никто не собирает рейд, или собирают, но не через меня :cry:"
        await ctx.send(msg_no_raids)


@bot.command(name='покажи', help=messages.help_msg_show)
@commands.has_role('Капитан')
async def show(ctx, captain_name, time_leaving=''):
    curr_raid = find_raid(captain_name, time_leaving)
    if curr_raid:
        link = curr_raid.create_table()
        curr_raid.save_raid()
        await ctx.send(file=discord.File(link))
        await ctx.message.add_reaction('✔')
        instr.print_log(ctx.author, ctx.message.content, True)
    else:
        await ctx.message.add_reaction('❌')
        instr.print_log(ctx.author, ctx.message.content, False)


@bot.command(name='удали_рейд', help=messages.help_msg_remove_raid)
@commands.has_role('Капитан')
async def remove_raid(ctx, captain_name, time_leaving=''):
    curr_raid = find_raid(captain_name, time_leaving)
    if curr_raid:
        curr_raid.is_delete_raid = True
        for task in curr_raid.task_list:
            task.cancel()
        raid_list.remove(curr_raid)
        await ctx.message.add_reaction('✔')
        instr.print_log(ctx.author, ctx.message.content, True)
    else:
        await ctx.message.add_reaction('❌')
        instr.print_log(ctx.author, ctx.message.content, False)


@bot.command(name='сбор', help=messages.help_msg_collection)
@commands.has_role('Капитан')
async def collection(ctx, captain_name, time_leaving=''):
    curr_raid = find_raid(captain_name, time_leaving)
    if curr_raid:
        collection_msg = (f"Капитан {curr_raid.captain_name} выплывает на морские ежедневки с Око Окиллы в "
                          f"{curr_raid.time_leaving} на канале {curr_raid.server}."
                          f" Всего осталось {curr_raid.places_left}"
                          f"мест.\nЖелающие присоединиться к нему должны нажать на :heart:.\n"
                          f" И обязательно, посмотрите сообщение,"
                          f"которое я вам выслал в личные сообщения, может быть вы не попали в рейд.")
        curr_raid.guild = ctx.message.guild
        curr_raid.collection_msg = await ctx.send(collection_msg)
        curr_raid.info_msg = await ctx.send(f"Мест осталось {curr_raid.places_left}.\nТаблица появится скоро.")
        await curr_raid.collection_msg.add_reaction('❤')
        # Show raid_table in time
        curr_raid.table_msg = await ctx.send('Тут будет таблица')
        for sec_left, time_display in curr_raid.time_left_to_display():
            await curr_raid.info_msg.edit(content=f"Мест осталось {curr_raid.places_left}.\n"
                                                  f"Обновлённая таблица появится в {time_display}.")
            curr_raid.save_raid()
            instr.print_log(ctx.author, 'сохранить рейд', True)
            await asyncio.sleep(sec_left)
            await curr_raid.table_msg.delete()
            curr_raid.table_msg = await ctx.send(file=discord.File(curr_raid.create_table()))
        await ctx.send(f"Рейд на {curr_raid.server} с капитаном {curr_raid.captain_name} уже уплыли на ежедневки")
        await remove_raid(ctx, captain_name, time_leaving)
    else:
        await ctx.message.add_reaction('❌')


@bot.command(name='капитан', help=messages.help_msg_captain)
@commands.has_role('Капитан')
async def captain(ctx, captain_name: str, server: str, time_leaving: str, time_reservation_open='',
                  reservation_count=0):
    async def start_captain_task(curr_raid):
        time_left_sec = instr.get_sec_left(time_reservation_open)
        await ctx.send(f"Новый рейд создан! Теперь участники могут записатся к тебе!\n"
                       f"Бронирование мест начнется в {time_reservation_open}")
        await ctx.message.add_reaction('✔')
        instr.print_log(ctx.author, ctx.message.content, True)
        await asyncio.sleep(time_left_sec)
        task2 = asyncio.create_task(collection(ctx, captain_name, time_leaving))
        curr_raid.task_list.append(task2)
        await task2

    if not time_reservation_open:
        current_hour, current_minute = map(int, time.ctime()[11:16].split(':'))
        if current_minute + 1 < 60:
            current_minute += 1
        else:
            current_minute -= 59
            current_hour += 1 if current_hour < 24 else -23
        time_reservation_open = ':'.join((str(current_hour), str(current_minute)))
    new_raid = raid.Raid(captain_name, server, time_leaving, time_reservation_open, reservation_count)
    new_raid.guild = ctx.message.guild
    raid_list.append(new_raid)
    task1 = asyncio.create_task(start_captain_task(new_raid))
    new_raid.task_list.append(task1)
    await task1

bot.run(token)
