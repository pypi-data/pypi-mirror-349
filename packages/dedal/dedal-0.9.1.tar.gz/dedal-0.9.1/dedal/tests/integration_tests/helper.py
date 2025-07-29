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

import uuid
from pathlib import Path

from dedal.spack_factory.SpackOperation import SpackOperation
from dedal.utils.spack_utils import extract_spack_packages
from dedal.utils.variables import test_spack_env_name


def check_installed_spack_packages(spack_operation: SpackOperation, install_dir: Path):
    to_install_spack_packages = extract_spack_packages(str(install_dir / test_spack_env_name / 'spack.yaml'))
    installed_spack_packages = list(spack_operation.find_packages().keys())
    for spack_pacakge in to_install_spack_packages:
        assert spack_pacakge in installed_spack_packages


def get_test_path():
    return Path(f"/tmp/test-{uuid.uuid4()}").resolve()