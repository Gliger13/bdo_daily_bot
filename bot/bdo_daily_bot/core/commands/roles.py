"""
Contain core commands logic for roles interaction
"""
import logging

import discord

from bdo_daily_bot.core.commands.common import command_logging
from bdo_daily_bot.core.database.manager import DatabaseManager
from bdo_daily_bot.core.logger import log_template
from bdo_daily_bot.core.models.context import ReactionContext

__database = DatabaseManager()


@command_logging
async def add_role_from_reaction(ctx: ReactionContext):
    """
    Give user a role by clicking reaction on message

    Gets guild settings from database and checks if the emoji from given payload in the
    role from reaction section. If it in, then gives user the role according to the reaction
    he clicked.

    :param ctx: discord reaction context
    :return: True if command success else False
    """
    guild_settings = await __database.settings.find_settings_post(ctx.guild.id)
    if not guild_settings:
        logging.info("No guild settings for guild: `{}`".format(ctx.guild.id))
        return

    role_from_reaction = guild_settings.get("role_from_reaction")
    if not role_from_reaction:
        logging.info("No role_from_reaction settings for guild: `{}`".format(ctx.guild.id))
        return

    reaction_role = role_from_reaction.get(str(ctx.message.id))
    if reaction_role and ctx.reaction in reaction_role:
        role = discord.utils.get(ctx.guild.roles, id=reaction_role.get(ctx.reaction))
        member = ctx.guild.get_member(ctx.author.id)
        await member.add_roles(role)
        log_template.role_add_from_reaction(ctx.guild, ctx.author, role, ctx.reaction)
        return True


@command_logging
async def remove_role_from_reaction(ctx: ReactionContext):
    """
    Remove from user a role by clicking reaction on message

    Gets guild settings from database and checks if the emoji from given payload in the
    role from reaction section. If it in, then remove from user the role according to the reaction
    he clicked.

    :param ctx: discord reaction context
    :return: True if command success else False
    """
    guild_settings = await __database.settings.find_settings_post(ctx.guild.id)
    if not guild_settings:
        return

    role_from_reaction = guild_settings.get("role_from_reaction")

    if not role_from_reaction:
        return

    reaction_role = role_from_reaction.get(str(ctx.message.id))
    if reaction_role and ctx.reaction in reaction_role:
        member = ctx.guild.get_member(ctx.author.id)
        role = discord.utils.get(ctx.guild.roles, id=reaction_role.get(ctx.reaction))
        await member.remove_roles(role)
        log_template.role_remove_from_reaction(ctx.guild, member, role, ctx.reaction)
        return True
