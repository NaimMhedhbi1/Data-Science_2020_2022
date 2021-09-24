
# remove space
spaces = ['\u200b', '\u200e', '\u202a', '\u202c', '\ufeff', '\uf0d8', '\u2061', '\x10', '\x7f', '\x9d', '\xad', '\xa0']
def remove_space(text):
    """
    remove extra spaces and ending space if any
    """
    for space in spaces:
        text = text.replace(space, ' ')
    text = text.strip()
    text = re.sub('\s+', ' ', text)
    return text

# replace strange punctuations and raplace diacritics
from unicodedata import category, name, normalize

def remove_diacritics(s):
    return ''.join(c for c in normalize('NFKD', s.replace('ø', 'o').replace('Ø', 'O').replace('⁻', '-').replace('₋', '-'))
                  if category(c) != 'Mn')

special_punc_mappings = {"—": "-", "–": "-", "_": "-", '”': '"', "″": '"', '“': '"', '•': '.', '−': '-',
                         "’": "'", "‘": "'", "´": "'", "`": "'", '\u200b': ' ', '\xa0': ' ','،':'','„':'',
                         '…': ' ... ', '\ufeff': ''}
def clean_special_punctuations(text):
    for punc in special_punc_mappings:
        if punc in text:
            text = text.replace(punc, special_punc_mappings[punc])
    # 注意顺序，remove_diacritics放前面会导致 'don´t' 被处理为 'don t'
    text = remove_diacritics(text)
    return text

def spacing_dash_point(text):
    if '-' in text:
        text = text.replace('-', ' - ')
    if '.' in text:
        text = text.replace('.', ' . ')
    return text


# clean numbers
def clean_number(text):
    # 字母和数字分开
    text = re.sub(r'(\d+)([a-zA-Z])', '\g<1> \g<2>', text)
    text = re.sub(r'(\d+) (th|st|nd|rd) ', '\g<1>\g<2> ', text)
    text = re.sub(r'(\d+),(\d+)', '\g<1>\g<2>', text)
    
#     text = re.sub('[0-9]{5,}', '#####', text)
#     text = re.sub('[0-9]{4}', '####', text)
#     text = re.sub('[0-9]{3}', '###', text)
#     text = re.sub('[0-9]{2}', '##', text)
    
    return text

#this function in order to use the rest of functions
def preprocess(text):
    """
    preprocess text main steps
    """
    text = remove_space(text)
    text = clean_special_punctuations(text)
    text = clean_number(text)
    text = remove_space(text)
    return text

def text_clean_wrapper(df):
    df["text"] = df["text"].apply(preprocess)
    return df

#removing stopwords
import nltk
nltk.download('stopwords')
stopword = nltk.corpus.stopwords.words('english')
def remove_stopwords(text):
    text = [word for word in text if word not in stopword]
    return text
    
df['text'] = df['text'].apply(lambda x: remove_stopwords(x))


#lemmitazation
import nltk
nltk.download('wordnet') 
wn = nltk.WordNetLemmatizer()

def lemmatizer(text):
    text = [wn.lemmatize(word) for word in text]
    return text

df['text'] = df['text'].apply(lambda x: lemmatizer(x))

