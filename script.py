import sys

def show_help():
    help_message = """
    Usage: script.py [OPTIONS]
    Options:
      --help    Show this help message and exit.
    """
    print(help_message)

if "--help" in sys.argv:
    show_help()
else:
    print("Hello, this is a simple script!")
