
import math
import random

def getIntOrFloat(str_number):
	number = None
	try:
		number = int(str_number)
	except ValueError:
		try:
			number = float(str_number)
		except ValueError:
			pass
	return number

def int_choice_generate(number):
	choices = set()
	choices.add(number)

	lg = math.log10(number)
	exp = math.floor(lg) - 1
	remain = int(number % (10**exp))

	while len(choices) < 4:
		if exp >= 0:
			r = random.randrange(10, 100)
			newchoice = int((r * 10**exp) + remain)
		else:
			newchoice = random.randrange(1, 10)
		print(newchoice)
		choices.add(newchoice)

	print(choices)


if __name__ == "__main__":
	while True:
		x = input("enter number: ")
		number = getIntOrFloat(x)
		if number == None:
			break
		int_choice_generate(number)