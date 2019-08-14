# llp

Literary Language Processing (LLP): corpora, models, and tools for the digital humanities.

## Quickstart

### Install


```
pip install llp
```

### Download an existing corpus...


```
llp status                # shows which corpora/data are available
llp download ECCO_TCP     # download a corpus
```

Then load in Python:

```python
import llp                                   # import llp as a python module
corpus = llp.load('ECCO_TCP')                # load the corpus
```

### ...or load your own corpus

```python
import llp
my_corpus = llp.Corpus(
	path_txt='/my/corpus/texts',               # path to a folder of txt files
	path_metadata='/my/corpus/metadata.xls',   # path to a metadata CSV, TSV, XLS, XLSX file
	col_fn='my_filename_column'                # column in metadata pointing to txt file (relative to `path_txt`)
)
```


### Access metadata

```python
# easy pandas access to metadata
df = corpus.metadata                    # get the metadata as a dataframe

# easy metadata query access
df_midcentury_poems = corpus.metadata.query('1740 < year < 1780 & genre=="Verse"')
```

### Use text objects

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

### Generate data about corpus



```







## Do things with models

```python
# Generate a word2vec model with gensim
w2v_model = corpus.word2vec()
w2v_model.model()

# Save model
w2v_model.save()

# Get the original gensim object
gensim_model = w2v_model.gensim


Then, in pyton:

```python

```


### Install

Just run pip:

```
pip install llp
```

Or if you're newer to Python programming, and prefer to install LLP as part of a text mining "starter pack" of tools and software, check out the [LTM Starter Pack](ltm-starterpack).

To configure, type:

```
llp configure
```

By default, 

### Load a corpus

Download a corpus:

```
llp download ECCO_TCP
```



```python
import llp
corpus = llp.load('ECCO_TCP')               # an llp.Corpus object
corpus.metadata                             # a pandas dataframe
```


### Work

e

```python
for text in corpus.texts():                 # looping over llp.Text objects
   print(text.id, text.author, text.year)   # print some attributes
   # ... (see below for more)
```

### Work




## Corpus magic

There's a few ways to create a corpus uing LLP.

### 1. Downloading pre-existing corpora

To see which corpora are downloadable, run:

```
llp status
```

If you see an up arrow next to a type of data, you can ...



If you have a folder of plain text files, and an accompanying metadata file,




## Load a pre-existing corpus

Start working with corpora in a few lines:

```python
# import the llp module
import llp

# load the ECCO-TCP corpus [distributed freely online]
corpus = llp.load('ECCO_TCP')

# don't have it yet?
corpus.download()
```


```
