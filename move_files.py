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

        if file_name.startswith("Discount"):
        return 'bank'
    if file_name.endswith(".exe"):
        return 'exe'0
    if file_name.startswith("WhatsApp Image"):
        return 'WhatsApp Image'
    if file_name.endswith(".mp4"):
        return
    """
    endswithDic = get_endsWith() #get endswith functions dict from settings file
    startswithDic = get_startsWith() #get startswith functions dict from settings file

    for category in endswithDic: #loop through categories in dic and check if one is מתאים
        if file_name.endswith(endswithDic[category][0]):
            return endswithDic[category][1].split('\n')[0]
    for category in startswithDic:
        if file_name.startswith(endswithDic[category][0]):
            return endswithDic[category][1].split('\n')[0]
    return destination# if nothing was found מתאים default destination




def move_file(src, filename):
    try:
        dest = sivug(filename)
    except KeyError:
        pass
    else:
        move(src + '\\' + filename, dest)


def get_endsWith():
    # returns dict of startsWith actions from settings file
    settingsFile = 'settings.txt'
    endsWithDic = {}

    with open(settingsFile) as f: #closes file after use
        index = 0 # index is used to run through the loop
        isDest = False #boolean used to check if found a destination
        isFun = False #boolean used to check if found a function

        for line in f.readlines(): #runs through the file line by line
            if line.startswith('fun: endswith'):
                fun = line.split("fun: endswith('", 1)[1].split("')")[0] #will return only whats within the ()
                isFun = True #found function that fits
            if line.startswith('destination')and isFun: #Called only if there was a function that fits
                dest = line.split("destination: ", 1)[1] # will return only destination without 'destination: '
                isDest = True #found destination that fits
            if isDest and isFun:
                endsWithDic[index] = (fun, dest) # adds to ends with dictionary
                isDest = False #resets values
                isFun = False
                index += 1

    return endsWithDic


def get_startsWith():
    # returns dict of startsWith acctions from settings file
    # for explanation see get_endsWith() expl. it's the same.
    settingsFile = 'settings.txt'
    startsWithDic = {}

    with open(settingsFile) as f:
        index = 0
        isDest = False
        isFun = False

        for line in f.readlines():
            if line.startswith('fun: startsWith'):
                fun = line.split("fun: startsWith('", 1)[1].split("')")[0]
                isFun = True
            if line.startswith('destination')and isFun:
                dest = line.split("destination: ", 1)[1]
                isDest = True
            if isDest and isFun:
                startsWithDic[index] = (fun, dest)
                isDest = False
                isFun = False
                index += 1

    return startsWithDic


if __name__ == '__main__':
    _, _, filenames = next(os.walk(source_folder), (None, None, []))
    for file in filenames:
        move_file(source_folder, file)
