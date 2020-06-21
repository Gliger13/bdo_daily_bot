import asyncio
import logging

import discord
from discord.ext import commands

from instruments import check_input, database_process
from settings import settings

module_logger = logging.getLogger('my_bot')


class Base(commands.Cog):
    database = database_process.DatabaseManager()

    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command('help')  # To make custom help

    @commands.command(name='test', help='Команда для разработчика. Смысла не несёт')
    async def test(self, ctx: commands.context.Context):
        await check_input.validation(**locals())
        module_logger.info(f'{ctx.author} ввёл команду {ctx.message.content}')
        await ctx.message.add_reaction('❌')
        await ctx.message.add_reaction('✔')

    @commands.command(name='pvp')
    @commands.has_role('Капитан')
    async def pvp(self, ctx):
        msg_pvp = await ctx.send('Если хочешь для себя открыть PVP контент, то нажми на ⚔️️')
        role = discord.utils.get(ctx.guild.roles, name="PVP")
        await msg_pvp.add_reaction('⚔️')

        def check(reaction, user):
            return str(reaction.emoji) == '⚔️'

        def create_task_reaction_add():
            add_reaction_task = asyncio.create_task(
                self.bot.wait_for('reaction_add', check=check)
            )
            add_reaction_task.set_name('reaction_add')
            return add_reaction_task

        def create_task_reaction_remove():
            remove_reaction_task = asyncio.create_task(
                self.bot.wait_for('reaction_remove', check=check)
            )
            remove_reaction_task.set_name('reaction_remove')
            return remove_reaction_task

        while True:
            pending_tasks = [
                create_task_reaction_add(),
                create_task_reaction_remove(),
            ]
            done_tasks, pending_tasks = await asyncio.wait(pending_tasks, return_when=asyncio.FIRST_COMPLETED)
            for task in done_tasks:
                reaction, user = task.result()
                if task.get_name() == 'reaction_add':
                    await user.add_roles(role)
                elif task.get_name() == 'reaction_remove':
                    await user.remove_roles(role)
            for task in pending_tasks:
                task.cancel()

    async def help_command(self, ctx, command):
        command = self.bot.get_command(command)
        if command:
            embed = discord.Embed(
                title=command.name,
                colour=discord.Colour.blue(),
                description=command.help,
            )

            bot_as_user = self.bot.get_user(settings.BOT_ID)
            embed.set_author(
                name=str(bot_as_user),
                icon_url=bot_as_user.avatar_url,
            )
            await ctx.send(embed=embed)
            await ctx.message.add_reaction('✔')
        else:
            await ctx.message.add_reaction('❌')

    # Custom help
    @commands.command(name='help')
    async def help(self, ctx, command=''):
        module_logger.info(f'{ctx.author} ввёл команду {ctx.message.content}')

        if command:
            await self.help_command(ctx, command)
            return

        HELP_EMODJI = ['🔼', '1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣']
        pages = {}
        not_help_cogs = ['Base', 'Events']
        normal_names = {
            'Admin': 'администрирование',
            'Fun': 'фан',
            'Statistics': 'статистика',
            'RaidCreation': 'создание рейда',
            'RaidSaveLoad': 'загрузка/сохранение рейда',
            'RaidRegistration': 'регистрация',
            'RaidJoining': 'попадание в рейд',
            'RaidOverview': 'просмотр рейда',
        }

        cogs_commands = {}
        for cog_name in self.bot.cogs:
            if cog_name not in not_help_cogs:
                cogs_commands[normal_names[cog_name]] = self.bot.get_cog(cog_name).get_commands()

        main_embed = discord.Embed(
            title='Команды бота',
            colour=discord.Colour.blue()
        )

        bot_as_user = self.bot.get_user(settings.BOT_ID)
        main_embed.set_author(
            name=str(bot_as_user),
            icon_url=bot_as_user.avatar_url,
        )

        section_help = f"**{HELP_EMODJI[0]}  -  описание разделов**\n"

        for index, (cog_name, bot_commands) in enumerate(cogs_commands.items()):
            section_help += f"**{HELP_EMODJI[1:][index]}  -  {cog_name}**\n"
            page = f"**{cog_name}**:\n"
            for command in bot_commands:
                page += f"**`{settings.PREFIX}{command.name}` - {command.short_doc}**\n"

            embed_page = discord.Embed(
                title='Команды бота',
                colour=discord.Colour.blue(),
                description=page
            )

            embed_page.set_author(
                name=str(bot_as_user),
                icon_url=bot_as_user.avatar_url,
            )

            pages[HELP_EMODJI[1:][index]] = embed_page

        main_embed.add_field(
            name='Разделы команд',
            value=section_help,
            inline=False
        )

        main_embed.add_field(
            name='Автор',
            value=f'`{settings.PREFIX}автор` - приглашение в Бартерята, исходный код',
            inline=False
        )

        main_embed.add_field(
            name='Дополнительная помощь',
            value="Чтобы получить подробную информацию об команде напиши `!!help [команда]`",
            inline=False
        )

        main_embed.add_field(
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

        pages[HELP_EMODJI[0]] = main_embed

        help_msg = await ctx.send(embed=main_embed)
        for emodji in HELP_EMODJI:
            await help_msg.add_reaction(emodji)

        def check(reaction, user):
            return (
                    user == ctx.message.author and
                    str(reaction.emoji) in HELP_EMODJI
            )

        while True:
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=600.0, check=check)
            except asyncio.TimeoutError:
                return

            embed = pages.get(str(reaction))
            if embed:
                await help_msg.edit(embed=embed)

    @commands.command(name='заверши_работу')
    async def start_exit(self, ctx):
        if ctx.author.id == 324528465682366468:
            module_logger.info(f'Программа была завершена по команде')
            await self.bot.logout()

    @commands.command(name='автор')
    async def author_of_bot(self, ctx: commands.context.Context):
        msg = (
            f"Бот был сделан **Gliger#7748** (Андрей).\n"
            f"Версия бота: **2.0.0**.\n"
            f"Сделан на Python, исходный код можно увидеть на https://github.com/Gliger13/bdo_daily_bot.\n"
            f"Приглашение в Отряд Бартерят - https://discord.gg/msMnCaV"
        )
        embed = discord.Embed(
            title='Автор',
            colour=discord.Colour.blue(),
            description=msg
        )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Base(bot))
    module_logger.debug('Успешный запуск bot.base')
