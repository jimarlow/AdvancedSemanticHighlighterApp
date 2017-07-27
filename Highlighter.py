import os, glob

HIGHLIGHTER_EXT = '.hil'

class Highlighter:
    def __init__(self, fname, name='Test', foreground='white', background='red'):
        self.fname = fname
        self.name = name
        self.foreground = foreground
        self.background = background
        self.terms = []
        self.load()

    def addTerm(self, term):
        if self.containsTerm(term):return # No duplicates allowed
        self.terms.append(term)
        self.terms.sort()

    def removeTerm(self, term):
        try:
            self.terms.remove(term)
        except ValueError:
            pass

    def containsTerm(self, term):
        return term in self.terms

    def save(self):
        try:
            with open(self.fname, 'w') as f:
                f.write(self.name + '\n')
                f.write(self.foreground + '\n')
                f.write(self.background + '\n')
                for line in self.terms:
                    f.write(line + '\n')
        except Exception as e:
            print("Highlihgter file save error: ", e)

    def load(self):
        try:
            with open(self.fname, 'r') as f:
                lines = f.readlines()
                self.name = lines[0].strip()
                self.foreground = lines[1].strip()
                self.background = lines[2].strip()
                for line in lines[3:]:
                    self.addTerm(line.strip())
        except Exception as e:
            print("Highlihgter file load error: ",e)

    def __str__(self):
        return "Class Highlighter fname: " + self.fname


# Find all of the .hil files in the specified directory and for each one
# create a Highlighter
class HighlighterSet:
    def __init__(self, directory):
        self.path = os.path.join(directory, '*' + HIGHLIGHTER_EXT)
        self.files = glob.glob(self.path)
        self.highlighters = {}
        for f in self.files:
            h = Highlighter(f)
            self.highlighters[h.name] = h

    @property
    def highlighterNames(self):
        return list(self.highlighters.keys())

    def getHighlighter(self, name):
        return self.highlighters[name]

    def __str__(self):
        ret = "Class HighlighterSet directory: " + self.directory + ", path: " + self.path + ", files: "
        for file in self.files:
            ret = ret + "\n" + file
        return ret


if __name__ == '__main__':
    # The test project is just for testing - do what you want with it
    TESTProjectDir = os.path.join(os.getcwd(), 'TESTProject')
    print(TESTProjectDir)
    hiSet = HighlighterSet(TESTProjectDir)
    for f in hiSet.highlighters.values():
        print(f)
    print(hiSet.highlighterNames)
