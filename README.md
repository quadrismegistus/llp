# llp

Literary Language Processing (LLP) for the Stanford Literary LAB. Corpora, models, and tools for the digital humanities. Written in Python.

## Load corpora in a few lines

Start working with corpora in two lines:

```python
# import the llp module
import llp

# load the chicago corpus
chicago = llp.load('Chicago')

# don't have it yet?
chicago.download()

# get the metadata as a dataframe
df_meta = chicago.metadata

# loop over the texts...
for text_obj in chicago.texts():
    # get a string of that text
    text_str = text_obj.txt

    # get the metadata as a dictionary
    text_meta = text_obj.meta

    # get (e.g.) the title (and set default)
    text_title = text_meta.get('title','[Unknown]')

    # get the rough number of words in the string
    num_words1 = len(text_str.split())
    num_words2 = text_obj.num_words
````

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

## Do oother things with texts

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
