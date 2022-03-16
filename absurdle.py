from collections import defaultdict
from random import choice as randomChoice
GREENSQUARE, YELLOWSQUARE, GRAYSQUARE = "🟩", "🟨", "⬛"

memo = {}
def generateFeedback(guessWord, correctWord):
    if (guessWord, correctWord) in memo:
        return memo[(guessWord, correctWord)]

    feedback = [GRAYSQUARE for i in range(5)]
    yellowFeedbackUnusedLetters = list(correctWord)
    for i, (guessWordLetter, correctWordLetter) in enumerate(zip(list(guessWord), list(correctWord))):
        if guessWordLetter == correctWordLetter:
            feedback[i] = GREENSQUARE
            yellowFeedbackUnusedLetters.remove(correctWordLetter)
    for i, (guessWordLetter, correctWordLetter) in enumerate(zip(list(guessWord), list(correctWord))):
        if guessWordLetter in yellowFeedbackUnusedLetters and feedback[i] != GREENSQUARE:
            feedback[i] = YELLOWSQUARE
            yellowFeedbackUnusedLetters.remove(guessWordLetter)
    
    stringFeedback = "".join(feedback)
    memo[(guessWord, correctWord)] = stringFeedback
    return stringFeedback

def allLargestBuckets(buckets):
    largestBucketSize = 0
    largestBucketVals = []
    for bucketFeedback in buckets:
        if len(buckets[bucketFeedback]) > largestBucketSize:
            largestBucketSize = len(buckets[bucketFeedback])
            largestBucketVals = [bucketFeedback]
        elif len(buckets[bucketFeedback]) == largestBucketSize:
            largestBucketVals.append(bucketFeedback)
    
    # more adversarial
    if len(largestBucketVals) >= 2:
        if GREENSQUARE * 5 in largestBucketVals:
            largestBucketVals.remove(GREENSQUARE * 5)

    # feedback
    if len(largestBucketVals) >= 2 and __name__ == "__main__":
        print(f"Multiple largest buckets, choosing between {len(largestBucketVals)}")
        print("\n".join([f"{val}: {', '.join(buckets[val])}" for val in largestBucketVals]))
    
    return largestBucketVals

def playAbsurdle(guess: str, wordbank: set) -> str:
    if len(guess) != 5:
        if __name__ == "__main__": print("Bad input. Try again.")
        return ("", wordbank, True)

    buckets = defaultdict(set)
    for word in wordbank:
        buckets[generateFeedback(guess, word)].add(word)
    
    # largest bucket calculations
    largestBucketVal = randomChoice(allLargestBuckets(buckets))
    largestBucket = buckets[largestBucketVal]
    if __name__ == "__main__":
        [print(f"{feedback}: {word}") for feedback, word in sorted([(feedback, len(words)) for feedback, words in buckets.items()], key=lambda x: x[1], reverse=True)]
        print(largestBucketVal, " ".join(sorted(list(largestBucket))))
    
    return (largestBucketVal, largestBucket, False)

if __name__ == "__main__":
    # local wordbank
    mystery_words_file = open("absurdle_mystery_words.txt", "r")
    wordbank = set(mystery_words_file.read().splitlines())
    while True:
        feedback, wordbank, error = playAbsurdle(input("Guess a word: "), wordbank)
        if feedback == GREENSQUARE * 5:
            print("You win!")
            more = input("Continue? (y/n) ")
            if more == "n": break
            mystery_words_file = open("absurdle_mystery_words.txt", "r")
            wordbank = set(mystery_words_file.read().splitlines())