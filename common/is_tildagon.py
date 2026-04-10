import os


def is_tildagon():
    """Are we a badge?"""
    return "Tildagon" in os.uname().machine
