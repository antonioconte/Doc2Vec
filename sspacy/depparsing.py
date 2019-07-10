import spacy
from spacy.symbols import nsubj, VERB

nlp = spacy.load("en_core_web_sm")
text = "Autonomous cars shift insurance liability toward manufacturers"
doc = nlp(text)

# Finding a verb with a subject from below — good
verbs = set()
for possible_subject in doc:
    if possible_subject.dep == nsubj and possible_subject.head.pos == VERB:
        verbs.add(possible_subject.head)
print(verbs)

newString = ""
for chunk in doc.noun_chunks:
    if chunk.root.dep == nsubj and chunk.root.head.pos == VERB:
        newString += "subj"
    else:
        newString += " " + chunk.text
print("ORIGINAL:", text)
print("EDIT:", newString)
        # form = "Text: {}, RootText: {}, RootDep: {}, RootHeadText: {}, RootHeadDep: {}"
        # print(form.format(chunk.text, chunk.root.text, chunk.root.dep_,
        #     chunk.root.head.text, chunk.root.head.pos_))
