import logging

from discord.ext import commands

from commands.raid_manager import common
from instruments import messages, check_input

module_logger = logging.getLogger('my_bot')


class RaidRegistration(commands.Cog):
    database = common.Database().database('discord')
    collection_users = database['user_nicknames']
    raid_list = common.Raids.active_raids

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='рег', help=messages.help_msg_reg)
    async def reg(self, ctx: commands.context.Context, name: str):
        # Checking correct input
        await check_input.validation(**locals())

        # Try to find user in BD
        old_post = RaidRegistration.collection_users.find_one({"discord_user": str(ctx.author)})
        if not old_post:  # If not find...
            post = {'discord_user': str(ctx.author), 'nickname': str(name), 'entries': 0}
            RaidRegistration.collection_users.insert_one(post)
            module_logger.info(f'{ctx.author} успешно использовал команду {ctx.message.content}')
            await ctx.message.add_reaction('✔')
        else:
            module_logger.info(f'{ctx.author} неудачно использовал команду {ctx.message.content}. Уже есть в БД')
            await ctx.author.send("Ты уже зарегистрировался, хватит использовать эту команду."
                                  " Сейчас тапком в тебя кину! :sandal:. Иди и нажми на милое сердечко :heart:!")
            await ctx.message.add_reaction('❌')

    @commands.command(name='перерег', help=messages.help_msg_rereg)
    async def rereg(self, ctx: commands.context.Context, name: str):
        # Checking correct input
        await check_input.validation(**locals())
        # Try to find user in BD
        old_post = RaidRegistration.collection_users.find_one({"discord_user": str(ctx.author)})
        if old_post:  # If not find...
            post = {'discord_user': str(ctx.author), 'nickname': str(name), 'entries': int(old_post['entries'])}
            RaidRegistration.collection_users.update(old_post, post)
            module_logger.info(f'{ctx.author} успешно использовал команду {ctx.message.content}')
            await ctx.message.add_reaction('✔')
        else:
            await self.reg(ctx, name)


def setup(bot):
    bot.add_cog(RaidRegistration(bot))
    module_logger.debug(f'Успешный запуск bot.raid_manager.registration')
