import logging

import discord
from discord.ext import commands

from commands.raid_manager import common
from instruments import check_input, messages, database_process

module_logger = logging.getLogger('my_bot')


class RaidOverview(commands.Cog):
    database = database_process.Database()
    raid_list = common.Raids.active_raids

    def __init__(self, bot):
        self.bot = bot

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


def setup(bot):
    bot.add_cog(RaidOverview(bot))
    module_logger.debug(f'Успешный запуск bot.raid_manager.overview')
