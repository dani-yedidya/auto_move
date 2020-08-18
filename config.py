import  sys

print('Welcome to settings script.')
print('1 - view categories ')
print('2 - add categories ')
print('3 - delete categories ')
print('0 - end ')

#TODO: matybe we should add a change destination and source folder here.(.py=>.txt)
#TODO: make it easier to change without needing to know how to code.


settingsFile = 'settings.txt'  # this is for categories
varFile = 'variables.py'  # this is for directories


def end():
    print('End')
    sys.exit()



def view():
    try:
        with open(settingsFile, 'r') as f:
            print(f.read())
    except(FileNotFoundError):
        print('file not found')
        file = open(settingsFile, 'a+')
        file.write("")
        file.close()


def add():
    print('Enter name of function you want to add:')
    name = input()

    # search for name to avoid duplicates:
    isThereDup = False
    with open(settingsFile) as myFile:
        for num, line in enumerate(myFile, 1):  # why enumerate?? (y.t)
            if name in line:
                isThereDup = True
    if isThereDup:
        print('There is already a function named ' + name + '\n')
        add()  # אהבתי
    else:
        print("Enter function (e.g: endswith('.exe')")
        fun = input()
        print("Enter destination (e.g: C:\\Users\\yedid\\OneDrive\\Documents")
        des = input()
        # creates a function with name and function
        action = 'name: ' + name + '\nfun: ' + fun + '\n' + 'destination: ' + des + '\n\n'
        f = open(settingsFile, 'a')
        f.write(action)
        print('added ' + action)


def delete():
    print('Enter name of function you want to delete: ')
    name = input()

    with open(settingsFile, 'r') as read_file:
        lines = read_file.readlines()
    index = 0

    deleted = False
    for line in lines:
        if line == 'name: ' + name + '\n':
            del lines[index]  # why not shorten to [index:index+3]
            del lines[index]
            del lines[index]
            deleted = True
        index += 1
    with open(settingsFile, 'w+') as write_file:
        for line in lines:
            write_file.write(line)  # what are you writing here?
    if deleted:
        print('\ndeleted ' + name)
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
