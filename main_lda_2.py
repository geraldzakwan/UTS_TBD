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
# print(quotes[0])

compiled_doc = ""
for elem in doc_complete:
    compiled_doc = compiled_doc + '\t'
    compiled_doc = compiled_doc + elem

# CLEANING AND PREPROCESSING

# import nltk
# nltk.download()

import pickle
# Ignore warning from Gensim
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
import gensim
from sklearn.feature_extraction.text import CountVectorizer

# Use CountVectorizor to find three letter tokens, remove stop_words,
# remove tokens that don't appear in at least 20 documents,
# remove tokens that appear in more than 20% of the documents
vect = CountVectorizer(min_df=20, max_df=0.2, stop_words='english',
                       token_pattern='(?u)\\b\\w\\w\\w+\\b')
# Fit and transform
X = vect.fit_transform(doc_complete)

# Convert sparse matrix to gensim corpus.
corpus = gensim.matutils.Sparse2Corpus(X, documents_columns=False)

# Mapping from word IDs to words (To be used in LdaModel's id2word parameter)
id_map = dict((v, k) for k, v in vect.vocabulary_.items())

# Use the gensim.models.ldamodel.LdaModel constructor to estimate
# LDA model parameters on the corpus, and save to the variable `ldamodel`

# Your code here:
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=int(sys.argv[3]), id2word=id_map, passes=100)

# Print Top 10 Topics / Word Distribution
output = ldamodel.print_topics(10)
print(output)

new_doc = ["how to create property binding in a visual webgui silverlight control"]


# for new document, use the previous model to find the probability which topic it belongs to
def topic_distribution():

    # Fit and transform
    X = vect.transform(new_doc)

    # Convert sparse matrix to gensim corpus.
    corpus = gensim.matutils.Sparse2Corpus(X, documents_columns=False)

    output = list(ldamodel[corpus])[0]

    return output

print(topic_distribution())
