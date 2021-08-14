"""
Contain classes for picking handlers for the specific reactions
"""
from typing import Any, Callable, Coroutine, Dict, List, NewType, Optional

from core.commands.raid.joining import join_raid_by_reaction, leave_raid_by_reaction
from core.commands.raid.settings import not_notify_me, notify_me
from core.commands.roles import add_role_from_reaction, remove_role_from_reaction
from core.database.manager import DatabaseManager
from core.models.context import ReactionContext
from core.users_interactor.message_reaction_interactor import MessagesReactions


class DynamicReactionsFactory:
    """
    Factory to produce reactions
    """

    __database = DatabaseManager()

    ReactionsFactoryMethod = NewType("ReactionsFactoryMethod",
                                     Callable[[ReactionContext], Coroutine[Any, Any, List[str]]])

    @classmethod
    async def get_reactions_to_role_action(cls, ctx: ReactionContext) -> ReactionsFactoryMethod:
        """
        Return reactions to role action from the database

        :param ctx: discord reaction context
        :return: list of reactions
        """
        if ctx.guild:
            return await cls.__database.settings.get_reactions_for_action_with_roles(ctx.guild.id) or []
        return []


class ReactionStrategy:
    """
    Responsible for providing method to handle the reaction that user adds or removes

    Provide handlers to call by the given reaction context and reaction from the static and dynamic maps.
    Static reactions maps contain reactions and handlers that can't be changed via commands.
    Dynamic reactions maps contain reactions and handlers that can be changed via commands.
    To add new reaction strategy, need to update static or dynamic map.
    """

    Handler = Callable[[Any], Coroutine[Any, Any, Any]]
    StaticReactionsMap = NewType("StaticReactionsMap", Dict[str, List[Handler]])
    DynamicReactionsMap = NewType("DynamicReactionsMap", Dict[DynamicReactionsFactory.ReactionsFactoryMethod, Handler])
    ReactionMap = Dict[str, List[Handler]]

    __static_add_reaction_map: StaticReactionsMap = {
        MessagesReactions.COLLECTION_EMOJI: [join_raid_by_reaction],
        MessagesReactions.NOTIFICATION_CONTROLLER_EMOJI: [not_notify_me],
    }
    __static_remove_reaction_map: StaticReactionsMap = {
        MessagesReactions.COLLECTION_EMOJI: [leave_raid_by_reaction],
        MessagesReactions.NOTIFICATION_CONTROLLER_EMOJI: [notify_me],
    }

    __dynamic_add_reaction_map: DynamicReactionsMap = {
        DynamicReactionsFactory.get_reactions_to_role_action: add_role_from_reaction,
    }
    __dynamic_remove_reaction_map: DynamicReactionsMap = {
        DynamicReactionsFactory.get_reactions_to_role_action: remove_role_from_reaction,
    }

    @classmethod
    async def get_add_reaction_handlers(cls, ctx: ReactionContext) -> Optional[List[Handler]]:
        """
        Gets add reaction handlers for the specific guild and reaction from the given reaction context

        :param ctx: discord reaction context
        :return: list of add reaction handlers to call
        """
        reaction_map = await cls.__get_add_reaction_map(ctx)
        return reaction_map.get(ctx.reaction)

    @classmethod
    async def get_remove_reaction_handlers(cls, ctx: ReactionContext) -> Optional[List[Handler]]:
        """
        Gets remove reaction handlers for the specific guild and reaction from the given reaction context

        :param ctx: discord reaction context
        :return: list of remove reaction handlers to call
        """
        reaction_map = await cls.__get_remove_reaction_map(ctx)
        return reaction_map.get(ctx.reaction)

    @classmethod
    async def __get_add_reaction_map(cls, ctx: ReactionContext) -> ReactionMap:
        """
        Return map with reaction and their add reaction handlers

        :param ctx: discord reaction context
        :return: map with reaction and their add reaction handlers
        """
        dynamic_add_reaction_map = await cls.__produce_dynamic_map(ctx, cls.__dynamic_add_reaction_map)
        return cls.__union_maps(cls.__static_add_reaction_map, dynamic_add_reaction_map)

    @classmethod
    async def __get_remove_reaction_map(cls, ctx: ReactionContext) -> ReactionMap:
        """
        Return map with reaction and their remove reaction handlers

        :param ctx: discord reaction context
        :return: map with reaction and their remove reaction handlers
        """
        dynamic_remove_reaction_map = await cls.__produce_dynamic_map(ctx, cls.__dynamic_remove_reaction_map)
        return cls.__union_maps(cls.__static_remove_reaction_map, dynamic_remove_reaction_map)

    @classmethod
    def __union_maps(cls, *reaction_maps: ReactionMap) -> ReactionMap:
        """
        Union given reaction maps to the one

        :param reaction_maps: list of reaction maps to union
        :return: united maps
        """
        united_map: cls.ReactionMap = {}
        for reaction_map in reaction_maps:
            for reactions, handler in reaction_map.items():
                for reaction in reactions:
                    handlers = united_map.get(reaction)
                    if handlers:
                        handlers.extend(handler)
                    else:
                        united_map[reaction] = handler
        return united_map

    @classmethod
    async def __produce_dynamic_map(cls, ctx: ReactionContext,
                                    dynamic_reaction_map: DynamicReactionsMap) -> ReactionMap:
        """
        Call factory methods from the dynamic reaction map and produce reaction map

        :param ctx: discord reaction context
        :param dynamic_reaction_map: reaction map with the method to produce roles and their handlers
        :return: reaction map from the dynamic reaction map
        """
        reactions_map: cls.ReactionMap = {}
        for reactions_source, handler in dynamic_reaction_map.items():
            reactions: List[str] = await reactions_source(ctx)
            for reaction in reactions:
                if handlers := reactions_map.get(reaction):
                    handlers.append(handler)
                else:
                    reactions_map[reaction] = [handler]
        return reactions_map
