"""
Contains variable with commands fails reasons
"""
from enum import Enum


class CommandFailureReasons(Enum):
    """
    Contains the reasons for the failed commands.
    """

    CAPTAIN_NOT_EXIST = "captain_not_exist"
    RAID_NOT_FOUND = "raid_not_found"
    RAID_EXIST = "raid_exist"
    USER_NOT_RESPONSE = "user_not_response"
    NO_AVAILABLE_RAIDS = "no_available_raids"
    RAID_IS_FULL = "raid_is_full"
    ALREADY_IN_RAID = "already_in_raid"
    ALREADY_IN_SAME_RAID = "already_in_same_raid"
    USER_NOT_FOUND_IN_RAID = "user_not_found_in_raid"
    NO_AVAILABLE_TO_CLOSE_RESERVATION = "no_available_to_close_reservation"
    NOT_CAPTAIN = "not_captain"
    VALIDATION_ERROR = "validation_error"
    NO_ACTIVE_RAIDS = "no_active_raids"
    ALREADY_REGISTERED = "already_registered"
    WRONG_CHANNEL_TO_DELETE_IN = "wrong_channel_to_delete_in"
    ROLES_NOT_EXIST = "roles_not_exist"
    REMOVE_REACTION_FAILURE = "remove_reaction_failure"
    COMMAND_NOT_FOUND = "command_not_found"
    LOGS_NOT_FOUND = "logs_not_found"
    CHANNEL_NOT_FOUND = "channel_not_found"
    MESSAGE_NOT_FOUND = "message_not_found"
