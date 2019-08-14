# llp

Literary Language Processing (LLP): corpora, models, and tools for the digital humanities.

## Quickstart

Install:

```
pip install llp           # install via pip
```

Download an existing corpus...

```
llp status                # shows which corpora/data are available
llp download ECCO_TCP     # download a corpus
```

...or import your own:

```
llp import -path_txt /my/corpus/texts -path_metadata /my/corpus/metadata.xls
```

Then load in Python:

```python
import llp                                   # import llp as a python module
corpus = llp.load('ECCO_TCP')                # load the corpus
```

And play with corpus objects:

```
corpus.metadata                               # get metadata as a pandas dataframe
corpus.metadata.query('1740 < year < 1780')   # quick query access
```


And play with text objects:


```python
for text in corpus.texts():         # loop over text objects

    text_meta = text.meta           # get text metadata
    author = text.author            # easy access to common metadata
    year = text.year                # text.year, text.title, ...
    
    txt = text.txt                  # get plain text as string
    xml = text.xml                  # get xml as string

    tokens = text.tokens            # get list of words
    counts = text.freqs()           # get word counts (from JSON if saved)
```


Generate other data about corpora:

```
corpus.save_metadata()        # save metadata from files (if nec)
corpus.save_plain_text()      # save plain text from xml (if nec)
corpus.save_mfw()             # save list of all words in corpus and their total corpus.save_freqs()           # save counts as JSON files:
corpus.save_dtm()
```

Or:

```
llp save_freqs my_corpus
```



Also:




```python
# generate a word2vec model with gensim
w2v_model = corpus.word2vec()
w2v_model.model()

# Save model
w2v_model.save()

# Get the original gensim object
gensim_model = w2v_model.gensim
```

























