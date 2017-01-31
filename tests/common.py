import os
import sys

def set_library_path(config, platforms = ['darwin'], path = None):
    '''
    Calls config.set_library_path(path) if the current platform is one of the
    listed platforms. If the path is not set, it defaults to ../output,
    relative to the tests directory (i.e. the one containing this file).
    '''
    if sys.platform in platforms:
        if path is None:
            # FIXME: Find a way to avoid hardcoding this path (Maybe get it from CMake?).
            path = os.path.dirname(os.path.realpath(__file__)) + '/../build/generated'
        config.set_library_path(path)
