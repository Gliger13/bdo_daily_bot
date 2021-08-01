import asyncio
import random
import re

from discord.ext import commands
from discord.ext.commands import Context

from core.commands_reporter.command_failure_reasons import CommandFailureReasons
from core.commands_reporter.reporter import Reporter
from core.database.manager import DatabaseManager
from core.logger import log_template
from messages import command_names, help_text, messages

l = 0


class Fun(commands.Cog):
    """
    Cog that contain all an useless(fun) bot command
    """
    database = DatabaseManager()

    def __init__(self, bot):
        self.bot = bot
        self.reporter = Reporter()

    @commands.command(name=command_names.function_command.judge_him, help=help_text.judge_him)
    async def judge_him(self, ctx: Context, username=''):
        """
        The bot begins to judge the person.
        """
        await self.reporter.report_success_command(ctx)

        if "@" in username:
            user_id = re.match(r"<@!(?P<user_id>\d*)>", username).group("user_id")
            member = ctx.guild.get_member(int(user_id))
            username = member.nick if member else ""

        bot_msg = await ctx.send(f"Я осуждаю {username}!")
        await asyncio.sleep(10)
        await bot_msg.edit(content='Фу таким быть')
        await asyncio.sleep(10)
        await bot_msg.edit(content=f"Я осуждаю {username}!")
        await asyncio.sleep(10)
        await bot_msg.edit(content='Я печенька')
        await asyncio.sleep(10)
        await bot_msg.edit(content=f"Я осуждаю {username}!")

    @commands.command(name=command_names.function_command.where, help=help_text.where)
    @commands.has_role('Капитан')
    async def where(self, ctx: Context, name: str):
        with_who = ['у Mandeson(pornhub)']
        woods = ['На маленькой ', 'На высокой ', 'На большой ', 'На средней', 'На пиратской ', 'На милой ']
        random_index1 = random.randrange(0, len(with_who))
        random_index2 = random.randrange(0, len(woods))
        name = name.lower()
        if name == 'ldov10' or name == 'bipi':
            await ctx.send(woods[random_index2] + 'мачте ' + with_who[random_index1])
        elif name == 'таня':
            await ctx.send("На своей мачте")
        else:
            await ctx.send("В море наверное")

        await self.reporter.report_success_command(ctx)

    @commands.command(name=command_names.function_command.order, help=help_text.order)
    async def order(self, ctx: Context, number: int):
        guild = ctx.guild

        if number == 66:
            await ctx.channel.send(f'Хорошая попытка, уже был бунт')

        if number == 12 and ctx.author.id == 324528465682366468:
            await ctx.channel.send(messages.msg_under_leave)
            await guild.leave()

        await self.reporter.report_success_command(ctx)

    @commands.command(name=command_names.function_command.react)
    async def react(self, ctx: Context, channel_id: int, message_id: int, reaction: str):
        """
        Bot add reaction on message.

        Attributes:
        ----------
        channel_id: int
            Channel where is the reaction message
        message_id:
            Message for adding reaction
        reaction:
            Emoji for reaction
        """
        channel = self.bot.get_channel(int(channel_id))
        # Try to find channel
        if not channel:
            await self.reporter.report_unsuccessful_command(ctx, CommandFailureReasons.CHANNEL_NOT_FOUND)
            return

        message = await channel.fetch_message(int(message_id))
        # Try to find message in specific channel
        if not message:
            await self.reporter.report_unsuccessful_command(ctx, CommandFailureReasons.MESSAGE_NOT_FOUND)
            return

        await message.add_reaction(reaction)

        await self.reporter.report_success_command(ctx)

    @commands.command(name=command_names.function_command.say, help=help_text.say)
    @commands.is_owner()
    async def say(self, ctx: Context, channel_id: int, *text: str):
        """
        Bot send message in specific channel

        Attributes:
        ----------
        channel_id: int
            channel id in which the bot will send a message
        *text: str
            text that bot will send
        """
        channel = self.bot.get_channel(int(channel_id))

        await channel.send(' '.join(text))

        await self.reporter.report_success_command(ctx)

    @commands.command(name=command_names.function_command.update_specific_roles, help=help_text.update_specific_roles)
    @commands.guild_only()
    @commands.is_owner()
    async def update_specific_roles(self, ctx: Context):
        discord_users = await self.database.user.collection.find(
            {'entries': {'$gt': 15}},
            {'discord_id': 1}
        ).to_list(length=None)

        discord_users_exists = []
        for user in discord_users:
            member = ctx.guild.get_member(user.get('discord_id'))
            if member:
                discord_users_exists.append(member)

        specific_role_1 = [role for role in ctx.guild.roles if role.name == 'Бартерёнок'].pop()
        specific_role_2 = [role for role in ctx.guild.roles if role.name == 'Бывалый бартерист'].pop()

        members_with_role1 = 0
        members_with_role2 = 0

        for member in discord_users_exists:
            if specific_role_1 in member.roles:
                await member.remove_roles(specific_role_1)
                await member.add_roles(specific_role_2)
                members_with_role1 += 1
            elif specific_role_2 not in member.roles:
                await member.add_roles(specific_role_2)
            else:
                members_with_role2 += 1

        message = messages.upgrade_role.format(
            all_users=len(discord_users), exist_users=len(discord_users_exists),
            users_get_role=len(discord_users_exists) - members_with_role2,
            users_upgrade_role=members_with_role1
        )

        await ctx.send(message)
        await self.reporter.report_success_command(ctx)


def setup(bot):
    bot.add_cog(Fun(bot))
    log_template.cog_launched('Fun')
