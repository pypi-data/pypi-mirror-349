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

import os
import re
import subprocess
from pathlib import Path
from dedal.configuration.SpackConfig import SpackConfig
from dedal.enum.SpackConfigCommand import SpackConfigCommand
from dedal.error_handling.exceptions import BashCommandException, NoSpackEnvironmentException, \
    SpackInstallPackagesException, SpackConcertizeException, SpackMirrorException, SpackGpgException, \
    SpackRepoException, SpackReindexException, SpackSpecException, SpackConfigException, SpackFindException
from dedal.logger.logger_builder import get_logger
from dedal.tests.testing_variables import SPACK_VERSION
from dedal.utils.utils import run_command, git_clone_repo, log_command, set_bashrc_variable, get_first_word
from dedal.wrapper.spack_wrapper import check_spack_env
import glob


class SpackOperation:
    """
    This class should implement the methods necessary for installing spack, set up an environment, concretize and install packages.
    Factory design pattern is used because there are 2 cases: creating an environment from scratch or creating an environment from the buildcache.

    Attributes:
    -----------
    env : SpackDescriptor
        spack environment details
    repos : list[SpackDescriptor]
    upstream_instance : str
        path to Spack instance to use as upstream (optional)
    """

    def __init__(self, spack_config: SpackConfig = SpackConfig(), logger=get_logger(__name__)):
        self.spack_config = spack_config
        self.spack_config.install_dir = spack_config.install_dir
        os.makedirs(self.spack_config.install_dir, exist_ok=True)
        self.spack_dir = self.spack_config.install_dir / 'spack'

        self.spack_setup_script = "" if self.spack_config.use_spack_global else f"source {self.spack_dir / 'share' / 'spack' / 'setup-env.sh'}"
        self.logger = logger
        self.spack_config.concretization_dir = spack_config.concretization_dir
        if self.spack_config.concretization_dir:
            os.makedirs(self.spack_config.concretization_dir, exist_ok=True)
        self.spack_config.buildcache_dir = spack_config.buildcache_dir
        if self.spack_config.buildcache_dir:
            os.makedirs(self.spack_config.buildcache_dir, exist_ok=True)
        if self.spack_config.env and spack_config.env.name:
            self.env_path: Path = spack_config.env.path / spack_config.env.name
            if self.spack_setup_script != "":
                self.spack_command_on_env = f'{self.spack_setup_script} && spack env activate -p {spack_config.view.value} {self.env_path}'
            else:
                self.spack_command_on_env = f'spack env activate -p {spack_config.view.value} {self.env_path}'
        else:
            self.spack_command_on_env = self.spack_setup_script
        if self.spack_config.env and spack_config.env.path:
            self.spack_config.env.path.mkdir(parents=True, exist_ok=True)

    def create_fetch_spack_environment(self):
        """Fetches a spack environment if the git path is defined, otherwise creates it."""
        if self.spack_config.env and self.spack_config.env.git_path:
            git_clone_repo(self.spack_config.env.name, self.spack_config.env.path / self.spack_config.env.name,
                           self.spack_config.env.git_path,
                           logger=self.logger)
        else:
            os.makedirs(self.spack_config.env.path / self.spack_config.env.name, exist_ok=True)
            run_command("bash", "-c",
                        f'{self.spack_setup_script} && spack env create -d {self.env_path}',
                        check=True, logger=self.logger,
                        info_msg=f"Created {self.spack_config.env.name} spack environment",
                        exception_msg=f"Failed to create {self.spack_config.env.name} spack environment",
                        exception=BashCommandException)

    def setup_spack_env(self):
        """
        This method prepares a spack environment by fetching/creating the spack environment and adding the necessary repos
        """
        if self.spack_config.system_name:
            set_bashrc_variable('SYSTEMNAME', self.spack_config.system_name, self.spack_config.bashrc_path,
                                logger=self.logger)
            os.environ['SYSTEMNAME'] = self.spack_config.system_name
        if self.spack_dir.exists() and self.spack_dir.is_dir():
            set_bashrc_variable('SPACK_USER_CACHE_PATH', str(self.spack_dir / ".spack"), self.spack_config.bashrc_path,
                                logger=self.logger)
            set_bashrc_variable('SPACK_USER_CONFIG_PATH', str(self.spack_dir / ".spack"), self.spack_config.bashrc_path,
                                logger=self.logger)
            self.logger.debug('Added env variables SPACK_USER_CACHE_PATH and SPACK_USER_CONFIG_PATH')
        else:
            self.logger.error(f'Invalid installation path: {self.spack_dir}')
        # Restart the bash after adding environment variables
        if self.spack_config.env:
            self.create_fetch_spack_environment()
        if self.spack_config.install_dir.exists():
            for repo in self.spack_config.repos:
                repo_dir = self.spack_config.install_dir / repo.path / repo.name
                git_clone_repo(repo.name, repo_dir, repo.git_path, logger=self.logger)
                if not self.spack_repo_exists(repo.name):
                    self.add_spack_repo(repo.path, repo.name)
                    self.logger.debug(f'Added spack repository {repo.name}')
                else:
                    self.logger.debug(f'Spack repository {repo.name} already added')

    def spack_repo_exists(self, repo_name: str) -> bool | None:
        """Check if the given Spack repository exists.
        Returns:
            True if spack repository exists, False otherwise.
        """
        if self.spack_config.env is None:
            result = run_command("bash", "-c",
                                 f'{self.spack_setup_script} && spack repo list',
                                 check=True,
                                 capture_output=True, text=True, logger=self.logger,
                                 info_msg=f'Checking if {repo_name} exists')
            if result is None:
                return False
        else:
            if self.spack_env_exists():
                result = run_command("bash", "-c",
                                     f'{self.spack_command_on_env} && spack repo list',
                                     check=True,
                                     capture_output=True, text=True, logger=self.logger,
                                     info_msg=f'Checking if repository {repo_name} was added').stdout
            else:
                self.logger.debug('No spack environment defined')
                raise NoSpackEnvironmentException('No spack environment defined')
            if result is None:
                return False
        return any(line.strip().endswith(repo_name) for line in result.splitlines())

    def spack_env_exists(self):
        """Checks if a spack environments exists.
        Returns:
            True if spack environments exists, False otherwise.
        """
        result = run_command("bash", "-c",
                             self.spack_command_on_env,
                             check=True,
                             capture_output=True, text=True, logger=self.logger,
                             info_msg=f'Checking if environment {self.spack_config.env.name} exists')
        return result is not None

    def add_spack_repo(self, repo_path: Path, repo_name: str):
        """Add the Spack repository if it does not exist."""
        run_command("bash", "-c",
                    f'{self.spack_command_on_env} && spack repo add {repo_path}/{repo_name}',
                    check=True, logger=self.logger,
                    info_msg=f"Added {repo_name} to spack environment {self.spack_config.env.name}",
                    exception_msg=f"Failed to add {repo_name} to spack environment {self.spack_config.env.name}",
                    exception=SpackRepoException)

    @check_spack_env
    def get_compiler_version(self):
        """Returns the compiler version
        Raises:
            NoSpackEnvironmentException: If the spack environment is not set up.
        """
        result = run_command("bash", "-c",
                             f'{self.spack_command_on_env} && spack compiler list',
                             check=True, logger=self.logger,
                             capture_output=True, text=True,
                             info_msg=f"Checking spack environment compiler version for {self.spack_config.env.name}",
                             exception_msg=f"Failed to checking spack environment compiler version for {self.spack_config.env.name}",
                             exception=BashCommandException)

        if result.stdout is None:
            self.logger.debug(f'No gcc found for {self.spack_config.env.name}')
            return None

        # Find the first occurrence of a GCC compiler using regex
        match = re.search(r"gcc@([\d\.]+)", result.stdout)
        gcc_version = match.group(1)
        self.logger.debug(f'Found gcc for {self.spack_config.env.name}: {gcc_version}')
        return gcc_version

    def get_spack_installed_version(self):
        """Returns the spack installed version"""
        spack_version = run_command("bash", "-c", f'{self.spack_setup_script} && spack --version',
                                    capture_output=True, text=True, check=True,
                                    logger=self.logger,
                                    info_msg=f"Getting spack version",
                                    exception_msg=f"Error retrieving Spack version")
        if spack_version:
            return spack_version.stdout.strip().split()[0]
        return None

    @check_spack_env
    def concretize_spack_env(self, force=True, test=None):
        """Concretization step for a spack environment
            Args:
                force (bool): TOverrides an existing concretization when set to True
                test: which test dependencies should be included
            Raises:
                NoSpackEnvironmentException: If the spack environment is not set up.
        """
        force = '--force' if force else ''
        test = f'--test {test}' if test else ''
        run_command("bash", "-c",
                    f'{self.spack_command_on_env} && spack concretize {force} {test}',
                    check=True,
                    logger=self.logger,
                    info_msg=f'Concertization step for {self.spack_config.env.name}',
                    exception_msg=f'Failed the concertization step for {self.spack_config.env.name}',
                    exception=SpackConcertizeException)

    def reindex(self):
        """Reindex step for a spack environment
            Raises:
                SpackReindexException: If the spack reindex command fails.
        """
        run_command("bash", "-c",
                    f'{self.spack_command_on_env} && spack reindex',
                    check=True,
                    logger=self.logger,
                    info_msg=f'Reindex step.',
                    exception_msg=f'Failed the reindex.',
                    exception=SpackReindexException)

    def spec_pacakge(self, package_name: str):
        """Reindex step for a spack environment
            Raises:
                SpackSpecException: If the spack spec command fails.
        """
        try:
            spec_output = run_command("bash", "-c",
                                      f'{self.spack_command_on_env} && spack spec {package_name}',
                                      check=True,
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE,
                                      text=True,
                                      logger=self.logger,
                                      info_msg=f'Spack spec {package_name}.',
                                      exception_msg=f'Failed to spack spec {package_name}.',
                                      exception=SpackSpecException).stdout
            pattern = r'^\s*-\s*([\w.-]+@[\d.]+)'
            match = re.search(pattern, spec_output)
            if match:
                return match.group(1)
            return None
        except SpackSpecException:
            return None

    def create_gpg_keys(self):
        """Creates GPG keys (which can be used when creating binary cashes) and adds it to the trusted keyring."""
        if self.spack_config.gpg:
            run_command("bash", "-c",
                        f'{self.spack_setup_script} && spack gpg init && spack gpg create {self.spack_config.gpg.name} {self.spack_config.gpg.mail}',
                        check=True,
                        logger=self.logger,
                        info_msg=f'Created pgp keys for {self.spack_config.env.name}',
                        exception_msg=f'Failed to create pgp keys mirror {self.spack_config.env.name}',
                        exception=SpackGpgException)
        else:
            raise SpackGpgException('No GPG configuration was defined is spack configuration')

    def add_mirror(self, mirror_name: str, mirror_path: Path, signed=False, autopush=False, global_mirror=False):
        """Adds a Spack mirror.
        Adds a new mirror to the Spack configuration, either globally or to a specific environment.
        Args:
            mirror_name (str): The name of the mirror.
            mirror_path (str): The path or URL of the mirror.
            signed (bool): Whether to require signed packages from the mirror.
            autopush (bool): Whether to enable autopush for the mirror.
            global_mirror (bool): Whether to add the mirror globally (True) or to the current environment (False).
        Raises:
            ValueError: If mirror_name or mirror_path are empty.
            NoSpackEnvironmentException: If global_mirror is False and no environment is defined.
        """
        autopush = '--autopush' if autopush else ''
        signed = '--signed' if signed else ''
        spack_add_mirror = f'spack mirror add {autopush} {signed} {mirror_name} {mirror_path}'
        if global_mirror:
            run_command("bash", "-c",
                        f'{self.spack_setup_script} && {spack_add_mirror}',
                        check=True,
                        logger=self.logger,
                        info_msg=f'Added mirror {mirror_name}',
                        exception_msg=f'Failed to add mirror {mirror_name}',
                        exception=SpackMirrorException)
        else:
            check_spack_env(
                run_command("bash", "-c",
                            f'{self.spack_command_on_env} && {spack_add_mirror}',
                            check=True,
                            logger=self.logger,
                            info_msg=f'Added mirror {mirror_name}',
                            exception_msg=f'Failed to add mirror {mirror_name}',
                            exception=SpackMirrorException))

    @check_spack_env
    def trust_gpg_key(self, public_key_path: str):
        """Adds a GPG public key to the trusted keyring.
        This method attempts to add the provided GPG public key to the
        Spack trusted keyring.
        Args:
            public_key_path (str): Path to the GPG public key file.
        Returns:
            bool: True if the key was added successfully, False otherwise.
        Raises:
            ValueError: If public_key_path is empty.
            NoSpackEnvironmentException: If the spack environment is not set up.
        """
        if not public_key_path:
            raise ValueError("public_key_path is required")

        run_command("bash", "-c",
                    f'{self.spack_command_on_env} && spack gpg trust {public_key_path}',
                    check=True,
                    logger=self.logger,
                    info_msg=f'Trusted GPG key for {self.spack_config.env.name}',
                    exception_msg=f'Failed to trust GPG key for {self.spack_config.env.name}',
                    exception=SpackGpgException)

    def config(self, config_type: SpackConfigCommand, config_parameter):
        run_command("bash", "-c",
                    f'{self.spack_command_on_env} && spack config {config_type.value} \"{config_parameter}\"',
                    check=True,
                    logger=self.logger,
                    info_msg='Spack config command',
                    exception_msg='Spack config command failed',
                    exception=SpackConfigException)

    def mirror_list(self):
        """Returns of available mirrors. When an environment is activated it will return the mirrors associated with it,
           otherwise the mirrors set globally"""
        mirrors = run_command("bash", "-c",
                              f'{self.spack_command_on_env} && spack mirror list',
                              check=True,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              text=True,
                              logger=self.logger,
                              info_msg=f'Listing mirrors',
                              exception_msg=f'Failed list mirrors',
                              exception=SpackMirrorException).stdout
        return list(map(get_first_word, list(mirrors.strip().splitlines())))

    def remove_mirror(self, mirror_name: str):
        """Removes a mirror from an environment (if it is activated), otherwise removes the mirror globally."""
        if not mirror_name:
            raise ValueError("mirror_name is required")
        run_command("bash", "-c",
                    f'{self.spack_command_on_env} && spack mirror rm {mirror_name}',
                    check=True,
                    logger=self.logger,
                    info_msg=f'Removing mirror {mirror_name}',
                    exception_msg=f'Failed to remove mirror {mirror_name}',
                    exception=SpackMirrorException)

    def update_buildcache_index(self, mirror_path: str):
        """Updates buildcache index"""
        if not mirror_path:
            raise ValueError("mirror_path is required")
        run_command("bash", "-c",
                    f'{self.spack_command_on_env} && spack buildcache update-index {mirror_path}',
                    check=True,
                    logger=self.logger,
                    info_msg=f'Updating build cache index for mirror {mirror_path}',
                    exception_msg=f'Failed to update build cache index for mirror {mirror_path}',
                    exception=SpackMirrorException)

    def install_gpg_keys(self):
        """Install gpg keys"""
        run_command("bash", "-c",
                    f'{self.spack_command_on_env} && spack buildcache keys --install --trust',
                    check=True,
                    logger=self.logger,
                    info_msg=f'Installing gpg keys from mirror',
                    exception_msg=f'Failed to install gpg keys from mirror',
                    exception=SpackGpgException)

    @check_spack_env
    def install_packages(self, jobs: int, signed=True, fresh=False, debug=False, test=None):
        """Installs all spack packages.
        Raises:
            NoSpackEnvironmentException: If the spack environment is not set up.
        """
        signed = '' if signed else '--no-check-signature'
        fresh = '--fresh' if fresh else ''
        debug = '--debug' if debug else ''
        test = f'--test {test}' if test else ''
        install_result = run_command("bash", "-c",
                                     f'{self.spack_command_on_env} && spack {debug} install -v {signed} -j {jobs} {fresh} {test}',
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE,
                                     text=True,
                                     logger=self.logger,
                                     info_msg=f"Installing spack packages for {self.spack_config.env.name}",
                                     exception_msg=f"Error installing spack packages for {self.spack_config.env.name}",
                                     exception=SpackInstallPackagesException)
        log_command(install_result, str(Path(os.getcwd()).resolve() / ".generate_cache.log"))
        if install_result.returncode == 0:
            self.logger.info(f'Finished installation of spack packages from scratch')
        else:
            self.logger.error(f'Something went wrong during installation. Please check the logs.')
        return install_result

    @check_spack_env
    def find_packages(self):
        """Returns a dictionary of installed Spack packages in the current environment.
        Each key is the name of a Spack package, and the corresponding value is a list of
        installed versions for that package.
        Raises:
            NoSpackEnvironmentException: If the spack environment is not set up.
        """
        packages = run_command("bash", "-c",
                               f'{self.spack_command_on_env} && spack find -c',
                               check=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               text=True,
                               logger=self.logger,
                               info_msg=f'Listing installed packages.',
                               exception_msg=f'Failed to list installed packages',
                               exception=SpackFindException).stdout
        dict_packages = {}
        for package in packages.strip().splitlines():
            if package.startswith('[+]'):
                package = package.replace('@', ' ').split()
                if len(package) == 3:
                    _, name, version = package
                    dict_packages.setdefault(name, []).append(version)
        return dict_packages

    def install_spack(self, spack_version=f'{SPACK_VERSION}', spack_repo='https://github.com/spack/spack',
                      bashrc_path=os.path.expanduser("~/.bashrc")):
        """Install spack.
            Args:
                spack_version (str): spack version
                spack_repo (str): Git path to the Spack repository.
                bashrc_path (str): Path to the .bashrc file.
        """
        spack_version = f'v{spack_version}'
        try:
            user = os.getlogin()
        except OSError:
            user = None

        self.logger.info(f"Starting to install Spack into {self.spack_dir} from branch {spack_version}")
        if not self.spack_dir.exists():
            run_command(
                "git", "clone", "--depth", "1",
                "-c", "advice.detachedHead=false",
                "-c", "feature.manyFiles=true",
                "--branch", spack_version, spack_repo, self.spack_dir
                , check=True, logger=self.logger)
            self.logger.debug("Cloned spack")
        else:
            self.logger.debug("Spack already cloned.")

        if bashrc_path:
            # ensure the file exists before opening it
            if not os.path.exists(bashrc_path):
                open(bashrc_path, "w").close()
            # add spack setup commands to .bashrc
            with open(bashrc_path, "a") as bashrc:
                bashrc.write(f'export PATH="{self.spack_dir}/bin:$PATH"\n')
                spack_setup_script = f"source {self.spack_dir / 'share' / 'spack' / 'setup-env.sh'}"
                bashrc.write(f"{spack_setup_script}\n")
            self.logger.info("Added Spack PATH to .bashrc")
        if user:
            run_command("chown", "-R", f"{user}:{user}", self.spack_dir, check=True, logger=self.logger,
                        info_msg='Adding permissions to the logged in user')
        self.logger.info("Spack install completed")
        if self.spack_config.use_spack_global is True and bashrc_path is not None:
            # Restart the bash only of the spack is used globally
            self.logger.info('Restarting bash')
            run_command("bash", "-c", f"source {bashrc_path}", check=True, logger=self.logger, info_msg='Restart bash')
            os.system("exec bash")
        # Configure upstream Spack instance if specified
        if self.spack_config.upstream_instance:
            search_path = os.path.join(self.spack_config.upstream_instance, 'spack', 'opt', 'spack', '**', '.spack-db')
            spack_db_dirs = glob.glob(search_path, recursive=True)
            upstream_prefix = [os.path.dirname(dir) for dir in spack_db_dirs]
            for prefix in upstream_prefix:
                self.config(SpackConfigCommand.ADD, f':upstream-spack-instance:install_tree:{prefix}')
            self.logger.info("Added upstream spack instance")
