"""Contains the definition of class DEFAULT."""
from ytmdl import setupConfig
import os
from xdg.BaseDirectory import xdg_cache_home

def _providers_string_to_list(val):
    if type(val) == str:
        return val.replace(' ', '').split(',')
    return val

class DEFAULT:
    """DEFAULT class contains value of different constants."""

    # The home dir
    HOME_DIR = os.path.expanduser('~')

    # The directory where songs will be saved
    SONG_DIR = setupConfig.GIVE_DEFAULT(1, 'SONG_DIR')

    # The temp directory where songs will be modded
    SONG_TEMP_DIR = os.path.join(xdg_cache_home, 'ytmdl')

    # The path to keep cover image
    COVER_IMG = os.path.join(SONG_TEMP_DIR, 'cover.jpg')

    # The song quality
    SONG_QUALITY = setupConfig.GIVE_DEFAULT(1, 'QUALITY')

    # The metadata providers
    METADATA_PROVIDERS = _providers_string_to_list(
        setupConfig.GIVE_DEFAULT(1, 'METADATA_PROVIDERS'))


class FORMAT:
    """
    Class to handle stuff related to the passed
    format.
    """
    valid_formats = [
        'mp3',
        'm4a'
    ]
