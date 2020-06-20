import json
import logging
import os

from discord.ext import commands

from commands.raid_manager import common
from instruments import check_input, raid, messages

module_logger = logging.getLogger('my_bot')


class RaidSaveLoad(commands.Cog):
    raid_list = common.Raids.active_raids

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='загрузи_рейд', help=messages.help_msg_load_raid)
    @commands.has_role('Капитан')
    async def load_raid(self, ctx: commands.context.Context, captain_name, time_leaving):
        # Checking correct input
        await check_input.validation(**locals())

        # Checking save file exists
        file_name = f"saves/{captain_name}_{'-'.join(time_leaving.split(':'))}.json"
        if not os.path.exists(file_name):
            await check_input.not_correct(ctx, 'Файл сохранения не найден')
            return

        # Open file and load information in new Raid
        with open(file_name, 'r', encoding='utf-8') as save_file:
            raid_information = json.load(save_file)
        old_raid = raid.Raid(
            captain_name=raid_information['captain_name'],
            server=raid_information['server'],
            time_leaving=raid_information['time_leaving'],
            time_reservation_open=raid_information['time_reservation_open'],
            guild_id=raid_information['guild_id'],
            channel_id=raid_information['channel_id'],
            reservation_count=int(raid_information['reservation_count']),
        )
        old_raid.raid_time.time_to_display = raid_information['time_to_display']
        old_raid.raid_time.secs_to_display = raid_information['secs_to_display']
        old_raid.member_dict.update(raid_information['members_dict'])
        old_raid.members_count = raid_information['members_count']
        self.raid_list.append(old_raid)
        module_logger.info(f'{ctx.author} успешно использовал команду {ctx.message.content}')
        await ctx.message.add_reaction('✔')

    @commands.command(name='сохрани_рейды', help='сохраняет все рейды')
    async def save_raids(self, ctx: commands.context.Context):
        if self.raid_list:
            for some_raid in self.raid_list:
                some_raid.save_raid()
            module_logger.info(f'{ctx.author} успешно использовал команду {ctx.message.content}')
            await ctx.message.add_reaction('✔')
        else:
            module_logger.info(f'{ctx.author} неудачно использовал команду {ctx.message.content}. Не рейдов')
            await ctx.message.add_reaction('❌')

    @commands.command(name='сохрани_рейд', help='сохраняет рейд')
    async def save_raid(self, ctx: commands.context.Context, captain_name: str, time_leaving=''):
        # Checking correct input
        await check_input.validation(**locals())

        curr_raid = common.find_raid(ctx.guild.id, ctx.channel.id, captain_name, time_leaving, ignore_channels=True)
        # if not find raid to save
        if not curr_raid:
            await check_input.not_correct(ctx, 'Не нашёл рейд для сохранение.')
            return

        curr_raid.save_raid()
        module_logger.info(f'{ctx.author} успешно использовал команду {ctx.message.content}')
        await ctx.message.add_reaction('✔')


def setup(bot):
    bot.add_cog(RaidSaveLoad(bot))
    module_logger.debug(f'Успешный запуск bot.raid_manager.save_load')
