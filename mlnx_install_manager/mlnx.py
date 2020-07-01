#!/usr/bin/env python3
"""This module provides the SlurmInstallManager."""

import logging
import os
from pathlib import Path
import subprocess
from time import sleep


from ops.framework import Object
from ops.model import ModelError

from ops.framework import StoredState


logger = logging.getLogger()


class MLNXInstallManager(Object):
    """MLNX installation ops."""

    _state = StoredState()

    def __init__(self, *args):
        super().__init__(*args)

        if os_series() == 'ubuntu':
            _MLNX_REPO = ("https://linux.mellanox.com/public/repo/"
                          "mlnx_ofed/latest/ubuntu18.04/mellanox_mlnx_ofed.list")
            _APT_SOURCE_PATH = Path("/etc/apt/sources.list.d/mellanox_mlnx_ofed.list")
        elif os_series() == 'centos':
            _MLNX_REPO = ("https://linux.mellanox.com/public/repo/"
                          "mlnx_ofed/latest/ubuntu18.04/mellanox_mlnx_ofed.list")
            _APT_SOURCE_PATH = Path("/etc/apt/sources.list.d/mellanox_mlnx_ofed.list")


    def add_mlnx_ubuntu(self):
        """Prepare for the installation of mlnx repo and packages."""
        # Add the mlnx key
        subprocess.call(
            ("get -qO - https://www.mellanox.com/downloads/ofed/RPM-GPG-KEY-Mellanox "
             "| apt-key add -"),
            shell=True
        )

        # Add the mlnx apt repo
        resp = requests.get(self._MLNX_REPO)
        self._APT_SOURCE_PATH.write_text(resp.text)
        subprocess.call(["apt", "update", "-y"])

        # Remove conflicting apt packages
        subprocess.call(
            ("apt-get remove libipathverbs1 librdmacm1 libibverbs1 "
             "libmthca1 libopenmpi-dev openmpi-bin openmpi-common "
             "openmpi-doc libmlx4-1 rdmacm-utils ibverbs-utils "
             "infiniband-diags ibutils perftest -y"),
            shell=True
        )
        subprocess.call(["apt", "install", "mlnx-ofed-all", "-y"])
        self.unit.status = ActiveStatus("MLNX ready")

    def add_mlnx_centos(self):
        pass
