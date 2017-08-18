from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfilename
from Highlighter import *
from NLTKWordAnalysis import *

DEFAULT_TAG = 'findAll'


class HighlightText(Text):
    def __init__(self, *args, **kwargs):
        Text.__init__(self, *args, **kwargs)
        # Set a default tag
        self.tag_configure(DEFAULT_TAG, foreground='white', background='red')

    # Tags the items given in the textList
    def tagAllList(self, textList, tag=DEFAULT_TAG):
        for t in textList:
            # print(t)
            self.tagAll(t, tag)

    def clearTags(self):
        for tag in self.tag_names():
            self.tag_delete(tag)

    def tagAll(self, text, tag=DEFAULT_TAG):
        start = self.index("1.0")
        end = self.index("end")

        self.mark_set("matchStart", start)
        self.mark_set("matchEnd", start)
        self.mark_set("searchLimit", end)

        count = IntVar()
        while True:
            index = self.search(text, "matchEnd", "searchLimit", count=count, regexp=False)
            if index == "": break
            if count.get() == 0: break  # matches zero-length strings
            self.mark_set("matchStart", index)
            self.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
            self.tag_add(tag, "matchStart", "matchEnd")


class AdvancedSemanticHighlighterApp(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.pack(fill=BOTH, expand=True)
        self.master.title('Advanced semantic highlighter')
        self.initUI()

        self.fname = None
        self.highlighterSet = None
        self.currentHighlighter = None

    def initUI(self):
        # The text frame
        textFrame = Frame(self, borderwidth=2, relief=GROOVE)
        textFrame.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=5)

        # The text
        self.text = HighlightText(textFrame, height=26, width=50, wrap=WORD)
        self.text.bind("<Key>", lambda e: "break")  # Make read only by rebinding keys
        self.text.pack(side=BOTTOM, fill=BOTH, expand=True)

        # The frame for the buttons operating on the text
        textButtonFrame = Frame(textFrame)
        textButtonFrame.pack(side=TOP, fill=X)

        # The loadTextButton
        loadTextButton = Button(textButtonFrame, text="Load text", command=self.loadText)
        loadTextButton.pack(side=LEFT, padx=5, pady=5)

        # The highlightSelectionButton
        highlightSelectionButton = Button(textButtonFrame, text="Highlight selection", command=self.highlightSelection)
        highlightSelectionButton.pack(side=LEFT, padx=5, pady=5)

        # The highlighterFrame
        highlighterFrame = Frame(self, borderwidth=2, relief=GROOVE)
        highlighterFrame.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=5)

        # The highlighterComboBox
        self.highlighterCombobox = Combobox(highlighterFrame, state='readonly')
        self.highlighterCombobox.bind("<<ComboboxSelected>>", self.comboboxSelection)
        self.highlighterCombobox.pack(side=TOP, padx=5, pady=5)

        # The removeSelectedTermButton
        removeSelectedTermButton = Button(highlighterFrame, text="Remove selected term",
                                          command=self.removeSelectedTerm)
        removeSelectedTermButton.pack(side=BOTTOM, padx=5, pady=5)

        # The exploreSelectedTermButton
        exploreSelectedTermButton = Button(highlighterFrame, text="Explore selected term",
                                           command=self.exploreSelectedTerm)
        exploreSelectedTermButton.pack(side=BOTTOM, padx=5, pady=5)

        # The termListBox
        self.termListBox = Listbox(highlighterFrame)
        self.termListBox.configure(exportselection=False)  # Ensure it keeps it's selection
        self.termListBox.pack(side=TOP, fill=BOTH, expand=True)
        self.termListBox.bind('<ButtonRelease-1>', self.termListBoxItemSelected)

    @property
    def selectedTerm(self):
        try:
            return self.termListBox.get(self.termListBox.curselection()[0])
        except:
            return None

    def termListBoxItemSelected(self, evt):
        # We are going to change another control, so we have to set termListBox to DISABLED to preserve its state
        self.termListBox.configure(state=DISABLED)
        self.showCurrentHighlighter()
        self.text.tagAll(self.selectedTerm, 'selectedTerm')
        # OK - put termListBox back to NORMAL
        self.termListBox.configure(state=NORMAL)

    def removeSelectedTerm(self):
        if self.selectedTerm:
            self.currentHighlighter.removeTerm(self.selectedTerm)
            self.showCurrentHighlighter()
            self.currentHighlighter.save()

    def exploreSelectedTerm(self):
        if self.selectedTerm:
            WordNetInfoWindow(self.selectedTerm)

    def showCurrentHighlighter(self):
        if self.currentHighlighter:
            # Empty the Listbox
            self.termListBox.delete(0, END)
            # Populate the Listbox
            for t in self.currentHighlighter.terms:
                self.termListBox.insert(END, t)

            # Set up the highlighter and selectedTerm tags for the Text widget
            self.text.clearTags()  # First, clear all existing tags
            # Add the new tag for the currentHighlighter
            self.text.tag_configure(self.currentHighlighter.name, foreground=self.currentHighlighter.foreground,
                                    background=self.currentHighlighter.background)
            # Add the selectedTerm tag which is just the inverse of the highlighter tag
            self.text.tag_configure('selectedTerm', foreground=self.currentHighlighter.background,
                                    background=self.currentHighlighter.foreground)

            # Highlight the list of terms
            self.text.tagAllList(self.currentHighlighter.terms, self.currentHighlighter.name)

    def comboboxSelection(self, event):
        # Set the current Highlighter
        self.currentHighlighter = self.highlighterSet.getHighlighter(self.highlighterCombobox.get())
        self.showCurrentHighlighter()

    def highlightSelection(self):
        # If there is no current highlighter OR selected text - do nothing
        try:
            self.currentHighlighter.addTerm(self.text.selection_get())
            self.showCurrentHighlighter()
            self.currentHighlighter.save()
        except Exception as e:
            return

    def loadText(self):
        fname = askopenfilename(initialdir="./", title="Select file",
                                filetypes=(("text", "*.txt"), ("all files", "*.*")))
        try:
            with open(fname, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    self.text.insert(END, line)
                self.fname = fname
                # Create the set of Highlighters
                self.highlighterSet = HighlighterSet(self.directory)
                # Populate the combobox with the Highlighter names
                self.highlighterCombobox['values'] = self.highlighterSet.highlighterNames
        except Exception as e:
            print("Text file load error: ", e)

    @property
    def directory(self):
        return os.path.dirname(self.fname)


if __name__ == '__main__':
    root = Tk()
    app = AdvancedSemanticHighlighterApp()
    root.mainloop()
