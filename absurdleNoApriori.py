import itertools
from string import ascii_lowercase
from absurdle import GRAYSQUARE, playAbsurdle

runTime = False
def solve(letters):
	global runTime
	guess = "".join(letters)
	if guess == "jkeha": runTime = True
	if not runTime: return
	feedback, error = playAbsurdle(guess)
	if feedback != GRAYSQUARE * 5:
		# print(guess, feedback)
		resultFile.write(guess + "\n")

resultFile = open("noAprioriRankings.txt", "w")
for letters in itertools.product(ascii_lowercase, repeat=5):
	solve(letters)
resultFile.close()