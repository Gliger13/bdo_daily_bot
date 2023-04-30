"""Unit tests for the project path factory"""
import os.path

import pytest

from bdo_daily_bot.core.tools.path_factory import ProjectFileMapping
from bdo_daily_bot.core.tools.path_factory import ProjectPathFactory


@pytest.fixture(scope="session")
def project_path_factory() -> ProjectPathFactory:
    return ProjectPathFactory()


@pytest.fixture
def tmpdir_with_files(tmpdir: "LocalPath") -> "LocalPath":
    """Fixture that creates some test files with the .py extension in a temporary directory.

    :param tmpdir: temporary directory created by pytest.
    :return: the temporary directory with the test files.
    """
    file_1 = tmpdir.join("file1.py")
    file_1.write("")

    file_2 = tmpdir.join("file2.py")
    file_2.write("")

    tmpdir.join("file3.txt").write("")
    tmpdir.join("file4.png").write("")

    yield tmpdir

    file_1.remove()
    file_2.remove()
    tmpdir.join("file3.txt").remove()
    tmpdir.join("file4.png").remove()


def test_get_module_paths_returns_empty_list_for_nonexistent_directory(project_path_factory: ProjectPathFactory):
    """Test that the function returns an empty list if the directory doesn't exist.

    :param project_path_factory: initialized factory to test
    """
    assert (
        project_path_factory._get_module_paths("nonexistent_directory") == []
    ), "Check function returns an empty list if the directory doesn't exits"


def test_get_module_paths_returns_empty_list_for_empty_directory(
    project_path_factory: ProjectPathFactory, tmpdir: "LocalPath"
):
    """Test that the function returns an empty list if the directory doesn't contain any Python modules.

    :param project_path_factory: initialized factory to test
    :param tmpdir: Temporary directory created by pytest.
    """
    assert (
        project_path_factory._get_module_paths(tmpdir) == []
    ), "Check function returns an empty list if the directory doesn't contain any Python modules"


def test_get_module_paths_returns_list_of_module_paths(
    project_path_factory: ProjectPathFactory, tmpdir_with_files: "LocalPath"
):
    """Test that the function returns a list of module paths.

    :param project_path_factory: initialized factory to test
    :param tmpdir_with_files: Temporary directory created by pytest with test files.
    """
    module_paths = project_path_factory._get_module_paths(tmpdir_with_files)

    assert (
        len(module_paths) == 2
    ), "Check the function returns a list of two elements for the folder with two Python modules in it"
    assert (
        str(tmpdir_with_files.join("file1.py")) in module_paths
    ), "Check the function returns a list with the path to the first created Python module"
    assert (
        str(tmpdir_with_files.join("file2.py")) in module_paths
    ), "Check the function returns a list with the path to the second created Python module"


def test_get_module_paths_filters_out_non_python_files(
    project_path_factory: ProjectPathFactory, tmpdir_with_files: "LocalPath"
):
    """Test that the function filters out non-Python files in a directory.

    :param project_path_factory: initialized factory to test
    :param tmpdir_with_files: temporary directory created by pytest with test files.
    """
    module_paths = project_path_factory._get_module_paths(tmpdir_with_files)
    assert not any(
        file for file in module_paths if not file.endswith(".py")
    ), "Check the function returns only Python modules"


def test_get_module_paths_filters_out_init_files(project_path_factory: ProjectPathFactory, tmpdir: "LocalPath"):
    """Test that the function filters out __init__.py files in a directory.

    :param project_path_factory: initialized factory to test
    :param tmpdir: temporary directory created by pytest.
    """
    file_1 = tmpdir.join("file1.py")
    file_1.write("")

    file_2 = tmpdir.join("__init__.py")
    file_2.write("")

    module_paths = project_path_factory._get_module_paths(tmpdir)

    assert not any(
        file for file in module_paths if file.endswith("__init__.py")
    ), "Check the function doesn't return __init__.py file"


def test_get_bot_data_path(project_path_factory: ProjectPathFactory):
    """Test that the function creates and return actual path for bot data.

    :param project_path_factory: initialized factory to test
    """
    bot_data_dir_path = project_path_factory.get_bot_data_dir_path()

    assert os.path.abspath(bot_data_dir_path), "Check the function returns a valid path"
    assert os.path.exists(bot_data_dir_path), "Check bot data directory exists"

    if not any(os.scandir(bot_data_dir_path)):
        os.rmdir(bot_data_dir_path)


def test_get_log_file_path(project_path_factory: ProjectPathFactory):
    """Test that the function returns a valid path for the log file.

    :param project_path_factory: initialized factory to test
    """
    log_file_path = project_path_factory.get_logs_path()

    assert os.path.abspath(log_file_path), "Check the function returns a valid path"


def test_get_all_cog_paths(project_path_factory: ProjectPathFactory):
    all_cog_paths = project_path_factory.get_all_cog_paths()
    for path in all_cog_paths:
        is_valid_path = all(part.isidentifier() for part in path.split("."))
        assert is_valid_path, f"Check module path {path} is valid"
        assert path.startswith(ProjectFileMapping.ROOT_DIR_NAME), "Check the path starts with the project root dir name"
