from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.externals import joblib
import string
import sys
import operator

filename = '../../' + sys.argv[1]
number_of_line = int(sys.argv[2])
week = int(sys.argv[3])

raw_document = []
snippets = []
isAccepted = False

def rank_terms( A, terms ):
	# get the sums over each column
	sums = A.sum(axis=0)
	# map weights to the terms
	weights = {}
	for col, term in enumerate(terms):
		weights[term] = sums[0,col]
	# rank the terms by their weight over all documents
	return sorted(weights.items(), key=operator.itemgetter(1), reverse=True)

def extract_domain(line):
	domain_raw = line.split('\t')[1]
	temp = domain_raw.split('/')
	domain_net = temp[2]
	domain_net = domain_net.replace('\n', '')
	return domain_net

def process_content(line):
	output = line.split('\t')[1]
	output = output.replace("\n", "")
	return output

def get_week(x):
	if x >= 1 or x <= 7:
		return 1
	elif x > 7 or x <= 14:
		return 2
	elif x > 14 or x <= 21:
		return 3
	else :
		return 4

# open the docs and read line by line
temp = None
with open(filename, 'r') as infile:
	for line in infile:
		# to store the domain 
		if 'P' in line:
			temp = extract_domain(line)

		# Do we need this quotes ?
		if 'T' in line:
			if(week == get_week(int(line.split('\t')[1].split('-')[2].split(' ')[0]))):
				isAccepted = True
			else:
				isAccepted = False

		# if yes, store its domain too 
		if isAccepted: snippets.append(temp)

		if 'Q' in line and isAccepted:
			raw_document.append(process_content(line))
			number_of_line -= 1

		if number_of_line == 0:
			break

# cleaning and preprocessing
custom_stop_words = []
with open( "stopwords.txt", "r" ) as fin:
    for line in fin.readlines():
        custom_stop_words.append( line.strip() )
print("Stopword list has %d entries" % len(custom_stop_words) )

vectorizer = TfidfVectorizer(stop_words=custom_stop_words, min_df = 20)
A = vectorizer.fit_transform(raw_document)
print( "Created %d X %d TF-IDF-normalized document-term matrix" % (A.shape[0], A.shape[1]) )

terms = vectorizer.get_feature_names()
print("Vocabulary has %d distinct terms" % len(terms))

ranking = rank_terms( A, terms )
for i, pair in enumerate( ranking[0:20] ):
	print( "%02d. %s (%.2f)" % ( i+1, pair[0], pair[1] ) )

# Save to external file
joblib.dump((A,terms,snippets), "articles" + str(week) + ".pkl")