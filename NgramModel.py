import sys
import re
import argparse
import random
import io
import math

parser = argparse.ArgumentParser()
parser.add_argument("-aone", "--addone", action="store_true", default=False, help="Use plus-one smoothing")
parser.add_argument("-perp", "--perplexity", action="store_true", default=False, help="Calculate perplexity of the test set")
parser.add_argument("-top", default = 10 , type=int, help="generate top given numbers of uinigrams biograms")
parser.add_argument("-gsent", "--gensent", default=0, type=int, help="Option to generate given number of sentences")
parser.add_argument("-trainData", default="./corpora/trump80.txt", help="traininging data file location")
parser.add_argument("-testData", default="./corpora/trump20.txt", help = "test data file location")

args = parser.parse_args()

class Word():
	"""docstring for Word"""
	def __init__(self, word):
		self.nextWords = []
		self.word = word
		self.occurances = 0

trainingWordDict = {"WordKey": Word("WordKey")}
testWordDict = {"WordKey": Word("Wordkey")}

# add new word to trainingWordDict if unique
# if word in dict already, increment occurances
# push next word 
# trainingFile, the io stream; dictionary, the dict to fill
# TODO: fix miscounts for ending characters
def fillDict(trainingFile, dictionary):

	location = "./corpora/trump.txt"
	train = trainingFile #80precent corpus
	numberOfWords = 0;
	currWord = "" 
	lastWord = ""  #not supposed to be int
	isLastWord = False
	for line in train:
		currLine = line.split()
		for i in range(0,len(currLine)):
			currWord = currLine[i]
			nextWord = ""
			if (i<len(currLine)-1):
				if(isLastWord): 
				# if word is last in the line, save for next iteration of loop and use first word in that iteration 
					nextWord = currWord
					isLastWord = False
					# print("at last word")
					if (lastWord not in dictionary):
						# print(lastWord.word)
						newWord = Word(lastWord)
						newWord.nextWords.append(currWord)
						dictionary[lastWord] = Word(currWord)
					else:
						dictionary[lastWord].occurances += 1
						dictionary[lastWord].nextWords.append(currWord)
					continue
				nextWord = currLine[i+1]
				re.sub("(\u2018|\u2019|\u2014|\u2013|\u2026|\ufffd)", " ", currWord)
				if (currWord not in dictionary):
					if (currWord == "Henry"):
						print("next index ", currLine[i+1])
						print("next word ", nextWord)
					newWord = Word(currWord)
					newWord.nextWords.append(nextWord)
					
				else:
					dictionary[currWord].occurances = dictionary[currWord].occurances + 1
					dictionary[currWord].nextWords.append(nextWord)

			else:
				isLastWord = True
				lastWord = currWord

				
	dictionary.pop("WordKey")

def getVocabSize(traindict, testdict): #TODO: figure out what the vocabulary is 
	trainSet = set(traindict.items())
	testSet = set(testdict.items())
	vocabSet = trainSet ^ testSet
	return len(vocabSet)

# generates bigraom on probabilistic model 
# NOTE: if givenword has no succeeding word (e.g. last word of a file), will cause index out of bounds
def generateBigram(givenWord):
	#print(givenWord)
	word1 = trainingWordDict[givenWord]
	if (len(word1.nextWords) == 1):
		# print("only one occurance")
		# print(word1.nextWords)
		word2 = word1.nextWords[0]
	elif (len(word1.nextWords) == 0):
		pass;
	else:
		randNum = random.randint(0,len(word1.nextWords)) - 1
		# print(len(word1.nextWords))
		# print("rand int= ", randNum)
		word2 = word1.nextWords[randNum]
	# print(word1.word)
	# print(word2)
	# print("done\n")
	return word2

def generateSent(givenWord, sentLen, numSent):
	sentList = []
	for i in range(0, numSent):
		sentence = givenWord + " "
		nextWord = givenWord
		for j in range(1, sentLen):
			nextWord = generateBigram(nextWord)
			sentence += nextWord + " "
		sentList.append(sentence)	
	return sentList

# read corpus data from corpusData txt files
# @training, the training metadata, 
# @test, the test metadata
def compare2080(training, test):
	corpData = open(dataLoc, "w+", encoding="utf-8")
	numberOfWords = int(corpData.readline())
	vocabularySize = int(corpData.readline())
	dataArray = [numberOfWords, vocabularySize]
	print(dataArray)
	return

# generate the random number line to pick first word
def genRandWordLine(dictionary, plusOne):
	WordLine = []
	for key in iter(dictionary): # iterate over values in dict 
		value = dictionary[key]
		if (value.occurances == 0 and plusOne):
			# print("plus one-ing")
			value.occurances +=1
		for i in range(0, value.occurances):
			WordLine.append(value)
	return WordLine

# after random number line made, pick the word at random
# returns a Word object
def getFirstWord(wordsList):
	ind = random.randint(0, len(wordsList))
	return wordsList[ind]

def main():

	trainFile = open(args.trainData, "r",  encoding="utf-8-sig")
	testFile = open(args.testData, "r", encoding="utf-8-sig")
	numberOfWords = 0 #WARNING: HARD CODED NUMBER
	varWord = "Mexico"
	givenString = "been"
	givenStringCount = 0
	NgramCount = 0 # C sub i
	vocabularySize = 0;
	plusOne = True
	Ngram = varWord + " " + givenString
	vocabularySize = getVocabSize(trainingWordDict, testWordDict)
	print("vocab size is ", vocabularySize)
	fillDict(trainFile, trainingWordDict)
	fillDict(testFile, testWordDict)
	randWordLine = genRandWordLine(trainingWordDict, args.addone)
	
	# tempWord = trainingWordDict["know"]
	# #print("temp Word ", tempWord.word, tempWord.occurances, tempWord. nextWords)
	# tempWord = trainingWordDict["Henry"]
	# print("temp Word ", tempWord.word, tempWord.occurances, tempWord. nextWords)
	if (args.gensent > 0):
		# for i in range(0, args.gensent):
		firstWord = getFirstWord(randWordLine).word #firstword a string
		sentence = generateSent(firstWord, 10, args.gensent) # sentence 
		print("Sentence Generated\n", sentence)
	corpusValues=[]
	if (args.topten):
		for key in iter(trainingWordDict):
			corpusValues.append(trainingWordDict[key])
		corpusValues.sort(key = lambda x: x.occurances)
		greatestVal = corpusValues[len(corpusValues)-1].occurances
	
		topTenList = []

		for i in range(len(corpusValues)-10, len(corpusValues)):
			word = corpusValues[i] 
			topTenList.append(corpusValues[i])
			print("Top bi grams for ", word.word)
			for i in range(0,10):
				print("\t", word.nextWords[i])

	if (args.perplexity):
		biGramCount = 0;
		unigramCount = 0;
		perplex = 0;
		for wordObj in trainingWordDict.values():
			w1 = wordObj
			w1Str = wordObj.word
			# print("working.....", w1.word)
			wordList = w1.nextWords
			unigramCount += wordObj.occurances
			if (unigramCount == 0):
				print("\tuni is 0")
				unigramCount = 1
			for i in range(0, len(wordList)):
				w2 = wordList[i]
				uniGramProd = 0
				biGramProd = 1
				for j in range(i, len(wordList)): 
					if (wordList[j] == wordList[i]):
						biGramCount += 1 
				# biGramProd *= biGramCount	
				if (args.addone):
					perplex += math.log((biGramCount+1)/ len(trainingWordDict) + vocabularySize)
				else:
					perplex += math.log(biGramCount/(unigramCount)) 
				#biGramProd/math.pow(unigramCount, len(wordList))		
		# adjustedCount = (NgramCount + 1) /(numberOfWords + vocabularySize)
		# print("adjustedCount", adjustedCount)
		if(args.addone):
			print("With add one prob, perplex is = ", perplex)
		else:
			print("no add one prob, perplex is = ", perplex)

	trainFile.close()
	testFile.close()

if __name__ == "__main__": main()


#C = N(C+1)/(N+V)