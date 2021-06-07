"""Contain function to get different project paths"""
import os
from functools import lru_cache
from typing import Optional, List


class ProjectFileMapping:
    """Contain main directory names"""

    ROOT_DIR_NAME = "bdo_daily_bot"
    COMMANDS_DIR_NAME = "commands"
    BOT_DATA_DIR_NAME = "bot_data"
    EXCLUDE_DIRS_FROM_SEARCH = {"venv", ".idea", "__pycache__"}


class ProjectPathFactory:
    """Provide different project paths"""

    @classmethod
    def get_root_dir_path(cls) -> str:
        """
        Gets abs path of the root project directory

        :return: abs path of the root project directory
        """
        current_directory_path = os.path.dirname(__file__)
        while os.path.basename(current_directory_path) != ProjectFileMapping.ROOT_DIR_NAME:
            current_directory_path = os.path.dirname(current_directory_path)
        return current_directory_path

    @classmethod
    @lru_cache
    def __get_dir_path_in_project_by_name(cls, dirname: str) -> Optional[str]:
        """
        Gets directory path in current project by it's name

        :param dirname: directory name in project files
        :return: directory path
        """
        for root_path, dirs, filenames in os.walk(cls.get_root_dir_path(), topdown=True):
            dirs[:] = [directory for directory in dirs if directory not in ProjectFileMapping.EXCLUDE_DIRS_FROM_SEARCH]
            if dirname in dirs:
                return os.path.join(root_path, dirname)

    @classmethod
    def get_bot_data_dir_path(cls) -> Optional[str]:
        """
        Gets path of the bot data directory

        :return: bot data directory path
        """
        return cls.__get_dir_path_in_project_by_name(ProjectFileMapping.BOT_DATA_DIR_NAME)

    @classmethod
    def get_commands_dir_path(cls) -> Optional[str]:
        """
        Gets path of the commands directory

        :return: commands directory path
        """
        return cls.__get_dir_path_in_project_by_name(ProjectFileMapping.COMMANDS_DIR_NAME)

    @classmethod
    def get_all_py_file_paths_from_dir(cls, dir_path: str) -> List[str]:
        """
        Gets lists of file paths from specific directory

        :param dir_path: directory path to search in it
        :return: list of file names
        """
        file_paths = []
        for root_path, _, filenames in os.walk(dir_path, topdown=True):
            for filename in filenames:
                if filename.endswith(".py") and filename != "__init__.py":
                    file_paths.append(os.path.join(root_path, filename))
        return file_paths

    @classmethod
    def get_all_cogs_with_extensions(cls) -> List[Optional[str]]:
        """
        Gets all discord cogs with extensions paths

        :return: all discord cogs with extensions paths
        """
        discord_cogs_paths = []
        for file_path in cls.get_all_py_file_paths_from_dir(cls.get_commands_dir_path()):
            relative_cog_path = os.path.relpath(file_path, os.path.dirname(cls.get_commands_dir_path()))
            split_path = os.path.normpath(relative_cog_path).split(os.sep)
            discord_cogs_paths.append(".".join(split_path)[:-3])
        return discord_cogs_paths
