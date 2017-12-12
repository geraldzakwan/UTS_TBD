from gensim import corpora, models, similarities
from itertools import chain
import string
import sys

filename = '../../' + sys.argv[1]
number_of_line = int(sys.argv[2])
month = int(sys.argv[3])

raw_document = []
snippets = []
isAccepted = False

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

# open the docs and read line by line
temp = None
with open(filename, 'r') as infile:
  for line in infile:
    # to store the domain 
    if 'P' in line:
      temp = extract_domain(line)

    # Do we need this quotes ?
    if 'T' in line:
      if(month == int(line.split('\t')[1].split('-')[1])):
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

# remove common words and tokenize
stoplist = set('for a of the and to in'.split())
texts = [[word for word in document.lower().split() if word not in stoplist] for document in raw_document]

# remove words that appear only once
all_tokens = sum(texts, [])
tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word) == 1)
texts = [[word for word in text if word not in tokens_once] for text in texts]

# Create Dictionary.
id2word = corpora.Dictionary(texts)
# Creates the Bag of Word corpus.
mm = [id2word.doc2bow(text) for text in texts]

# Trains the LDA models.
lda = models.ldamodel.LdaModel(corpus=mm, id2word=id2word, num_topics=3, update_every=1, chunksize=10000, passes=1)

# Prints the topics.
for top in lda.print_topics():
  print top
print

# Assigns the topics to the documents in corpus
lda_corpus = lda[mm]

# Find the threshold, let's set the threshold to be 1/#clusters,
# To prove that the threshold is sane, we average the sum of all probabilities:
scores = list(chain(*[[score for topic_id,score in topic] for topic in [doc for doc in lda_corpus]]))
threshold = sum(scores)/len(scores)
print threshold
print

cluster1 = [j for i,j in zip(lda_corpus,raw_document) if i[0][1] > threshold]
#cluster2 = [j for i,j in zip(lda_corpus,raw_document) if i[1][1] > threshold]
#cluster3 = [j for i,j in zip(lda_corpus,raw_document) if i[2][1] > threshold]

print cluster1
#print cluster2
#print cluster3