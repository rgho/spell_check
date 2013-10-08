# http://norvig.com/spell-correct.html

import re, collections

# takes words, converts to a list, makes all lowercase, 
# strips non alpha chars ("HEY! don't." becomes ['hey','don','t']).
def words(text): return re.findall('[a-z]+', text.lower())

# counts occurances of a list of words.
# ['chess','chess','chess','the','time'] becomes {'the': 2, 'chess': 4, 'time': 2}
def train(features):
     model = collections.defaultdict(lambda: 1)
     for f in features:
         model[f] += 1
     return model

# stores english language frequncies in NWORDS OBJECT by processing
# a big file full of natural english language text.
NWORDS = train(words(file('big.txt').read()))

#define an alphabet
alphabet = 'abcdefghijklmnopqrstuvwxyz'

# generates a list of all word edit distance 1 away from param word.
def edits1(word):
  # this is probably the most brilliant terse, succinct function ive seen.
  # first it computes a splits - list of tuples. it then uses that to make the list
  # of del, trans, repl, insets. then it joins them using set. it doesnt join splits
   
    # splits turns word they into: [('', 'they'), ('t', 'hey'), ('th', 'ey'), ('the', 'y'), ('they', '')]
   splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
   
   #delete turns the splits of they into ['hey', 'tey', 'thy', 'the'] - one char deleted at every spot. 
   deletes    = [a + b[1:] for a, b in splits if b]

   #transpose - flips chars at each pos turns splits of they to:
   # ['htey', 'tehy', 'thye']
   transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
   
   #replace -  replaces with each valid char at each pos. turns splits of they to:
   #['ahey', 'bhey', 'chey', 'dhey', 'ehey', 'fhey', 'ghey', 'hhey', 'ihey', ... ]
   replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
   
   #inserts inserts each char at each pos in the word. turns splits of they to 
   # ['athey', 'bthey', 'cthey', 'dthey', 'ethey', 'fthey', 'gthey', 'hthey', 'ithey', 'jthey' ... ]
   inserts    = [a + c + b     for a, b in splits for c in alphabet]
   return set(deletes + transposes + replaces + inserts)

#since edits1 function generates all strings with edit dist 1 from original word, 
# edits2 uses edits 1 function to generate list of all words two edits from param word
# this represent 98.7 of mistakes. it keeps only those words from this massive set that
# are actually in the dictionary.

def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

def known(words): return set(w for w in words if w in NWORDS)

def correct(word):
    candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
    return max(candidates, key=NWORDS.get)


def main():
  while True:
    testCase = raw_input("Enter a word or Q to quit: ")
    if testCase == 'Q': quit()
    
    correct1 = correct(str(testCase))
    
    print 
    print "You entered: " + testCase
    if testCase == correct1:
        print "Either your word is spelled correctly"
        print "or I couldn't find a replacement!"
    else:
      print "Did you mean: " + correct1 + "?"
    print

main()
