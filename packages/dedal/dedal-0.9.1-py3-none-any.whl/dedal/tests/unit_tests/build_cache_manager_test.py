# Dedal library - Wrapper over Spack for building multiple target
# environments: ESD, Virtual Boxes, HPC compatible kernels, etc.

#  (c) Copyright 2025 Dedal developers

#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at

#      http://www.apache.org/licenses/LICENSE-2.0

#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import pytest
from _pytest.fixtures import fixture

from dedal.build_cache.BuildCacheManager import BuildCacheManager


class TestBuildCacheManager:

    @fixture(scope="function")
    def mock_build_cache_manager(self, mocker):
        mocker.patch("dedal.build_cache.BuildCacheManager.get_logger")
        return BuildCacheManager("TEST_HOST", "TEST_PROJECT", "TEST_USERNAME", "TEST_PASSWORD", "TEST_VERSION")

    def test_get_public_key_from_cache_success_path(self, mock_build_cache_manager, tmp_path):

        # Arrange
        build_cache_dir = tmp_path / "build_cache"
        pgp_folder = build_cache_dir / "project" / "_pgp"
        pgp_folder.mkdir(parents=True)
        key_file = pgp_folder / "key.pub"
        key_file.write_text("public key content")

        # Act
        result = mock_build_cache_manager.get_public_key_from_cache(str(build_cache_dir))

        # Assert
        assert result == str(key_file)

    @pytest.mark.parametrize("test_id, num_pgp_folders, num_key_files, expected_log_message", [
        ("more_than_one_gpg_folder", 2, 1,
         "More than one PGP folders found in the build cache: %s, using the first one in the list: %s"),
        ("more_than_one_key_file", 1, 2,
         "More than one PGP key files found in the build cache: %s, using the first one in the list: %s"),
    ])
    def test_get_public_key_from_cache_multiple_files_or_folders(self, mock_build_cache_manager, test_id,
                                                                 tmp_path, num_pgp_folders,
                                                                 num_key_files, expected_log_message):

        # Arrange
        pgp_folders = []
        key_files = []
        build_cache_dir = tmp_path / "build_cache"
        for i in range(num_pgp_folders):
            pgp_folder = build_cache_dir / f"project{i}" / "_pgp"
            pgp_folders.append(str(pgp_folder))
            pgp_folder.mkdir(parents=True)
            for j in range(num_key_files):
                key_file = pgp_folder / f"key{j}.pub"
                key_files.append(str(key_file))
                key_file.write_text(f"public key {j} content")

        # Act
        result = mock_build_cache_manager.get_public_key_from_cache(str(build_cache_dir))

        # Assert
        # Cannot assure the order in which the OS returns the files,
        # hence check if the result is in the expected list
        assert result in [str(build_cache_dir / "project0" / "_pgp" / "key0.pub"),
                          str(build_cache_dir / "project0" / "_pgp" / "key1.pub"),
                          str(build_cache_dir / "project1" / "_pgp" / "key0.pub")]
        assert mock_build_cache_manager._logger.warning.call_args[0][0] == expected_log_message
        assert set(mock_build_cache_manager._logger.warning.call_args[0][1]) == set(
            pgp_folders) if test_id == "more_than_one_gpg_folder" else set(key_files)
        assert mock_build_cache_manager._logger.warning.call_args[0][
                   2] in pgp_folders if test_id == "more_than_one_gpg_folder" else key_files

    @pytest.mark.parametrize("build_cache_dir, expected_log_message", [
        (None, 'Build cache directory does not exist!'),
        ("non_existent_dir", 'Build cache directory does not exist!'),
    ])
    def test_get_public_key_from_cache_no_build_cache(self, mock_build_cache_manager, build_cache_dir,
                                                      expected_log_message, tmp_path):

        # Arrange
        build_cache_dir = str(tmp_path / build_cache_dir) if build_cache_dir else None

        # Act
        result = mock_build_cache_manager.get_public_key_from_cache(build_cache_dir)

        # Assert
        assert result is None
        mock_build_cache_manager._logger.warning.assert_called_once_with(expected_log_message)

        # Assert
        assert result is None
        mock_build_cache_manager._logger.warning.assert_called_once_with(expected_log_message)

    @pytest.mark.parametrize("build_cache_dir, expected_log_message", [
        ("non_existent_dir", "No _pgp folder found in the build cache!"),
    ])
    def test_get_public_key_from_cache_no_pgp_folder(self, mock_build_cache_manager, build_cache_dir,
                                                     expected_log_message, tmp_path):

        # Arrange
        if build_cache_dir == "non_existent_dir":
            build_cache_dir = tmp_path / build_cache_dir
            build_cache_dir.mkdir(parents=True)

        # Act
        result = mock_build_cache_manager.get_public_key_from_cache(build_cache_dir)

        # Assert
        assert result is None
        mock_build_cache_manager._logger.warning.assert_called_once_with(expected_log_message)

        # Assert
        assert result is None
        mock_build_cache_manager._logger.warning.assert_called_once_with(expected_log_message)

    def test_get_public_key_from_cache_empty_pgp_folder(self, mock_build_cache_manager, tmp_path):

        # Arrange
        build_cache_dir = tmp_path / "build_cache"
        pgp_folder = build_cache_dir / "project" / "_pgp"
        pgp_folder.mkdir(parents=True)

        # Act
        result = mock_build_cache_manager.get_public_key_from_cache(str(build_cache_dir))

        # Assert
        assert result is None
        mock_build_cache_manager._logger.warning.assert_called_once_with("No PGP key files found in the build cache!")

    @pytest.mark.parametrize("items, expected_log_message", [
        (["item1", "item2"], "test message item1 item2 item1"),
        (["item1", "item2", "item3"], "test message item1 item2 item3 item1"),
    ])
    def test_log_warning_if_needed_multiple_items(self, mock_build_cache_manager, items, expected_log_message):
        # Test ID: multiple_items

        # Arrange
        warn_message = "test message"

        # Act
        mock_build_cache_manager._BuildCacheManager__log_warning_if_needed(warn_message, items)

        # Assert
        mock_build_cache_manager._logger.warning.assert_called_once_with(warn_message, items, items[0])

    @pytest.mark.parametrize("items", [
        [],
        ["item1"],
    ])
    def test_log_warning_if_needed_no_warning(self, mock_build_cache_manager, items):
        # Test ID: no_warning

        # Arrange
        warn_message = "test message"

        # Act
        mock_build_cache_manager._BuildCacheManager__log_warning_if_needed(warn_message, items)

        # Assert
        mock_build_cache_manager._logger.warning.assert_not_called()
