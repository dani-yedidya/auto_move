import json
import os
from shutil import move
from os import path

setting_file = "settings.txt"
with open(setting_file, 'r') as f:
    settings = json.load(f)
    source_folder = settings['vars']['source folder']
    destination = settings['vars']['default destination']


def sivug(file_name: str):
    """
    defines what type of file by file name.
    not just by suffix, because this is user specific.

    TO DO: we should try to make this generic!!
    maybe with another variables dictionary,
    maybe with a separate function for each type, and this function should just call
    the function by filename.
    ***other option***: this functions is moved to a user specific file and
    is changed to fit user. because it is not complex.

    :param file_name: str
    :return: type of file for relocation: str
    the types are keys in variables dictionary
    where the values are the folder locations

    if file_name.startswith("Discount"):
        return 'bank'
    if file_name.endswith(".exe"):
        return 'exe'0
    if file_name.startswith("WhatsApp Image"):
        return 'WhatsApp Image'
    if file_name.endswith(".mp4"):
        return
    """
    with open(setting_file, 'r') as f:
        settings = json.load(f)
        endswith_dic = settings['endswith']  # get endswith functions dict from settings file
        startswith_dic = settings['startswith']  # get startswith functions dict from settings file

    for function in endswith_dic:  # loop through categories in dic and check if one is מתאים
        if file_name.endswith(function['key']):  # need to change config. fun --> type,
            # and make it not have words 'endswith' and 'startswith' in the function itself.
            return function['destination']
    for function in startswith_dic:
        if file_name.startswith(function['key']):
            return function['destination']
    return destination  # if nothing was found מתאים  - default destination


def move_file(src, filename, func=sivug, rename_option=True):
    """
    moves the file from source folder to desired destination folder.
    :param src: {str} source folder, taken from setting.txt
    :param filename: {str} filename of file to be moved
    :param func: option for sefaria.py module decorated sivug function: elis_sivug.
    :param rename_option: while using sefaria.py, renaming must be canceled because new dest
     includes the desired new file name.
    :return: None. just moves the file and maybe renames it.
    """
    dest = func(filename)
    # Check if there is already a file like this
    if rename_option:
        newfilename = "\\" + rename_if_necessary(src, dest, filename)
    else:
        newfilename = ""
    if dest != source_folder:
        move(src + '\\' + filename, dest + newfilename)


def rename_if_necessary(dir_src, dir_dest, oldfilename):
    newfilename = oldfilename
    index = 1
    if (path.exists(dir_dest + '\\' + newfilename)):
        while True:
            if path.exists(dir_src + '\\' + newfilename) or path.exists(dir_dest + '\\' + newfilename):
                newfilename = os.path.splitext(oldfilename)[0] + ' (' + str(index) + ')' + \
                              os.path.splitext(oldfilename)[1]
                index += 1
            else:
                break
    return newfilename


if __name__ == '__main__':  # goes over all files in source folder. not involving watchdog
    _, _, filenames = next(os.walk(source_folder), (None, None, []))
    for file in filenames:
        move_file(source_folder, file)
