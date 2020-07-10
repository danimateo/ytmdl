"""Some definitions to interact with the command line."""

import subprocess
from os import remove, path, popen
from ytmdl import defaults
from shutil import which
import ffmpeg


def exe(command):
    """Execute the command externally.

    Written by Nishan Pantha.
    """
    command = command.strip()
    c = command.split()
    output, error = subprocess.Popen(c,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE).communicate()
    output = output.decode('utf-8').strip()
    error = error.decode('utf-8').strip()
    return (output, error)


def get_terminal_length():
    """Return the length of the terminal."""
    rows, cols = popen('stty size', 'r').read().split()

    return int(cols)


def convert_to_mp3r(path):
    """Convert the file to mp3 using ffmpeg."""
    try:
        new_name = path + '_new.mp3'

        command = "ffmpeg -loglevel panic -i {} -vn -ar 44100 -ac 2 -ab {}k -f mp3 {}".format(path,
                                                                                             defaults.DEFAULT.SONG_QUALITY,
                                                                                              new_name)
        output, error = exe(command)

        # Delete the temp file now
        remove(path)
        return new_name
    except Exception as e:
        return e


def convert_to_mp3(path):
    """Covert to mp3 using the python ffmpeg module."""
    new_name = path + '_converted.mp3'
    try:
        ffmpeg.input(path).output(
                            new_name,
                            loglevel='panic',
                            ar=44100,
                            ac=2,
                            ab='{}k'.format(defaults.DEFAULT.SONG_QUALITY),
                            f='mp3'
                        ).run()
        # Delete the temp file now
        remove(path)
        return new_name
    except ffmpeg._run.Error:
        # This error is usually thrown where ffmpeg doesn't have to
        # overwrite a file.
        # The bug is from ffmpeg, I'm just adding this catch to
        # handle that.
        return new_name


def cut_song(path, start, stop):
    """Cut song based on start and stop values using the ffmpeg module."""
    if '.mp3' in path:
        new_name = ('_cut.mp3').join(path.split('.mp3'))
    else:
        new_name = path + '_cut.mp3'
    try:
        start_converted = _get_converted_time(start)
        stop_converted = _get_converted_time(stop)

        command = 'ffmpeg -y -i {} '.format(path)
        if start is not None:
            command += '-ss {} '.format(start_converted)
        if stop is not None:
            command += '-to {} '.format(stop_converted)
        command += '-c copy  {}'.format(new_name)

        output, error = exe(command)
        remove(path)
        return new_name
    
    except Exception as e:
        print("Error: {}".format(e))
        return e


def is_valid(dir_path):
    """Check if passed path is valid or not."""
    if not path.isfile(dir_path):
        return False
    else:
        return True


def get_songs(file_path):
    """Extract the songs from the provided list."""

    if is_valid(file_path):
        RSTREAM = open(file_path, 'r')

        song_tup = RSTREAM.read().split("\n")

        return song_tup
    else:
        return []


def is_present(app):
    """Check if the passed app is installed in the machine."""
    return which(app) is not None


def _get_converted_time(time):
    if time is not None:
        sec_values = [1]
        time_split = time.split(":")
        time_units = len(time_split)
        if time_units > 1:
            sec_values.insert(0, 60)
        if time_units == 3:
            sec_values.insert(0, 3600)
        return sum(x * int(t) for x, t in zip(sec_values, time.split(":"))) 
    return None
