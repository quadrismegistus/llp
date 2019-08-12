# llp

Literary Language Processing (LLP): corpora, models, and tools for the digital humanities.

## Quickstart

### Install

Just run pip:

```
pip install llp
```

Or if you're newer to Python programming, and prefer to install LLP as part of a text mining "starter pack" of tools and software, check out the [LTM Starter Pack](ltm-starterpack).

### Configure

To configure, type:

```
llp configure
```

By default,

### Load

Download a corpus:

```
llp download ecco_tcp
```

Then use it:

```python
import llp
corpus = llp.load('ECCO_TCP')               # an llp.Corpus object
corpus.metadata                             # a pandas dataframe

for text in corpus.texts():                 # looping over llp.Text objects
   print(text.id, text.author, text.year)   # print some attributes
   # ... (see below for more)
```


## Corpus magic

There's a few ways to create a corpus uing LLP.

### 1. Downloading pre-existing corpora

To see which corpora are downloadable, run:

```
llp status
```

If you see an up arrow next to a type of data, you can 



If you have a folder of plain text files, and an accompanying metadata file,

```python
from llp.corpus import Corpus

my_corpus = Corpus(
	path_txt='my_texts',                # path to a folder of txt files
	path_metadata='my_metadata.xls',    # path to a metadata CSV, TSV, XLS, XLSX file
	col_fn='my_filename_column'         # column in metadata pointing to txt file (relative to `path_txt`)
)
```


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

## Do things with corpora

```python
# get the metadata as a dataframe
df_meta = corpus.metadata

# loop over the texts...
for text in corpus.texts():
    # get a string of that text
    text_str = text.txt

    # get the metadata as a dictionary
    text_meta = text.meta

```



## Do other things with texts

With any text object,

```python
# Get a text
texts = corpus.texts()
text = texts[0]

# Get the plain text as a string
txt = text.txt

# Get the metadata as a dictionary
metadata = text.meta

# Get the word tokens as a list
tokens = text.tokens

# Get the word counts as a dictionary
counts = text.freqs()

# Get the n-gram counts as a dictionary
bigrams = text.freqs_ngram(n=2)

# Get a list of passages mentioning a phrase (Key Word In Context)
passages = text.get_passages(phrases=['labour'])

# Get a spacy (http://spacy.io) representation
text_spacy = text.spacy()
```




## Do other things with corpora

Now that you have a corpus object,

```python
# Get the texts as a list
texts = corpus.texts()

# Get the metadata as a list of dictionaries
metadata = corpus.meta

# Save a list of the most frequent words
corpus.gen_mfw()

# Save a term-document matrix for the top 10000 most frequent words
corpus.gen_freq_table(n=10000)

# Save a list of possible duplicate texts in corpus, by title similarity
corpus.rank_duplicates_bytitle()

# Save a list of possible duplicate texts in corpus, by the content of the text (MinHash)
corpus.rank_duplicates()
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
```
