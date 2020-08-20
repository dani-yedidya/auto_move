import sys
import json
import os

# TODO: matybe we should add a change destination and source folder here.(.py=>.txt). DONE
# TODO: make it easier to change without needing to know how to code. DONE


settingsFile = 'settings.txt'  # this is for categories


def print_menu():
    print('\n\nWelcome to settings script.')
    print('1 - view categories and folders ')
    print('2 - add categories ')
    print('3 - delete categories ')
    print('4 - change source folder')
    print('5 - change default destination folder')
    print('9 - reset all.')
    print('0 - end ')


print_menu()


def write_default():
    open(settingsFile, 'a').close()
    if os.stat(settingsFile).st_size == 0:
        with open(settingsFile, 'w')as f:
            vars = {"source folder": "C:\\Users\\user\\Downloads",
                    "default destination": "C:\\Users\\user\\Desktop\\dest"}
            base = {
                "endswith": [

                ],
                "startswith": [],
                "vars": vars
            }

            json.dump(base, f, indent=4)


def end():
    print('End')
    sys.exit()


def view():
    with open(settingsFile, 'r') as f:
        write_default()
        read = json.load(f)
        print(json.dumps(read, indent=4))



def add():
    print('Enter name of function you want to add:')  # add e.g.
    name = input()
    write_default()
    # search for name to avoid duplicates:
    isThereDup = False
    with open(settingsFile) as myFile:  # should we change to f like in view function?
        f = json.load(myFile)
        for category, functions in f.items():
            if category != "vars":
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
            print("Type file ending:")
            type = "."+input()


        elif num == 2:
            print("Type beginning of file name. Please be accurate:")
            type = input()

        fun = fun_options[num]

        print("Enter destination (e.g: C:\\Users\\yedid\\OneDrive\\Documents):")
        des = input()
        action = {'name': name, 'key': type, 'destination': des}

        with open(settingsFile, 'r') as f:  # open file and edit settings
            settings_json = json.load(f)
            if fun in settings_json:
                settings_json[fun].append(action)
        os.remove(settingsFile)

        with open(settingsFile, 'w') as f:  # update settings file and print added function
            json.dump(settings_json, f, indent=4)
            print("Added: ", settings_json[fun][-1]) # show last funtion in list


def delete():
    write_default()
    with open(settingsFile, 'r') as read_file:
        f = json.load(read_file)
        if not f["endswith"] and not f["startswith"]:
            print("nothing to delete")
            return
        else:
            print('Enter name of function you want to delete: ')
            name = input()
    deleted = False
    for category, functions in f.items():
        if category != "vars":
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
    elif ans == 4:
        change_dir(1)
    elif ans == 5:
        change_dir(2)
    elif ans == 9:
        reset_all()
    else:
        print('syntax error')
    print_menu()


def change_dir(type):  # type 1 - source folder, type 2 - default dest
    print("Enter new path (e.g: C:\\Users\\yedid\\OneDrive\\Documents): ")
    path = input()
    with open(settingsFile, 'r')as f:
        read = json.load(f)
    if type == 1:
        read["vars"]["source folder"] = path
    elif type == 2:
        read["vars"]["default destination"] = path
    with open(settingsFile, 'w')as f:
        json.dump(read, f, indent=4)
    print("\nnew path is now: " + path)


def reset_all():
    print("are you sure? all categories will be deleted permanently.")
    print("enter y/n: ")
    answer = input()
    if answer == 'y':
        try:
            os.remove(settingsFile)
        except FileNotFoundError:
            pass
        write_default()
        print("all settings deleted")
        return
    elif answer == 'n':
        print("few! you scared me there.")
        return
    else:
        print("syntax error. ")
        reset_all()


while True:
    ans = input()
    try:
        runfun(int(ans))
    except ValueError:
        print('syntax error')
