

import gensim
import spacy
import re
import nltk
import unicodedata
from nltk.corpus import stopwords
import pandas as pd
import numpy as np



from gensim.models.word2vec import Word2Vec


# In[23]:


df = pd.read_csv(r"C:/Users/Dell/Notebook/NLP/french_comments_annotated.csv")
df.columns = ["text", "note"]


# In[133]:


df


# In[24]:


len(df)


# In[25]:


df_text_clean = df.text.dropna()


# In[52]:


nlp_ = spacy.load(r"C:\Users\Dell\spacy\dist\fr_core_news_md-2.2.5\fr_core_news_md\fr_core_news_md-2.2.5")

# nltk.download('stopwords') 
fr_nltk_stopWords = set(stopwords.words('french'))
fr_spacy_stopWords = spacy.lang.fr.stop_words.STOP_WORDS
FRENCH_STOPWORDS = list(fr_spacy_stopWords | fr_nltk_stopWords) 

#Stopwords = mots trop communs inutiles au modèle 


# In[53]:


FRENCH_STOPWORDS


# In[134]:


list_text = list(df_text_clean)
# list_text : liste des commentaires du csv


# In[32]:


ALPHA_CLEANING_PATTERN = re.compile(r"(((?![\d])\w)+)", re.MULTILINE) # 3+ alpha caracters

def keep_alpha_text_only(text):
    """ Renvoie les caractères alpha d'un commentaire
    """
    txt_match = [alpha.group() for alpha in ALPHA_CLEANING_PATTERN.finditer(text)]
    return " ".join(txt_match)


# In[38]:


def clean_text(seq_of_texts, flag_lower = True):
    """ cleaning processing steps on a seq of text. Return the cleaned seq of text"""
    for text in seq_of_texts:
        #print(type(text))
        text_strip = keep_alpha_text_only(text)
        text_normalized = normalize(text_strip, flag_lower)
        yield text_normalized


# In[63]:


def normalize(text, flag_lower = True):
    """ normalize by remove non ascii caracter"""
    #U-test : normalize("  le chat\xa3 est beau \xa3\xa3")
    if(flag_lower):
        return unicodedata.normalize("NFKD", text).encode('ascii', 'ignore').decode('utf8', 'ignore').lower()
    else:
        return unicodedata.normalize("NFKD", text).encode('ascii', 'ignore').decode('utf8', 'ignore')
    
    
def preprocessing_tokeniziong_lemmatization_and_grammar_filter(list_of_text, nlp_model = nlp_):
    """Pipeline for processing, tokenizing and lemmatizing"""
    seq_of_cleaned_text = [*clean_text(list_of_text)] #la liste de textes propres
    for spacy_doc in nlp_model.pipe(seq_of_cleaned_text, n_threads=3):
        list_of_useful_token = [spacy_token for spacy_token in spacy_doc]
        list_of_useful_token_wo_stopwords = [token.lemma_ for token in list_of_useful_token] # je veux uniquement récupérer les racines de mots. Exemples : Chanteurs -> chant
        yield list_of_useful_token_wo_stopwords  

    
def make_n_grams(list_of_useful_token_wo_stopwords, min_count, max_vocab, threshold, common_terms , scoring = "npmi"):
    """[New, York] -> [New_York]
    """
    ngram = gensim.models.Phrases(list_of_useful_token_wo_stopwords, max_vocab_size=max_vocab, min_count=min_count, scoring=scoring,threshold=threshold, common_terms=common_terms)
    ngram_mod = gensim.models.phrases.Phraser(ngram)
    seq_of_useful_text = [u" ".join([x for x in ngram_mod[doc]]) for doc in list_of_useful_token_wo_stopwords]
    return (ngram_mod, seq_of_useful_text)


# In[102]:


bigram_mod, seq_of_text_cleaned = make_n_grams([*preprocessing_tokeniziong_lemmatization_and_grammar_filter(list_text[:10000])], min_count = 2, max_vocab= 5000, threshold = 0.5, common_terms=FRENCH_STOPWORDS)
w2vec_input = [gensim.utils.simple_preprocess(seq) for seq in seq_of_text_cleaned]


# In[119]:


w2vec_model = Word2Vec(w2vec_input, size = 150, window = 5, min_count=5)


# In[123]:


list_voc = w2vec_model.wv.vocab.keys()


# In[124]:


list_voc


# In[135]:


w2vec_model.wv.most_similar("dragon_ball")

