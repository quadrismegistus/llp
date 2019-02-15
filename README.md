# llp

Literary Language Processing (LLP): Corpora, models, and tools for the digital humanities. Written in Python.

## Make a corpus in two lines

If you have a folder of plain text files,

```python
from llp.corpus.default import PlainTextCorpus

corpus = PlainTextCorpus(
	path_txt='/path/to/a/folder/of/txt/files',
	path_metadata='/path/to/a/metadata_TSV_or_Excel_file',
	col_fn='column_in_metadata_containing_filename'  # relative path from POV of path_txt
)
```

## What corpora can do

## What texts can do

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

