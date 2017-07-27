from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfilename
from Highlighter import *

FINDALLTAG = 'findAll'

class HighlightText(Text):
    def __init__(self, *args, **kwargs):
        Text.__init__(self, *args, **kwargs)
        self.tag_configure(FINDALLTAG, foreground='white', background='red')

    # Tags the items given in the textList
    def tagAllList(self, textList, tag=FINDALLTAG):
        for t in textList:
            print(t)
            self.tagAll(t, tag)

    def addTag(self, name, foreground='red', background='white'):
        self.tag_configure(name, foreground=foreground, background=background)

    def clearTags(self):
        for tag in self.tag_names():
            self.tag_delete(tag)

    def tagAll(self, text, tag=FINDALLTAG):
        start = self.index("1.0")
        end = self.index("end")

        self.mark_set("matchStart", start)
        self.mark_set("matchEnd", start)
        self.mark_set("searchLimit", end)

        count = IntVar()
        while True:
            index = self.search(text, "matchEnd","searchLimit", count=count, regexp=False)
            if index == "": break
            if count.get() == 0: break # matches zero-length strings
            self.mark_set("matchStart", index)
            self.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
            self.tag_add(tag, "matchStart", "matchEnd")


class SemanticHighlighterApp(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.pack(fill=BOTH, expand=True)
        self.master.title('Semantic highlighter')
        self.initUI()

        self.fname = None
        self.highlighterSet = None
        self.currentHighlighter = None

    def initUI(self):
        # The text frame
        textFrame = Frame(self, borderwidth=2, relief=GROOVE)
        textFrame.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=5)

        textButtonFrame = Frame(textFrame)
        textButtonFrame.pack(side=TOP, fill=X)

        loadTextButton = Button(textButtonFrame, text="Load text", command = self.loadText)
        loadTextButton.pack(side=LEFT, padx=5, pady=5)

        addHighlightSelectionButton = Button(textButtonFrame, text="Highlight selection", command=self.highlightSelection)
        addHighlightSelectionButton.pack(side=LEFT, padx=5, pady=5)

        self.text = HighlightText(textFrame, height=26, width=50, wrap=WORD)
        scroll = Scrollbar(self.text, command=self.text.yview)
        self.text.configure(yscrollcommand=scroll.set)
        # Make read only by rebinding keys
        self.text.bind("<Key>", lambda e: "break")
        self.text.pack(side=BOTTOM,fill=BOTH, expand=True)

        # The term list frame
        highlighterFrame = Frame(self, borderwidth=2, relief=GROOVE)
        highlighterFrame.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=5)

        # The highlighter combo box
        self.selectHighlighterCombobox = Combobox(highlighterFrame)
        self.selectHighlighterCombobox.bind("<<ComboboxSelected>>", self.comboboxSelection)
        self.selectHighlighterCombobox.pack(side=TOP, padx=5, pady=5)

        removeHighlightedTermButton = Button(highlighterFrame, text="Remove highlighted term", command=self.removeTerm)
        removeHighlightedTermButton.pack(side=BOTTOM, padx=5, pady=5)

        self.hiList = Listbox(highlighterFrame)
        self.hiList.pack(side=TOP, fill=BOTH, expand=True)

    def removeTerm(self):
        if self.hiList.curselection() != ():
            self.currentHighlighter.removeTerm(self.hiList.get(self.hiList.curselection()[0]))
            self.showCurrentHighlighter()
            self.currentHighlighter.save()

    def showCurrentHighlighter(self):
        # If there is no current highlighter - do nothing
        if self.currentHighlighter == None: return
        # Empty the Listbox
        self.hiList.delete(0,END)
        # Populate the Listbox
        for t in self.currentHighlighter.terms:
            self.hiList.insert(END,t)
        # Process the text box
        # Clear any existing tags
        self.text.clearTags()
        # Set the new tag
        self.text.addTag(self.currentHighlighter.name, self.currentHighlighter.foreground, self.currentHighlighter.background)
        # Highlight the list of terms
        self.text.tagAllList(self.currentHighlighter.terms, self.currentHighlighter.name)

    def comboboxSelection(self, event):
        # Set the current Highlighter
        self.currentHighlighter = self.highlighterSet.getHighlighter(self.selectHighlighterCombobox.get())
        self.showCurrentHighlighter()

    def highlightSelection(self):
        # If there is no current highlighter - do nothing
        if self.currentHighlighter == None: return
        self.currentHighlighter.addTerm(self.text.selection_get())
        self.showCurrentHighlighter()
        self.currentHighlighter.save()

    def loadText(self):
        fname = askopenfilename(initialdir = "./",title = "Select file",filetypes = (("text","*.txt"),("all files","*.*")))
        try:
            with open(fname,'r') as f:
                lines = f.readlines()
                for line in lines:
                    self.text.insert(END, line)
                self.fname = fname
                # Create the set of Highlighters
                self.highlighterSet = HighlighterSet(self.directory)
                # Populate the combobox with the Highlighter names
                self.selectHighlighterCombobox['values'] = self.highlighterSet.highlighterNames
        except Exception as e:
            print("Text file load error: ",e)

    @property
    def directory(self):
        return os.path.dirname(self.fname)


if __name__ == '__main__':
    root = Tk()
    app = SemanticHighlighterApp()
    root.mainloop()
