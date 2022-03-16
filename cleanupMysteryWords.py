absurdle_mystery_words_file = open("absurdle_mystery_words.txt", "r")
absurdle_mystery_words = [i.lower() for i in absurdle_mystery_words_file.read().splitlines()]

absurdle_mystery_words_file_new = open("absurdle_mystery_words_new.txt", "w")
absurdle_mystery_words_file_new.write("\n".join(absurdle_mystery_words))