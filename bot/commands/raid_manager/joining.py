import logging

from discord.ext import commands

from commands.raid_manager import raid_list
from instruments import check_input, database_process
from messages import command_names, help_text, messages
from settings import settings

module_logger = logging.getLogger('my_bot')


class RaidJoining(commands.Cog):
    database = database_process.DatabaseManager()
    raid_list = raid_list.RaidList()

    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def update_info(curr_raid):
        # Rewrite!!!!!!!!!!!!!!!
        old_text = curr_raid.collection_msg.content
        edited_text = f"Мест осталось {curr_raid.places_left}.\n"
        start_index = old_text.find('Мест осталось')
        end_index = old_text.find('Обновлённая')
        new_text_msg = old_text[:start_index] + edited_text + old_text[end_index:]
        await curr_raid.collection_msg.edit(content=new_text_msg)

    async def raid_reaction_add(self, collection_msg, emoji, user):
        if str(emoji) == '❤' and not user.id == settings.BOT_ID:  # Ignore bot action
            for curr_raid in self.raid_list:
                if (curr_raid.collection_msg and curr_raid.collection_msg.id == collection_msg.id and
                        curr_raid.guild_id == collection_msg.guild.id):
                    nickname = self.database.user.find_user(str(user))
                    if nickname:  # if find user in data base
                        if curr_raid.member_dict.get(nickname):
                            await user.send(messages.no_registration)
                            module_logger.info(f'{user} не смог попасть в рейд к кэпу. Уже есть в рейде')
                            break
                        else:
                            if curr_raid.places_left != 0:
                                msg_success = messages.raid_joined.format(
                                    captain_name=curr_raid.captain_name, server=curr_raid.server,
                                    time_leaving=curr_raid.raid_time.time_leaving,
                                )
                                curr_raid += str(nickname)
                                self.database.user.user_joined_raid(str(user))
                                module_logger.info(f'{user} попал в рейд к кэпу {curr_raid.captain_name}')
                                await user.send(msg_success)
                                await RaidJoining.update_info(curr_raid)
                                break
                            else:
                                msg_no_space = messages.raid_not_joined
                                module_logger.info(f'{user} не попал в рейд к кэпу {curr_raid.captain_name}. Нет мест')
                                await user.send(msg_no_space)
                                break
                    else:
                        module_logger.info(f'{user} не попал в рейд. Нет регистрации')
                        await user.send(messages.already_in_raid)
                        break

    async def raid_reaction_remove(self, collection_msg, emoji, user):
        if str(emoji) == '❤':
            for curr_raid in self.raid_list.active_raids:
                if (curr_raid.collection_msg and curr_raid.collection_msg.id == collection_msg.id
                        and curr_raid.guild_id == collection_msg.guild.id):
                    nickname = self.database.user.find_user(str(user))
                    if nickname:
                        if curr_raid.member_dict.get(nickname):
                            curr_raid -= str(nickname)
                            self.database.user.user_leave_raid(str(user))
                            module_logger.info(f'{user} убрал себя из рейда кэпа {curr_raid.captain_name}')
                            await user.send(messages.raid_leave.format(captain_name=curr_raid.captain_name))
                            await RaidJoining.update_info(curr_raid)
                            break

    @commands.command(name=command_names.function_command.reserve, help=help_text.reserve)
    @commands.has_role('Капитан')
    async def reserve(self, ctx: commands.context.Context, name: str, captain_name='', time_leaving=''):
        # Checking correct input
        await check_input.validation(**locals())

        curr_raid = self.raid_list.find_raid(ctx.guild.id, ctx.channel.id, captain_name, time_leaving)
        if curr_raid and not curr_raid.places_left == 0:
            if curr_raid.member_dict.get(name):
                module_logger.info(f'{ctx.author} неудачно использовал команду {ctx.message.content}. Есть в рейде')
                await ctx.message.add_reaction('❌')
                return
            curr_raid += name
            module_logger.info(f'{ctx.author} успешно использовал команду {ctx.message.content}')
            await RaidJoining.update_info(curr_raid)
            await ctx.message.add_reaction('✔')
        else:
            guild_raid_list = []
            for curr_raid in self.raid_list:
                if curr_raid.guild_id == ctx.message.guild.id and not curr_raid.member_dict.get(name):
                    guild_raid_list.append(curr_raid)
                    break
            if not guild_raid_list:  # If list empty
                module_logger.info(f'{ctx.author} неудачно использовал команду {ctx.message.content}. Нет рейдов')
                await ctx.message.add_reaction('❌')
                return
            smaller_raid = min(guild_raid_list)
            smaller_raid += name
            module_logger.info(f'{ctx.author} успешно использовал команду {ctx.message.content}')
            await ctx.message.add_reaction('✔')

    @commands.command(name=command_names.function_command.remove_res, help=help_text.remove_res)
    @commands.has_role('Капитан')
    async def remove_res(self, ctx: commands.context.Context, name: str):
        # Checking correct inputs arguments
        await check_input.validation(**locals())

        for finding_raid in self.raid_list:
            finding_raid -= name
            if finding_raid:
                module_logger.info(f'{ctx.author} успешно использовал команду {ctx.message.content}')
                await RaidJoining.update_info(finding_raid)
                await ctx.message.add_reaction('✔')
                break
        else:
            module_logger.info(f'{ctx.author} неудачно использовал команду {ctx.message.content}. Нету в рейдах')
            await ctx.message.add_reaction('❌')


def setup(bot):
    bot.add_cog(RaidJoining(bot))
    module_logger.debug(f'Успешный запуск bot.raid_manager.joining')
