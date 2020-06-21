import logging

import discord
from discord.ext import commands

from commands.raid_manager import common
from instruments import check_input, help_messages, database_process

module_logger = logging.getLogger('my_bot')


class RaidOverview(commands.Cog):
    database = database_process.DatabaseManager()
    raid_list = common.Raids.active_raids

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='покажи_рейды', help=help_messages.show_raids)
    async def show_raids(self, ctx: commands.context.Context, show_all=''):
        module_logger.info(f'{ctx.author} использовал команду {ctx.message.content}')
        if not show_all:
            if self.raid_list:
                msg_of_raid = "В данный момент собирают рейды:\n"
                for curr_raid in self.raid_list:
                    msg_of_raid += (
                        f"{str(ctx.channel)} - капитан **{curr_raid.captain_name}** на канале **{curr_raid.server}**"
                        f" выплывает в **{curr_raid.time_leaving}**.\n"
                    )
                await ctx.send(msg_of_raid)
            else:
                msg_no_raids = "В данный момент никто здесь не собирает рейды, или собирают, но не через меня :cry:"
                await ctx.send(msg_no_raids)
        elif show_all:
            if self.raid_list:
                msg_of_raid = "В данный момент собирают рейды:\n"
                for curr_raid in self.raid_list:
                    msg_of_raid += (
                        f" {str(ctx.guild)}/{str(ctx.channel)} - капитан **{curr_raid.captain_name}**"
                        f" выплывает в **{curr_raid.time_leaving}**.\n"
                    )
                await ctx.send(msg_of_raid)
            else:
                msg_no_raids = "В данный момент никто не собирает рейд, или собирают, но не через меня :cry:"
                await ctx.send(msg_no_raids)

    @commands.command(name='покажи_состав', help=help_messages.show_text_raids)
    @commands.has_role('Капитан')
    async def show_text_raids(self, ctx: commands.context.Context, captain_name, time_leaving=''):
        # Checking correct inputs arguments
        await check_input.validation(**locals())

        curr_raid = common.find_raid(ctx.guild.id, ctx.channel.id, captain_name, time_leaving, ignore_channels=True)
        if curr_raid:
            text = curr_raid.table.create_text_table()
            title = text.split('\n')[0]
            embed = discord.Embed(
                title=title,
                colour=discord.Colour.blue(),
                description=text[len(title) + 1:]
            )
            await ctx.send(curr_raid.table.create_text_table())
            await ctx.message.add_reaction('✔')
            module_logger.info(f'{ctx.author} успешно использовал команду {ctx.message.content}')
        else:
            await ctx.message.add_reaction('❌')
            module_logger.info(f'{ctx.author} неудачно использовал команду {ctx.message.content}')

    @commands.command(name='покажи', help=help_messages.show)
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
