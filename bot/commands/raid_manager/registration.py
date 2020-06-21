import logging

from discord.ext import commands

from commands.raid_manager import common
from instruments import help_messages, check_input, database_process

module_logger = logging.getLogger('my_bot')


class RaidRegistration(commands.Cog):
    database = database_process.DatabaseManager()
    raid_list = common.Raids.active_raids

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='рег', help=help_messages.reg)
    async def reg(self, ctx: commands.context.Context, name: str):
        # Checking correct input
        await check_input.validation(**locals())

        try:
            self.database.user.reg_user(ctx.author.id, str(ctx.author), name)
            module_logger.info(f'{ctx.author} успешно использовал команду {ctx.message.content}')
            await ctx.message.add_reaction('✔')
        except database_process.UserExists:
            module_logger.info(f'{ctx.author} неудачно использовал команду {ctx.message.content}. Уже есть в БД')
            await ctx.author.send("Ты уже зарегистрировался, хватит использовать эту команду."
                                  " Сейчас тапком в тебя кину! :sandal:. Иди и нажми на милое сердечко :heart:!")
            await ctx.message.add_reaction('❌')

    @commands.command(name='перерег', help=help_messages.rereg)
    async def rereg(self, ctx: commands.context.Context, name: str):
        # Checking correct input
        await check_input.validation(**locals())

        self.database.user.rereg_user(ctx.author.id, str(ctx.author), name)

        module_logger.info(f'{ctx.author} успешно использовал команду {ctx.message.content}')
        await ctx.message.add_reaction('✔')


def setup(bot):
    bot.add_cog(RaidRegistration(bot))
    module_logger.debug(f'Успешный запуск bot.raid_manager.registration')
