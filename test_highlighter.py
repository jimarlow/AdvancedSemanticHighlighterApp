from Highlighter import *
import unittest

class TestHighlighter(unittest.TestCase):
    def setUp(self):
        self.TESTDIR = os.path.join(os.getcwd(), 'TESTProject')
        self.TEST_LOAD_HIGHLIGHTER = os.path.join(self.TESTDIR, 'TESTLoadHighlighter.hil')
        self.TEST_SAVE_HIGHLIGHTER = os.path.join(self.TESTDIR, 'TESTSaveHighlighter.hil')
        self.LOAD_NAME = 'TEST Highlighter'
        self.SAVE_NAME = 'TEST Save Highlighter'
        self.FOREGROUND = 'blue'
        self.BACKGROUND = 'yellow'
        self.TERM_A = 'a term'
        self.TERM_B = 'b term'
        self.TERM_C = 'c term'
        self.TERMS = [self.TERM_B, self.TERM_C, self.TERM_A] # Out of order to test sorting
        # Set up the test file
        try:
            with open(self.TEST_LOAD_HIGHLIGHTER, 'w') as f:
                f.write(self.LOAD_NAME + '\n')
                f.write(self.FOREGROUND + '\n')
                f.write(self.BACKGROUND + '\n')
                f.write(self.TERM_A + '\n')
                f.write(self.TERM_B + '\n')
                f.write(self.TERM_C + '\n')
        except Exception as e:
            print("Test highlighter file setup error: ", e)

    def test_addTerm(self):
        h = Highlighter(self.TEST_LOAD_HIGHLIGHTER)
        h.addTerm(self.TERM_B)
        h.addTerm(self.TERM_C)
        h.addTerm(self.TERM_A)
        # Terms are added in alphabetical order
        self.assertEqual(h.terms, [self.TERM_A, self.TERM_B, self.TERM_C])

    def test_removeTerm(self):
        h = Highlighter(self.TEST_LOAD_HIGHLIGHTER)
        # Make test independent of Load
        h.terms = [self.TERM_A, self.TERM_B, self.TERM_C]
        h.removeTerm(self.TERM_B)
        self.assertEqual(h.terms, [self.TERM_A, self.TERM_C])

    def test_containsTerm(self):
        h = Highlighter(self.TEST_LOAD_HIGHLIGHTER)
        # Make test independent of Load
        h.terms = [self.TERM_A, self.TERM_B, self.TERM_C]
        self.assertTrue(h.containsTerm(self.TERM_C))

    def test_save(self):
        h = Highlighter(self.TEST_SAVE_HIGHLIGHTER, load=False) # Don't autoload
        h.name = self.SAVE_NAME
        h.foreground = self.FOREGROUND
        h.background = self.BACKGROUND
        h.terms = self.TERMS
        h.save()
        try:
            with open(self.TEST_SAVE_HIGHLIGHTER, 'r') as f:
                lines = f.readlines()
                self.assertEqual(lines[0].strip(), self.SAVE_NAME)
                self.assertEqual(lines[1].strip(), self.FOREGROUND)
                self.assertEqual(lines[2].strip(), self.BACKGROUND)
                # Terms should now be in order
                self.assertEqual(lines[3].strip(), self.TERMS[0])
                self.assertEqual(lines[4].strip(), self.TERMS[1])
                self.assertEqual(lines[5].strip(), self.TERMS[2])
        except Exception as e:
            self.fail()

    def test_load(self):
        h = Highlighter(self.TEST_LOAD_HIGHLIGHTER)
        self.assertEqual(h.name, self.LOAD_NAME)
        self.assertEqual(h.foreground, self.FOREGROUND)
        self.assertEqual(h.background, self.BACKGROUND)

if __name__ == "__main__":
    unittest.main()