from random import choice, randint
from subprocess import check_output, CalledProcessError
from onedriver import OneDrive

letters_dat = 'abcdefghijklmnopqrstuvwxyz'

letters = []

drive = OneDrive()

for letter in letters_dat:
    letters.append(letter)


def local_mkdir(dir):
    print('mkdir %s' % dir)
    try:
        check_output('mkdir test_root\\%s' % dir, shell=True)
    except CalledProcessError:
        pass


def mkdir(dir, one=False):
    if one:
        drive.mkdir(dir)
    else:
        local_mkdir(dir)


ONE = False

for a in range(20):
    mkdir(''.join(choice(letters) for b in range(randint(1, 15))),
          one=ONE)
