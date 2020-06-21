import asyncio
import logging

from discord.ext import commands

from instruments import database_process, help_messages

module_logger = logging.getLogger('my_bot')


class Admin(commands.Cog):
    database = database_process.DatabaseManager()

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='удалять_тут', help=help_messages.remove_there)
    @commands.has_permissions(administrator=True, manage_messages=True)
    async def del_there(self, ctx: commands.context.Context):
        guild = ctx.guild
        channel = ctx.channel
        self.database.settings.update_settings(guild.id, str(guild), channel.id, str(channel))
        await ctx.message.add_reaction('✔')
        await asyncio.sleep(10)
        await ctx.message.delete()

    @commands.command(name='очисти_чат', help=help_messages.remove_msgs)
    @commands.has_role('Капитан')
    async def remove_msgs(self, ctx: commands.context.Context, amount=100):
        guild = ctx.guild
        channel = ctx.channel
        if self.database.settings.can_delete_there(guild.id, channel.id):
            messages = []
            async for msg in channel.history(limit=int(amount)):
                if not msg.pinned:
                    messages.append(msg)
            await channel.delete_messages(messages)
            module_logger.info(f'{ctx.author} успешно ввёл команду {ctx.message.content}')
        else:
            await ctx.message.add_reaction('❌')
            module_logger.info(f'{ctx.author} ввёл команду {ctx.message.content}. Плохой канал')

    @commands.command(name='не_удалять', help=help_messages.not_remove_there)
    @commands.has_permissions(administrator=True, manage_messages=True)
    async def not_remove_there(self, ctx: commands.context.Context):
        guild = ctx.guild
        channel = ctx.channel
        self.database.settings.not_delete_there(guild.id, channel.id)
        await ctx.message.add_reaction('✔')


def setup(bot):
    bot.add_cog(Admin(bot))
    module_logger.debug('Успешный запуск bot.admin')
