from tkinter import *
from tkinter.ttk import *
from nltk.corpus import wordnet as wn
import nltk
from nltk import word_tokenize
from inflection import *

# This application uses Princeton WordNet
# Citation:
# Princeton University "About WordNet." WordNet. Princeton University. 2010.
# http://wordnet.princeton.edu

# Requires the following libraries to be installed:
#
# NLTK: http://www.nltk.org
#   http://www.nltk.org/install.html
#   pip3 install -U nltk
#   pip3 install -U numpy
#
# NLTK Data:
#   http://www.nltk.org/data.html
#   After installing NLTK run Python 3
#   >> import nltk
#   >> nltk.download()
#   When prompted, install everything
#
# Inflection:
#   https://inflection.readthedocs.io/en/latest/
#   pip3 install -U inflection


# Plain English dictionary for the Penn Treebank tag set.
# https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
# http://www.comp.leeds.ac.uk/amalgam/tagsets/upenn.html
PENN_TREEBANK_POS_TAGS = {'CC': 'Coordinating conjunction',
                          'CD': 'Cardinal number',
                          'DT': 'Determiner',
                          'EX': 'Existential there',
                          'FW': 'Foreign word',
                          'IN': 'Preposition or subordinating conjunction',
                          'JJ': 'Adjective',
                          'JJR': 'Adjective, comparative',
                          'JJS': 'Adjective, superlative',
                          'LS': 'List item marker',
                          'MD': 'Modal',
                          'NN': 'Noun, singular or mass',
                          'NNS': 'Noun, plural',
                          'NNP': 'Proper noun, singular',
                          'NNPS': 'Proper noun, plural',
                          'PDT': 'Predeterminer',
                          'POS': 'Possessive ending',
                          'PRP': 'Personal pronoun',
                          'PRP$': 'Possessive pronoun',
                          'RB': 'Adverb',
                          'RBR': 'Adverb, comparative',
                          'RBS': 'Adverb, superlative',
                          'RP': 'Particle',
                          'SYM': 'Symbol',
                          'TO': 'to',
                          'UH': 'Interjection',
                          'VB': 'Verb, base form',
                          'VBD': 'Verb, past tense',
                          'VBG': 'Verb, gerund or present participle',
                          'VBN': 'Verb, past participle',
                          'VBP': 'Verb, non-3rd person singular present',
                          'VBZ': 'Verb, 3rd person singular present',
                          'WDT': 'Wh-determiner',
                          'WP': 'Wh-pronoun',
                          'WP$': 'Possessive wh-pronoun',
                          'WRB': 'Wh-adverb'}


# Python 3 needs a built in flatten function!!!!!
# You can't do functional programming properly without one.
def flatten(l):
    if l == []:
        return []
    else:
        return flatten(l[0]) + (flatten(l[1:]) if len(l) > 1 else []) if type(l) is list else [l]


# Gets the word out of a Synset
def synsetWord(synset):
    return synset.lemmas()[0].name()


class WordAnalysis:
    def __init__(self, word):
        self.word = word
        self.singular = singularize(word)
        self.plural = pluralize(word)
        self.synsets = wn.synsets(word)
        self.numSynsets = len(self.synsets)

    @property
    def synonyms(self, i=0):
        try:
            return self.synsets[i].lemma_names()
        except:
            return []

    @property
    def hyponyms(self, i=0):
        try:
            return flatten([s.lemma_names() for s in self.synsets[i].hyponyms()])
        except:
            return []

    @property
    def hypernyms(self, i=0):
        try:
            return flatten([s.lemma_names() for s in self.synsets[i].hypernyms()])
        except:
            return []

    @property
    def definition(self, i=0):
        try:
            return self.synsets[i].definition()
        except:
            return 'Not in WordNet'

    @property
    def definitions(self):
        try:
            return [synsetWord(s) + ": " + s.definition() for s in self.synsets]

        except:
            return 'Not in WordNet'

    @property
    def pos(self):
        w, tag = nltk.pos_tag([self.word])[0]
        return PENN_TREEBANK_POS_TAGS[tag]


class TextAnalysis:
    def __init__(self, text):
        self.text = text
        self.words = word_tokenize(text)
        self.analyzedText = nltk.Text(self.words)
        self.analyzedWords = map(WordAnalysis, self.words)


# TextAnalysisTreeview is a specialized Treeview that shows Word Net information for some text.
# This is a very good example of appropriate use of multiple inheritance.
# Treeview is a TkInter widget, and TextAnalysis is a simple interface to NLTK (specifically, WordNet).
# Both classes are completely orthogonal and have no overlapping attributes or operations. We can combine them safely.
class TextAnalysisTreeview(TextAnalysis, Treeview):
    def __init__(self, root, text):
        TextAnalysis.__init__(self, text)
        Treeview.__init__(self, root)
        self.root = root
        treeRootIndex = 1
        for aw in self.analyzedWords:
            # The word is the root of the tree
            treeRoot = self.insert("", treeRootIndex, text=aw.word)
            treeRootIndex += 1

            # self.insert(treeRoot, 2, text=aw.definition)
            for i, d in enumerate(aw.definitions):
                self.insert(treeRoot, treeRootIndex, text="%d: %s" % (i, d))
                treeRootIndex += 1

            self.insert(treeRoot, treeRootIndex, text=aw.pos)
            treeRootIndex += 1

            inflectionsRoot = self.insert(treeRoot, treeRootIndex, text="Inflections")
            treeRootIndex += 1
            self.insert(inflectionsRoot, 1, text='Singular: ' + aw.singular)
            self.insert(inflectionsRoot, 2, text='Plural: ' + aw.plural)

            synonymsRoot = self.insert(treeRoot, treeRootIndex, text="Synonyms")
            treeRootIndex += 1
            for i, s in enumerate(aw.synonyms):
                self.insert(synonymsRoot, i, text=s)

            hypernymsRoot = self.insert(treeRoot, treeRootIndex, text="Hypernyms")
            treeRootIndex += 1
            for i, s in enumerate(aw.hypernyms):
                self.insert(hypernymsRoot, i, text=s)

            hyponymsRoot = self.insert(treeRoot, treeRootIndex, text="Hyponyms")
            treeRootIndex += 1
            for i, s in enumerate(aw.hyponyms):
                self.insert(hyponymsRoot, i, text=s)


# A child window that shows WordNet information for some text
class WordNetInfoWindow(Toplevel):
    def __init__(self, text):
        Toplevel.__init__(self)
        self.title('WordNet Information')
        TextAnalysisTreeview(self, text).pack(fill=BOTH, expand=True)


# A parent window to test the WordNetInfoWindow
class WordNetInfoWindowTestWindow(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        t = StringVar()
        t.set('cognitive dog')
        Entry(self, textvariable=t).pack(fill='x')
        Button(self,
               text="Analyze text using WordNet",
               command=lambda: WordNetInfoWindow(t.get())).pack(side="top")
        self.pack(side="top", fill="both", expand=True)


if __name__ == '__main__':
    t = TextAnalysis('no cats and dogs')
    print(t.words)
    print(t.analyzedText)
    for aw in t.analyzedWords:
        print(aw.singular)
        print(aw.plural)
        print(aw.hyponyms)
        print(aw.hypernyms)
        print(aw.synonyms)
        print(aw.definition)
        for i, d in enumerate(aw.definitions):
            print("%d: %s" % (i, d))
        print(aw.pos)

    root = Tk()
    main = WordNetInfoWindowTestWindow(root)
    root.mainloop()
