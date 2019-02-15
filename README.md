# llp

Literary Language Processing (LLP): Corpora, models, and tools for the digital humanities. Written in Python.

## Make a corpus in two lines

If you have a folder of plain text files,

```python
from llp.corpus.default import PlainTextCorpus

corpus = PlainTextCorpus(
	path_txt='folder',             # path to a folder of txt files
	path_metadata='metadata.xls',  # path to a metadata CSV, TSV, or XLS file
	col_fn='filename'              # column in meadata pointing to txt file (relative to `path_txt`)
)
```

## Corpora

...

## Texts

```python
# for every text in the corpus...
for text in corpus.texts():

	# get full text string
	text_as_string = text.text
	
	# get text metadata
	text_metadata_dicionary = text.meta
	
	# tokenize
	tokens = text.tokens
	
	# word counts
	counts = text.freqs()
	
	# n-gram counts
	bigrams = text.freqs_ngram(n=2)
	
	# key word in context
	passages_as_list_of_dictionaries = text.get_passages(phrases=['virtue','honour'])
	
	# spacy
	text_as_spacy_object = text.spacy()
	named_entities = text_as_spacy_object.ents
	
```

