import multiprocessing
import psutil
from absurdle import playAbsurdle, GREENSQUARE

def chunks(l, n):
	""" Yield n successive chunks from l.
	"""
	newn = int(len(l) / n)
	for i in range(0, n-1):
		yield l[i*newn:i*newn+newn]
	yield l[n*newn-newn:]


def solve(wordBank: set, maxDepth, depth, depth0Results, realWordBank = set()) -> list:
	if depth == 0:
		depth0SolvedWords = 0
	# base case
	if len(wordBank) == 1:
		return (0, list(wordBank))
	# max depth protection
	if depth >= maxDepth:
		return (-1, [])

	# best variables
	shortestMoveCount = maxDepth
	shortestWords = []

	for guess in wordBank:
		# main function invocation
		feedback, newWordBank, error = playAbsurdle(guess, realWordBank if depth == 0 else wordBank)
		# all correct base case?
		if feedback == GREENSQUARE * 5:
			return (0, [guess])
		newMoveCount, newWords = solve(newWordBank, depth + shortestMoveCount, depth + 1, depth0Results)
		if depth == 0:
			depth0SolvedWords += 1
			depth0Results.append(newMoveCount + 1)
			print(f"process id: {psutil.Process().pid} depth 0 solved word: {guess} solved total {depth0SolvedWords}")
		if newMoveCount == -1: continue
		if newMoveCount < shortestMoveCount - 1:
			shortestMoveCount = newMoveCount + 1
			shortestWords = [guess] + newWords
	return (shortestMoveCount, shortestWords)


MULTITHREAD = True
if __name__ == "__main__":
	mystery_words_file = open("absurdle_mystery_words.txt", "r")
	mysteryWordBank = mystery_words_file.read().splitlines()
	if MULTITHREAD:
		pool = multiprocessing.Pool(processes=7)
		args = []
		depth0Results = multiprocessing.Manager().list()
		for subWordBank in chunks(mysteryWordBank[0:294], 7):
			args.append((subWordBank, float("inf"), 0, depth0Results, set(mysteryWordBank)))
		results = pool.starmap(solve, args)
	else:
		results = []

	# logging results
	print(results)
	resultsFile = open("results.txt", "w")
	resultsFile.write(str(results) + "\n" + str(depth0Results))
	resultsFile.close()