import os

from .targets.base_target import TargetTypeRegister
from .cli import register_cmds

from .targets.file_target import FileTarget

from .utils.console import print_warn


if __name__ == "__main__":

    TargetTypeRegister.register_targets({
        "file": FileTarget
    })

    register_cmds()