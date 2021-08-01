"""
Contain user commands for creating and deleting raids
"""
import asyncio

from discord.ext import commands
from discord.ext.commands import Context

from core.commands.raid.builder import RaidBuilder
from core.logger import log_template
from core.parser.raid_input_parser import RaidInputAttributes, RaidInputParser
from messages import command_names, help_text


class RaidCreation(commands.Cog):
    """
    Cog that response for creating and removing raids
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name=command_names.function_command.captain, help=help_text.captain)
    @commands.guild_only()
    @commands.has_role('Капитан')
    async def captain(self, ctx: Context, captain_name: str, game_server: str, time_leaving: str,
                      time_reservation_open: str = '', reservation_amount: str = ''):
        """
        Create raid and start raid flow process of collection user into the new raid.

        :param ctx: discord command context
        :param captain_name: Nickname of user who drove people
        :param game_server: game server where captain will carry raid
        :param time_leaving: time when raid will sail.
        :param time_reservation_open: time when bot start collection people in raid.
        :param reservation_amount: amount of places which cannot be borrowed
        """
        if raid_item := await RaidInputParser.get_raid_item_from_input(**locals()):
            asyncio.ensure_future(RaidBuilder.build_by_command(ctx, raid_item))

    @commands.command(name=command_names.function_command.cap, help=help_text.cap)
    @commands.guild_only()
    @commands.has_role('Капитан')
    async def cap(self, ctx: Context):
        """
        Create raid using only discord command context

        Create raid using only discord command context and database. Gets captain name and
        other raids attributes by database request.

        :param ctx: discord command context
        """
        await RaidBuilder.build_by_ctx(ctx)

    @commands.command(name=command_names.function_command.remove_raid, help=help_text.remove_raid)
    @commands.guild_only()
    @commands.has_role('Капитан')
    async def remove_raid(self, ctx: Context, captain_name: str = '', time_leaving: str = ''):
        """
        Remove raid by given captain and time leaving

        Remove raid by given captain name. If captain name is empty, then try get it from database by user id.
        If time_leaving is empty, then ask user what raid he want to remove. If exist only one raid, then
        ask user about he choice.

        :param ctx: discord command context
        :param captain_name: captain name of raid to remove
        :param time_leaving: time leaving of raid to remove
        """
        if parsed_input := await RaidInputParser.parse_raid_remove_input(**locals()):
            captain_name = parsed_input.get(RaidInputAttributes.CAPTAIN_NAME.attribute_name)
            time_leaving = parsed_input.get(RaidInputAttributes.TIME_LEAVING.attribute_name)
            await RaidBuilder.destroy(ctx, captain_name, time_leaving)


def setup(bot):
    bot.add_cog(RaidCreation(bot))
    log_template.cog_launched('RaidCreation')
