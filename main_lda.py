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

# for i in range(0, int(sys.argv[2])):
# 	print(linelist[i])

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
# print(quotes)
# sys.exit()

doc1 = "Sugar is bad to consume. My sister likes to have sugar, but not my father."
doc2 = "My father spends a lot of time driving my sister around to dance practice."
doc3 = "Doctors suggest that driving may cause increased stress and blood pressure."
doc4 = "Sometimes I feel pressure to perform well at school, but my father never seems to drive my sister to do better."
doc5 = "Health experts say that Sugar is not good for your lifestyle."

# compile documents
doc_complete = [doc1, doc2, doc3, doc4, doc5]
doc_complete = quotes

# CLEANING AND PREPROCESSING

# import nltk
# nltk.download()

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

doc_clean = [clean(doc).split() for doc in doc_complete]

# PREPARING DOCUMENT-TERM MATRIX

# Ignore warning from Gensim
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')

# Importing Gensim
import gensim
from gensim import corpora

# Creating the term dictionary of our courpus, where every unique term is assigned an index.
dictionary = corpora.Dictionary(doc_clean)

# Converting list of documents (corpus) into Document Term Matrix using dictionary prepared above.
doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]

# RUNNING LDA MODEL

# Creating the object for LDA model using gensim library
Lda = gensim.models.ldamodel.LdaModel

# Running and Trainign LDA model on the document term matrix.
ldamodel = Lda(doc_term_matrix, num_topics=3, id2word = dictionary, passes=50)

# RESULTS

print(ldamodel.print_topics(num_topics=int(sys.argv[3]), num_words=int(sys.argv[4])))
# ['0.168*health + 0.083*sugar + 0.072*bad,
# '0.061*consume + 0.050*drive + 0.050*sister,
# '0.049*pressur + 0.049*father + 0.049*sister]
