from painlessdb import __version__


def commandManager(args):
    """
    Built in cligo command manager.
    We call this in Terminal :
    C:/Some/Path> painlessdb <some_command>
    """
    if not args:
        exit()

    if args[0] == "test":
        print(f"Test is Working ;)")

    elif args[0] == "--version" or args[0] == "-V":
        print(f"PainlessDB v{__version__}")
