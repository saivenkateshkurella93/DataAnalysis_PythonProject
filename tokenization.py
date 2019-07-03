
#Created on Wed Feb 14 02:13:32 2019

#@author: saivenkateshkurella

import glob
import sys
import time
import html2text
import codecs

path = str(sys.argv[1] + '/*.html')
all_word_freq = {}
timer = []
files=glob.glob(path)
start = time.time()
print('Start Time')
print(start)
#Reading Each file from the directory
for file in files:

    f=codecs.open(file, 'r', errors='ignore', encoding="utf8")
    #f.readlines()
    symbols = '''<>,?%/#@$^&*().“‘’|_~!-{}[]!"'':;""+-'''
    text = html2text.html2text(f.read())
    for char in symbols:
        text=text.replace(char,'')
    all_word_list = text.lower().split(None)
    end = time.time()
    print('End Time')
    print(end)
    f.close()
    # writeFileName = "outputDirectory.txt"
    # writeFile = open(writeFileName, 'w')
    #Creating New .txt file for every .html file
    writeFile = open((file.rsplit(".", 1)[0]) + ".txt", "w", encoding="utf-8")
    # Creating single .txt file for all the tokens sorted by frequency
    sortByFrequency = open(sys.argv[2]+'/sorted_by_frequency.txt', "w", encoding="utf-8")
    # Creating single .txt file for all the tokens sorted by token
    sortByToken = open(sys.argv[2]+'/sorted_by_token.txt', "w", encoding="utf-8")

    word_list = text.lower().split(None)
    word_freq = {}

    for allword in all_word_list:
        all_word_freq[allword] = all_word_freq.get(allword, 0) + 1
    allword_keys = sorted(all_word_freq.keys(), key=all_word_freq.get, reverse=True)
    allword_keys_token = sorted(all_word_freq.keys())
    for allword in allword_keys:
        allword_frequencyCount = all_word_freq[allword]
        sortByFrequency.write(allword)
        sortByFrequency.write('        ')

        sortByFrequency.write(str(allword_frequencyCount))
        sortByFrequency.write('\n')

    for allword in allword_keys_token:
        allword_frequencyCount = all_word_freq[allword]
        sortByToken.write(allword)
        sortByToken.write('        ')

        sortByToken.write(str(allword_frequencyCount))
        sortByToken.write('\n')

    for word in word_list:
        word_freq[word] = word_freq.get(word, 0) + 1
    keys = sorted(word_freq.keys(), key=word_freq.get, reverse=True)
    for word in keys:
        # print("%-10s %d" % (word, word_freq[word]))
        frequencyCount = word_freq[word]
        writeFile.write(word)
        writeFile.write('        ')

        writeFile.write(str(frequencyCount))
        writeFile.write('\n')
    print('Total Time Taken to Parse:')
    print("--- %s seconds ---" % (time.time() - start))

    writeFile.close()
    sortByFrequency.close()
    sortByToken.close()
