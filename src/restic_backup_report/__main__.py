import os

from .targets.base_target import TargetTypeRegister
from .formats.base_format import FormatRegister

from .cli import register_cmds

from .targets.file_target import FileTarget

from .formats.plaintext_format import PlaintextFormat

from .utils.console import print_warn


if __name__ == "__main__":

    FormatRegister.register_formats({
        "plaintext": PlaintextFormat
    })

    TargetTypeRegister.register_targets({
        "file": FileTarget
    })

    register_cmds()