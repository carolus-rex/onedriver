from random import choice, randint
from subprocess import check_output, CalledProcessError

letters_dat = 'abcdefghijklmnopqrstuvwxyz'

letters = []

for letter in letters_dat:
	letters.append(letter)

def mkdir(dir):
	print('mkdir %s' % dir)
	try:
		check_output('mkdir test_root/%s' % dir, shell=True)
	except CalledProcessError:
		pass

for a in range(10):
	mkdir(''.join(choice(letters) for a in range(randint(1,15))))
