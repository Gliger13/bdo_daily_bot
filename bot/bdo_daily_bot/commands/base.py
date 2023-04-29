"""
Module contain discord cog with name `Base`. Provide base discord commands for
debugging or providing bot information
"""
import asyncio
import os

import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext.commands import Context

from bdo_daily_bot.core.commands_reporter.command_failure_reasons import CommandFailureReasons
from bdo_daily_bot.core.commands_reporter.reporter import Reporter
from bdo_daily_bot.core.logger import log_template
from bdo_daily_bot.core.tools.path_factory import ProjectPathFactory
from bdo_daily_bot.messages import command_names
from bdo_daily_bot.messages import help_text
from bdo_daily_bot.messages import messages
from bdo_daily_bot.settings import settings


class Base(commands.Cog):
    """
    Cog that responsible for basic bot commands.
    """

    def __init__(self, bot: Bot):
        """
        :param bot: discord bot for executing the cog commands
        """
        self.bot = bot
        self.reporter = Reporter()
        self.bot.remove_command("help")  # Remove command to create custom help

    @commands.command(name=command_names.function_command.test, help=help_text.test)
    async def test(self, ctx: Context):
        """
        Command witch does nothing. For developing and debugging

        :param ctx: discord command context
        """
        await self.reporter.report_success_command(ctx)

    async def help_command(self, ctx: Context, command: str):
        """
        Send command detailed description as message in channel of the given context

        :param ctx: discord command context
        :param command: discord command name to get information
        """
        # Get command obj from the name
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

            await self.reporter.report_success_command(ctx)
        else:
            await self.reporter.report_unsuccessful_command(ctx, CommandFailureReasons.COMMAND_NOT_FOUND)

    @commands.command(name=command_names.function_command.send_logs, help=help_text.send_logs)
    @commands.is_owner()
    async def send_logs(self, ctx: Context):
        """
        Command for admins and developers. Send the bot logs as message with attachment to a channel

        :param ctx: discord command context
        """
        path_to_logs = ProjectPathFactory.get_logs_path()
        if os.path.exists(path_to_logs):
            await ctx.send(file=discord.File(path_to_logs))
            await self.reporter.report_success_command(ctx)
        else:
            await self.reporter.report_unsuccessful_command(ctx, CommandFailureReasons.LOGS_NOT_FOUND)

    @commands.command(name=command_names.function_command.help_command, help=help_text.help_command)
    async def help(self, ctx: Context, command=""):
        """
        Command to send help of the all bot commands as embed

        :param ctx: discord command context
        :param command: discord command name to get information
        """
        # If user enter name of command to get description
        if command:
            await self.help_command(ctx, command)
            return

        # Dict of emoji for control custom help
        help_emojis = ["🔼", "1⃣", "2⃣", "3⃣", "4⃣", "5⃣", "6⃣", "7⃣", "8⃣", "9️⃣"]
        pages = {}
        # Cogs witch should not be shown in help
        not_help_cogs = ["Base", "Events"]

        # Get all available commands of the bot
        cogs_commands = {}
        for cog_name in self.bot.cogs:
            if cog_name not in not_help_cogs:
                cogs_commands[messages.cog_names[cog_name]] = self.bot.get_cog(cog_name).get_commands()

        main_embed = discord.Embed(title=messages.help_title, colour=discord.Colour.blue())

        bot_as_user = self.bot.get_user(settings.BOT_ID)
        main_embed.set_author(
            name=str(bot_as_user),
            icon_url=bot_as_user.avatar_url,
        )

        # Generate pages of cogs with description of all commands in cog
        section_help = messages.section_help.format(emoji=help_emojis[0])
        for index, (cog_name, bot_commands) in enumerate(cogs_commands.items()):
            section_help += f"**{help_emojis[1:][index]}  -  {cog_name}**\n"
            page = f"**{cog_name}**:\n"
            for bot_command in bot_commands:
                page += f"**`{settings.PREFIX}{bot_command.name}` - {bot_command.short_doc}**\n"

            embed_page = discord.Embed(title=messages.help_title, colour=discord.Colour.blue(), description=page)

            embed_page.set_author(
                name=str(bot_as_user),
                icon_url=bot_as_user.avatar_url,
            )

            pages[help_emojis[1:][index]] = embed_page

        main_embed.add_field(name=messages.section_title, value=section_help, inline=False)

        main_embed.add_field(name=messages.author_title, value=messages.author_command_description, inline=False)

        main_embed.add_field(name=messages.additional_help_title, value=messages.additional_help, inline=False)

        main_embed.add_field(name=messages.help_reaction_title, value=messages.help_reaction, inline=False)

        # Set home page
        pages[help_emojis[0]] = main_embed

        help_msg = await ctx.send(embed=main_embed)

        await self.reporter.report_success_command(ctx)

        # Add control emoji for message
        for emoji in help_emojis:
            await help_msg.add_reaction(emoji)

        def check(reaction, user):
            """
            Only user who use command can use control emoji
            """
            return user == ctx.message.author and str(reaction.emoji) in help_emojis

        while True:
            try:
                # Waiting for a click reaction from the user
                reaction, _ = await self.bot.wait_for("reaction_add", timeout=600.0, check=check)
            except asyncio.TimeoutError:
                return

            log_template.user_answer(ctx, str(reaction))

            # Switch page
            embed = pages.get(str(reaction))
            if embed:
                await help_msg.edit(embed=embed)

    @commands.command(name=command_names.function_command.turn_off_bot, help=help_text.turn_off_bot)
    @commands.is_owner()
    async def turn_off_bot(self, ctx: Context):
        """
        Command to logout the bot

        :param ctx: discord command context
        """
        await self.reporter.report_success_command(ctx)
        await self.bot.logout()

    @commands.command(name=command_names.function_command.author_of_bot, help=help_text.author_of_bot)
    async def author_of_bot(self, ctx: Context):
        """
        Command to send information about creator and bot as message in current channel

        :param ctx: discord command context
        """
        embed = discord.Embed(
            title=messages.author_title, colour=discord.Colour.blue(), description=messages.about_author
        )
        await ctx.send(embed=embed)
        await self.reporter.report_success_command(ctx)


def setup(bot: Bot):
    """
    Function to add base cog to the given bot

    :param bot: discord bot to add the cog
    """
    bot.add_cog(Base(bot))
    log_template.cog_launched("Base")
