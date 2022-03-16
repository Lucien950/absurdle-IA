from absurdle import GRAYSQUARE, GREENSQUARE, YELLOWSQUARE, playAbsurdle
def conformFeedback(guess:str, feedback: str, wordbank:set):
   newWordBank = set()
   for word in wordbank:
      good = True
      wordLetters = list(word)

      for guessLetter, wordLetter, feedbackVal in zip(list(guess), list(word), feedback):
         if feedbackVal == GREENSQUARE:
            if guessLetter == wordLetter:
               wordLetters.remove(guessLetter) # which is also wordLetter
            else:
               good = False
               break
      if not good: continue
      for guessLetter, wordLetter, feedbackVal in zip(list(guess), list(word), feedback):
         if feedbackVal == YELLOWSQUARE and guessLetter in wordLetters and guessLetter != wordLetter:
            wordLetters.remove(guessLetter)
         elif (feedbackVal == GRAYSQUARE and guessLetter != wordLetter and guessLetter not in wordLetters):
            pass
         # alredy checked
         elif feedbackVal == GREENSQUARE:
            pass
         else:
            good = False
            break
      if good:
         newWordBank.add(word)
   return newWordBank

def solve(wordbank: set, engineWordbank: set, maxdepth = float("inf"), depth = 0) -> list:
   # base case
   if len(wordbank) == 1:
      return (0, list(wordbank))	

   shortestInterval = maxdepth
   shortestIntervalWords = []
   if depth >= maxdepth:
      return (-1, [])
   for guess in wordbank:
      feedback, localengineWordBank, error = playAbsurdle(guess, engineWordbank)
      # all correct base case?
      if feedback == GREENSQUARE * 5:
         return (0, [guess])
      localwordbank = conformFeedback(guess, feedback, wordbank)
      solveInterval, solveWords = solve(localwordbank, localengineWordBank, depth + shortestInterval, depth + 1)
      if depth == 0:
         print(solveInterval, solveWords)
      if solveInterval == -1: continue
      if solveInterval < shortestInterval:
         shortestInterval = solveInterval + 1
         shortestIntervalWords = [guess] + solveWords
   
   return (shortestInterval, shortestIntervalWords)

guessable_words_file = open("guessable_words.txt", "r")
wordbank = set(guessable_words_file.read().splitlines())
mystery_words_file = open("absurdle_mystery_words.txt", "r")
allEngineWordBank = set(mystery_words_file.read().splitlines())
solve(wordbank, allEngineWordBank)