import sys
from painlessdb.core.management.commands import commandManager


def execute_from_command_line():
    args = sys.argv[1:]
    commandManager(args)
