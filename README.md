# NgramModeling
Provides perplexity calcuation of a text corpus and generates likely sentences based on the corpus   

Usage
$ py NgramModel.py 
usage: NgramModel.py [-h] [-aone] [-perp] [-topten TOPTEN] [-gsent GENSENT]
                     [-trainData TRAINDATA] [-testData TESTDATA
optional arguments:
  -h, --help            show this help message and exit
  -aone, --addone       Use plus-one smoothing
  -perp, --perplexity   Calculate perplexity of the test set
  -topten TOPTEN        generate top 5 uinigrams biograms
  -gsent GENSENT, --gensent GENSENT
                        Option to generate sentences
  -trainData TRAINDATA  traininging data file location
  -testData TESTDATA    test data file location
Potential Errors:
Add one smoothing option for module increases the perplexity 
