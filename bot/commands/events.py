"""
Module contain discord cog with name `Events`. Provide discord listeners.
"""
import logging
import sys
import traceback

from discord import DiscordException, Game, Member, Message, RawReactionActionEvent, Status, TextChannel
from discord.ext import commands
from discord.ext.commands import Bot, Context

from bot import BdoDailyBot
from core.commands_reporter.reporter import Reporter
from core.database.manager import DatabaseManager
from core.guild_managers.managers_controller import ManagersController
from core.guild_security.guild_security_manager import GuildSecurityManager
from core.logger import log_template
from core.models.context_factory import ReactionContextFactory
from core.models.reaction_strategy import ReactionStrategy
from messages import logger_msgs, messages
from settings import settings


class Events(commands.Cog):
    """
    Cog that responsible for various events.
    """
    database = DatabaseManager()

    def __init__(self, bot: Bot):
        """
        :param bot: discord bot for executing the cog commands
        """
        self.bot = bot
        self.reporter = Reporter()
        # Needed to track unplanned bot reboots
        self.is_bot_ready = False

    @commands.Cog.listener()
    async def on_member_join(self, member: Member):
        """
        Listener sends hello message to the new server member

        Listener trigger where new member join server. Sends hello message to the new member.

        :param member: discord member which join server
        """
        # Send only for new users in the main guild
        if member.guild.id == settings.MAIN_GUILD_ID:
            await member.send(messages.hello_new_member)

    @commands.Cog.listener()
    async def on_ready(self):
        """
        Listener to set bot main configuration

        Listener trigger after bot will ready to process commands. Sets bot main configuration such
        as status and current game. Loads still active raids from the database.
        """
        # Set custom status
        custom_status = 'Разрушаюсь и перестраиваюсь'
        await self.bot.change_presence(status=Status.online, activity=Game(custom_status))

        BdoDailyBot.bot = self.bot
        # Track unplanned bot reboot
        if not self.is_bot_ready:
            self.is_bot_ready = True
            logging.info(logger_msgs.bot_ready)
            await ManagersController.load_managers()
            await ManagersController.load_raids()
            logging.debug("Bot initialization completed.")
        else:
            log_template.bot_restarted()

    @commands.Cog.listener()
    async def on_command_error(self, ctx: Context, error: DiscordException):
        """
        Listener to handle and process all errors

        :param ctx: discord command context
        :param error: discord exception to handle
        """
        if isinstance(error, commands.errors.BadArgument):
            await ctx.message.add_reaction('❔')
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.message.add_reaction('❔')
        elif isinstance(error, commands.errors.CommandNotFound):
            await ctx.message.add_reaction('❓')
        elif isinstance(error, commands.errors.PrivateMessageOnly):
            await ctx.message.author.send(messages.private_msg_only)
            await ctx.message.add_reaction('❓')
        elif isinstance(error, commands.errors.NoPrivateMessage):
            await ctx.message.author.send(messages.no_private_msg)
            await ctx.message.add_reaction('❓')
        elif isinstance(error, commands.errors.BotMissingPermissions):
            await ctx.message.author.send(messages.missing_perms.format(missing_perms='.'.join(error.missing_perms)))
            await ctx.message.add_reaction('❓')
        elif isinstance(error, commands.errors.UserInputError):
            await ctx.message.add_reaction('❓')
        elif isinstance(error, commands.errors.MissingRole):
            await ctx.message.add_reaction('⛔')
        else:
            # If this is an unknown error
            log_template.unknown_command_error(ctx, error)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
            return
        log_template.command_error(ctx, error)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: RawReactionActionEvent):
        """
        Listener to handle all added reaction by discord member

        :param payload: discord raw reaction action event payload
        """
        if payload.user_id == settings.BOT_ID:
            return

        ctx = await ReactionContextFactory.produce_by_raw_reaction_event(payload)
        if handlers := await ReactionStrategy.get_add_reaction_handlers(ctx):
            for handler in handlers:
                await handler(ctx)
            return
        channel_name = ctx.channel.name if isinstance(ctx.channel, TextChannel) else ctx.channel
        logging.debug("{}/{}/{}/{} No handler for reaction `{}`".format(
            ctx.guild, channel_name, ctx.author.name, ctx.command.name, ctx.reaction))

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: RawReactionActionEvent):
        """
        Listener to handle all removed reactions by discord member

        :param payload: discord raw reaction action event payload
        """
        if payload.user_id == settings.BOT_ID:
            return

        ctx = await ReactionContextFactory.produce_by_raw_reaction_event(payload)
        if handlers := await ReactionStrategy.get_remove_reaction_handlers(ctx):
            for handler in handlers:
                await handler(ctx)
            return
        channel_name = ctx.channel.name if isinstance(ctx.channel, TextChannel) else ctx.channel
        logging.debug("{}/{}/{}/{} No handler for reaction `{}`".format(
            ctx.guild, channel_name, ctx.author.name, ctx.command.name, ctx.reaction))

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        """
        Listen all created and sent messages

        :param message: income message
        """
        if message.author.id != settings.BOT_ID:
            await GuildSecurityManager.invoke_message_spam_checker(message)


def setup(bot: Bot):
    """
    Function to add events cog to the given bot

    :param bot: discord bot to add the cog
    """
    bot.add_cog(Events(bot))
    log_template.cog_launched('Events')
