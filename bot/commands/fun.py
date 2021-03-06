import asyncio
import logging
import random

from discord.ext import commands
from discord.ext.commands import Context

from messages import command_names, help_text, messages
from settings.logger import log_template

module_logger = logging.getLogger('my_bot')


class Fun(commands.Cog):
    """
    Cog that contain all an useless(fun) bot command
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name=command_names.function_command.judge_him, help=help_text.judge_him)
    async def judge_him(self, ctx: Context, username=''):
        """
        The bot begins to judge the person.
        """
        log_template.command_success(ctx)

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
        log_template.command_success(ctx)

    @commands.command(name=command_names.function_command.order, help=help_text.order)
    async def order(self, ctx: Context, number: int):
        guild = ctx.guild

        if number == 66:
            await ctx.channel.send(f'Хорошая попытка, уже был бунт')

        if number == 12 and ctx.author.id == 324528465682366468:
            await ctx.channel.send(messages.msg_under_leave)
            await guild.leave()

        log_template.command_success(ctx)

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
            await ctx.message.add_reaction('❌')
            return

        message = await channel.fetch_message(int(message_id))
        # Try to find message in specific channel
        if not message:
            await ctx.message.add_reaction('❌')
            return

        await message.add_reaction(reaction)
        await ctx.message.add_reaction('✔')
        log_template.command_success(ctx)

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
        log_template.command_success(ctx)


def setup(bot):
    bot.add_cog(Fun(bot))
    log_template.cog_launched('Fun')
