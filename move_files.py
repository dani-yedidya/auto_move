import os
from shutil import move
from variables import *


def sivug(file_name: str):
    """
    defines what type of file by file name.
    not just by suffix, because this is user specific.

    TO DO: we should try to make this generic!!
    maybe with another variables dictionary,
    maybe with a seperate function for each type, and this function should just call
    the function by filename.
    ***other option***: this functions is moved to a user specific file and
    is changed to fit user. because it is not complex.

    :param file_name: str
    :return: type of file for relocation: str
    the types are keys in variables dictionary
    where the values are the folder locations
    """
    if file_name.startswith("Discount"):
        return 'bank'
    if file_name.endswith(".exe"):
        return 'exe'
    if file_name.startswith("WhatsApp Image"):
        return 'WhatsApp Image'
    if file_name.endswith(".mp4"):
        return


def move_file(src, filename):
    try:
        dest = destinations[sivug(filename)]
    except KeyError:
        pass
    else:
        move(src + '\\' + filename, dest)


if __name__ == '__main__':
    _, _, filenames = next(os.walk(source_folder), (None, None, []))
    for file in filenames:
        move_file(source_folder, file)
