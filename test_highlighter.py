from Highlighter import *
import unittest

TESTDIR= os.path.join(os.getcwd(), 'TESTProject')
TEST_LOAD_HIGHLIGHTER = os.path.join(TESTDIR, 'TESTLoadHighlighter.hil')
TEST_SAVE_HIGHLIGHTER = os.path.join(TESTDIR, 'TESTSaveHighlighter.hil')
TERM_A = 'a term'
TERM_B = 'b term'
TERM_C = 'c term'

class TestHighlighter(unittest.TestCase):
    def test_addTerm(self):
        h = Highlighter(TEST_LOAD_HIGHLIGHTER)
        h.addTerm(TERM_B)
        h.addTerm(TERM_C)
        h.addTerm(TERM_A)
        # Terms are added in alphabetical order
        self.assertEqual(h.terms, [TERM_A, TERM_B, TERM_C])

    def test_removeTerm(self):
        h = Highlighter(TEST_LOAD_HIGHLIGHTER)
        h.terms = [TERM_A, TERM_B, TERM_C]
        h.removeTerm(TERM_B)
        self.assertEqual(h.terms, [TERM_A, TERM_C])

    def test_containsTerm(self):
        def test_removeTerm(self):
            h = Highlighter(TEST_LOAD_HIGHLIGHTER)
            h.terms = ['a', 'b', 'c']
            self.assertTrue(h.containsTerm('b'))

    def test_save(self):
        name = 'TEST save highlighter'
        foreground = 'white'
        background = 'blue'
        terms = ['a','b', 'c']
        h = Highlighter(TEST_SAVE_HIGHLIGHTER, name, foreground, background)
        h.terms = terms
        h.save()
        try:
            with open(TEST_SAVE_HIGHLIGHTER, 'r') as f:
                lines = f.readlines()
                self.assertEqual(lines[0].strip(), name)
                self.assertEqual(lines[1].strip(), foreground)
                self.assertEqual(lines[2].strip(), background)
                self.assertEqual(lines[3].strip(), terms[0])
                self.assertEqual(lines[4].strip(), terms[1])
                self.assertEqual(lines[5].strip(), terms[2])
        except Exception as e:
            self.fail()

    def test_load(self):
        h = Highlighter(TEST_LOAD_HIGHLIGHTER)
        self.assertEqual(h.name, 'TEST Highlighter')
        self.assertEqual(h.foreground, 'blue')
        self.assertEqual(h.background, 'yellow')

if __name__ == "__main__":
    unittest.main()