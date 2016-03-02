
import csv



def read_results(filename):
	with open(filename) as csvfile:
		spamreader = csv.reader(csvfile)
		for row in spamreader:
			pass



if __name__ == "__main__":
	read_results("globalwarming/results1.csv")