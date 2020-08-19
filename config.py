import sys
import json
import os

"""
json format:
{
    'endswith': [
        {
            'name':'name_str', 
            'fun': 'fun_str',
             'destination': 'dest_str'
        },
        {same}
    ],
    'startwith':
        [      
            {same},
            {and so on}
        ]
}
"""

print('Welcome to settings script.')
print('1 - view categories ')
print('2 - add categories ')
print('3 - delete categories ')
print('0 - end ')

# TODO: matybe we should add a change destination and source folder here.(.py=>.txt)
# TODO: make it easier to change without needing to know how to code.


settingsFile = 'settings.txt'  # this is for categories
varFile = 'variables.py'  # this is for directories


def end():
    print('End')
    sys.exit()


def view():
    try:
        with open(settingsFile, 'r') as f:
            read = json.load(f)
            print(json.dumps(read, indent=4))
    except(FileNotFoundError):
        print('file not found')
        file = open(settingsFile, 'a+')
        file.write("")
        file.close()


def add():
    print('Enter name of function you want to add:')  # add e.g.
    name = input()

    # search for name to avoid duplicates:
    isThereDup = False
    with open(settingsFile) as myFile:  # should we change to f like in view function?
        f = json.load(myFile)
        for category, functions in f.items():
            for function in functions:
                if function['name'] == name:
                    isThereDup = True
    if isThereDup:
        print('There is already a function named ' + name + '\n')
        add()  # אהבתי
    else:
        fun_options = {1: 'endswith', 2: 'startswith'}  # **can add more options if we use more functions, like regex**
        print("Choose function:")
        for k, v in fun_options.items():
            print(k, "-", v)  # print all function options
        print("Enter numbers only:")
        while True:
            try:
                num = int(input())
                if num in fun_options:  # meaning if input is 1 or 2, for now
                    break
                else:
                    print("Invalid input")
            except:
                pass
        if num == 1:
            type_options = {1: 'exe', 2: 'mp4', 3: 'jpg', 4: 'pdf'}  # same as above
            print("Choose function:")
            for k, v in type_options.items():
                print(k, "-", v)  # print all type options
            print("Enter numbers only:")
            while True:
                try:
                    type = int(input())
                    if type in type_options:
                        break
                    else:
                        print("Invalid input")
                except:
                    pass  # till here same
        elif num == 2:
            pass  # need to add options for startswith
        fun = fun_options[num]
        full_function = fun + "(." + type_options[type] + ")"

        print(r"Enter destination (e.g: C:\\Users\\yedid\\OneDrive\\Documents):")
        des = input()
        action = {'name': name, 'fun': full_function, 'destination': des}

        with open(settingsFile, 'r') as f:  # open file and edit settings
            settings_json = json.load(f)
            if fun in settings_json:
                settings_json[fun].append(action)
        os.remove(settingsFile)

        with open(settingsFile, 'w') as f:  # update settings file and print added function
            json.dump(settings_json, f, indent=4)
            print("Added: ", settings_json[fun][-1])


def delete():
    print('Enter name of function you want to delete: ')
    name = input()

    with open(settingsFile, 'r') as read_file:
        f = json.load(read_file)
    deleted = False
    for category, functions in f.items():
        for num, function in enumerate(functions):
            if function['name'] == name:
                del functions[num]
                deleted = True
    if deleted:
        os.remove(settingsFile)
        with open(settingsFile, 'w+') as write_file:
            json.dump(f, write_file, indent=4)

        print('\nDeleted ' + name)
    else:
        print(name + ' not found')


def runfun(ans):
    if ans == 0:
        end()
    elif ans == 1:
        view()
    elif ans == 2:
        add()
    elif ans == 3:
        delete()
    else:
        print('syntax error')


while True:
    ans = input()
    try:
        runfun(int(ans))
    except ValueError:
        print('syntax error')
