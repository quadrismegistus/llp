# llp

Literary Language Processing (LLP): corpora, models, and tools for the digital humanities.

## Quickstart

Install:

```
pip install llp                       # install with pip
```

Download an existing corpus...

```
llp status                            # show which corpora/data are available
llp download ECCO_TCP                 # download a corpus
```

...or import your own:

```
# point to a path of txt/xml files and ideally a metadata csv/tsv/xls
llp import -path_txt my_text_file_folder  -path_metadata my_metadata.xls
```

...or start a new one:

```
llp create                            # then follow the interactive prompt
```

Then load the corpus in Python:

```python
import llp                            # import llp as a python module
corpus = llp.load('ECCO_TCP')         # load the corpus by name or ID

df = corpus.metadata                  # get metadata as a pandas dataframe
smpl=df.query('1740 < year < 1780')   # quick query access

texts = corpus.texts()                # get a custom object for each text
texts = corpus.texts(smpl.id)         # get text objects for a list of IDs

for text in texts:                    # loop over text objects
    text_meta = text.meta             # get text metadata dictionary
    author = text.author              # get common metadata as attributes    

    txt = text.txt                    # get plain text as string
    xml = text.xml                    # get xml as string

    tokens = text.tokens              # get list of words (incl punct)
    words  = text.words               # get list of words (excl punct)
    counts = text.freqs()             # get word counts (from JSON if saved)
    ocracc = text.ocr_accuracy        # get estimate of ocr accuracy
    
    spacy_obj = text.spacy            # get a spacy.io text object
    nltk_obj = text.nltk              # get an nltk text object
    blob_obj = text.blob              # get a textblob object
```

## Corpus magic

Each corpus object can generate data about itself:

```
corpus.save_metadata()                # save metadata from xml files (if possible)
corpus.save_plain_text()              # save plain text from xml (if possible)
corpus.save_mfw()                     # save list of all words in corpus and their total  count
corpus.save_freqs()                   # save counts as JSON files
corpus.save_dtm()                     # save a document-term matrix with top N words
```

Or run in terminal:

```
llp install my_corpus                 # this is equivalent to python above
llp install my_corpus -parallel 4     # but can access parallel processing with MPI/Slingshot
llp install my_corpus dtm             # run a specific step
```

This then allows things like:

```python
mfw = corpus.mfw(n=10000)             # get the 10K most frequent words
dtm = corpus.freqs(words=mfw)         # get a document-term matrix as a pandas dataframe
```

You can also build word2vec models:

```python
w2v_model = corpus.word2vec()         # get an llp word2vec model object
w2v_model.model()                     # run the modeling process
w2v_model.save()                      # save the model somewhere
gensim_model = w2v_model.gensim       # get the original gensim object
```

























