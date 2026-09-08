from .targets.target import register_targets
from .cli import register_cmds

from .targets.file_target import FileTarget


if __name__ == "__main__":

    register_targets({
        "file": FileTarget
    })

    register_cmds()