"""Contain factory to produce different project paths"""
import os
from importlib.resources import files


class ProjectFileMapping:
    """Contain main directory names"""

    ROOT_DIR_NAME = "bdo_daily_bot"
    COMMANDS_DIR_NAME = "commands_v2"
    COMMAND_COGS_PATH = f"{ROOT_DIR_NAME}.{COMMANDS_DIR_NAME}"

    LOCALIZATION_PATH = "bdo_daily_bot.config.localization.data"
    LOCALIZED_COMMANDS_MAP = "commands.yaml"
    LOCALIZED_MESSAGES_MAP = "messages.yaml"
    LOCALIZED_VALIDATIONS_MAP = "validations.yaml"

    BOT_DATA_DIR_NAME = "bot_data"
    EXCLUDE_DIRS_FROM_SEARCH = {"venv", ".idea", "__pycache__"}
    LOGS_FILE_NAME = "logs.log"
    INIT_FILE_NAME = "__init__.py"


class ProjectPathFactory:
    """Generate different project paths."""

    @classmethod
    def get_all_cog_paths(cls) -> list[str]:
        """Get all configured discord cogs with extensions paths.

        :return: all configured discord cogs with extensions paths
        """
        discord_cogs_paths: list[str] = []
        project_root_path = str(files(ProjectFileMapping.ROOT_DIR_NAME))
        commands_dir_path = str(files(ProjectFileMapping.COMMAND_COGS_PATH))
        for file_path in cls._get_module_paths(commands_dir_path):
            relative_cog_path = os.path.relpath(file_path, os.path.dirname(project_root_path))
            split_path = os.path.normpath(relative_cog_path).split(os.sep)
            discord_cogs_paths.append(".".join(split_path)[:-3])
        return discord_cogs_paths

    @classmethod
    def get_bot_data_dir_path(cls) -> str:
        """Get path to the directory for the bot data.

        Get path to the directory for the bot data. If it does not exist, then
        create a new directory for it.

        :return: path to the directory for the bot data.
        """
        bot_data_dir_path = str(files(ProjectFileMapping.ROOT_DIR_NAME).joinpath(ProjectFileMapping.BOT_DATA_DIR_NAME))
        if not os.path.exists(bot_data_dir_path):
            os.mkdir(bot_data_dir_path)
        return bot_data_dir_path

    @classmethod
    def get_logs_path(cls) -> str:
        """Get absolute path to the log file."""
        return os.path.join(cls.get_bot_data_dir_path(), ProjectFileMapping.LOGS_FILE_NAME)

    @classmethod
    def _get_module_paths(cls, dir_path: str) -> list[str]:
        """Get list of python module paths from specific directory.

        :param dir_path: directory path to search in it.
        :return: list of paths to the python modules
        """
        file_paths: list[str] = []
        for root_path, _, filenames in os.walk(dir_path, topdown=True):
            for filename in filenames:
                if filename.endswith(".py") and filename != ProjectFileMapping.INIT_FILE_NAME:
                    file_paths.append(os.path.join(root_path, filename))
        return file_paths
