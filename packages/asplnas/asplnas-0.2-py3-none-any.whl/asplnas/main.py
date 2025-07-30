def one():
    print(""" #PROGRAM1
    import nltk
    from nltk.tokenize import word_tokenize, sent_tokenize
    from nltk.corpus import stopwords
    from nltk.stem import PorterStemmer, WordNetLemmatizer
    import string
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')
    nltk.download('punkt_tab')
    text1 = "Mumbai is the financial capital of India. It is known for Bollywood and its street food. I love going there"
    text2 = "The Taj Mahal is located in Agra. It was built by Emperor Shah Jahan in memory of his wife."
    sentences1 = sent_tokenize(text1)
    sentences2 = sent_tokenize(text2)
    sentences1
    words1 = word_tokenize(text1)
    words2 = word_tokenize(text2)
    words1
    #stopword removal
    stop_words = set(stopwords.words('english'))
    len(stop_words)
    filtered_words1 = []
    for word in words1:
        if word.lower() not in stop_words:
            filtered_words1.append(word)
    filtered_words1
    #stemming
    stemmer = PorterStemmer()
    stemmed_words1 = []
    for word in filtered_words1:
        stemmed_words1.append(stemmer.stem(word))
    stemmed_words1
    #lematization
    lemmatizer = WordNetLemmatizer()
    lemmatized_words1 = []
    for word in filtered_words1:
        lemmatized_words1.append(lemmatizer.lemmatize(word))
    lemmatized_words1 """)



def two():
    print(""" #PROGRAM2
!pip install svgling
import nltk
from nltk import word_tokenize, pos_tag, ne_chunk
from nltk.chunk import tree2conlltags
import pandas as pd
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('maxent_ne_chunker')
nltk.download('averaged_perceptron_tagger_eng')
nltk.download('words')
nltk.download('maxent_ne_chunker_tab')
text = "Apple Inc. is planning to open a new headquarters in Austin, Texas.
CEO Tim Cook announced the plan along with Harry Potter"
text2 = "Harry Potter, goes to Hogwarts"
tokens = word_tokenize(text)
tokens
pos_tags = pos_tag(tokens)
pos_tags
ne_tree = ne_chunk(pos_tags)
ne_tree
bio_tags = tree2conlltags(ne_tree)
bio_tags
entities = []
current_entity = []
current_type = None
for word, pos, tag in bio_tags:
    if tag.startswith('B-'):  # Beginning of entity
        # First handle any existing entity we were building
        if current_entity:
            entities.append((' '.join(current_entity), current_type))
        # Start a new entity
        current_entity = [word]
        current_type = tag[2:]
    elif tag.startswith('I-'):  # Inside entity
        # Only append if we're already building an entity of matching type
        if current_entity and current_type == tag[2:]:
            current_entity.append(word)
        # If we get an I- without a preceding B-, it's an error in the tagging
        # But we can handle it by treating it as a B-
        elif not current_entity:
            current_entity = [word]
            current_type = tag[2:]
    else:  # Outside entity (O tag)
        # Finish any entity we were building
        if current_entity:
            entities.append((' '.join(current_entity), current_type))
            current_entity = []
            current_type = None

# Don't forget to add the last entity if we end on an entity
if current_entity:
    entities.append((' '.join(current_entity), current_type))

entities    """)



