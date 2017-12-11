# PREPARING DOCUMENTS
import sys

def extract_link(line, delimiter):
	ret = ""
	for huruf in line:
		if(huruf != delimiter and huruf != ' ' and huruf != '\t' and huruf != '\n'):
			ret += huruf
	return ret

def extract_domain(line):
	first_slash = line.index('/')
	i = first_slash + 2

	while (i < len(line)):
		if(line[i] == '/'):
			break
		i = i + 1

	return line[:i]

def delete_front(line):
	if(line[1] == '\t'):
		return line[2:]

def delete_back(line):
    if(line[len(line)-1] == '\n'):
        return line[:len(line)-1]

def clean_quotes(line):
    line = line[2:len(line)-1]
    return line

fp = open(sys.argv[1], encoding='utf-8')
linelist = []
for i, line in enumerate(fp):
    if i < int(sys.argv[2]):
    	linelist.append(line)
    else:
        break
fp.close()

quotes = []
time = []
page = []
links = []

is_new_element = False
temp_elem = []
quotes_elem = []
links_elem = []
elem = []
l_st = False

for line in linelist:
	if('Q' in line):
		quotes.append(clean_quotes(line))
		quotes_elem.append(quotes[len(quotes)-1])
		q_st = True
	elif('T' in line):
		time.append(line)
		temp_elem.append(time[len(time)-1])
	elif('P' in line):
		if(l_st):
			temp_elem.append(links_elem)
			links_elem = []
			l_st = False

		# page.append(extract_domain(extract_link(line, 'P')))
		page.append(delete_front(line))
		elem.append(temp_elem)
		temp_elem = []
		temp_elem.append(page[len(page)-1])
	elif('L' in line):
		if(q_st):
			temp_elem.append(quotes_elem)
			quotes_elem = []
			q_st = False

		# links.append(extract_domain(extract_link(line, 'L')))
		links.append(delete_front(line))
		links_elem.append(links[len(links)-1])
		l_st = True

print('Extracting quotes DONE')

# compile documents
doc_complete = quotes

# CLEANING AND PREPROCESSING

from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
stop = set(stopwords.words('english'))
exclude = set(string.punctuation)
lemma = WordNetLemmatizer()
def clean(doc):
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized

documents = [clean(doc) for doc in doc_complete]

# Kalo mau niat ngurangin less frequent word ntar

import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
from gensim import corpora, models, similarities
from itertools import chain

# remove common words and tokenize
stoplist = set('for a of the and to in'.split())
texts = [[word for word in document.lower().split() if word not in stoplist]
         for document in documents]

# remove words that appear only once
all_tokens = sum(texts, [])
tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word) == 1)
texts = [[word for word in text if word not in tokens_once] for text in texts]

# Create Dictionary.
id2word = corpora.Dictionary(texts)
# Creates the Bag of Word corpus.
mm = [id2word.doc2bow(text) for text in texts]

# Trains the LDA models.
lda = models.ldamodel.LdaModel(corpus=mm, id2word=id2word, num_topics=3, \
                               update_every=1, chunksize=10000, passes=1)

# Prints the topics.
for top in lda.print_topics():
  print(top)
print(' ')

# Assigns the topics to the documents in corpus
lda_corpus = lda[mm]

# Find the threshold, let's set the threshold to be 1/#clusters,
# To prove that the threshold is sane, we average the sum of all probabilities:
scores = list(chain(*[[score for topic_id,score in topic] \
                      for topic in [doc for doc in lda_corpus]]))
threshold = sum(scores)/len(scores)
print(threshold)
print(' ')

cluster1 = [j for i,j in zip(lda_corpus,documents) if i[0][1] > threshold]
# cluster2 = [j for i,j in zip(lda_corpus,documents) if i[1][1] > threshold]
# cluster3 = [j for i,j in zip(lda_corpus,documents) if i[2][1] > threshold]

print(len(cluster1) == len(documents))
# print(cluster1)
# print(cluster2)
# print(cluster3)
