from sklearn.externals import joblib
from sklearn import decomposition
import sys
import numpy as np
import numpy as np
import matplotlib
import matplotlib.pyplot as plt


def get_top_snippets( all_snippets, W, topic_index, top ):
    # reverse sort the values to sort the indices
    top_indices = np.argsort( W[:,topic_index] )[::-1]
    # now get the snippets corresponding to the top-ranked indices
    top_snippets = []
    for doc_index in top_indices[0:top]:
        top_snippets.append( all_snippets[doc_index] )
    return top_snippets

def plot_top_term_weights( terms, H, topic_index, top ):
    # get the top terms and their weights
    top_indices = np.argsort( H[topic_index,:] )[::-1]
    top_terms = []
    top_weights = []
    for term_index in top_indices[0:top]:
        top_terms.append( terms[term_index] )
        top_weights.append( H[topic_index,term_index] )
    # note we reverse the ordering for the plot
    top_terms.reverse()
    top_weights.reverse()
    # create the plot
    fig = plt.figure(figsize=(13,8))
    # add the horizontal bar chart
    ypos = np.arange(top)
    ax = plt.barh(ypos, top_weights, align="center", color="green",tick_label=top_terms)
    plt.xlabel("Term Weight",fontsize=14)
    plt.tight_layout()
    plt.show()

def get_descriptor( terms, H, topic_index, top ):
	# reverse sort the values to sort the indices
	top_indices = np.argsort( H[topic_index,:] )[::-1]
	# now get the terms corresponding to the top-ranked indices
	top_terms = []
	for term_index in top_indices[0:top]:
		top_terms.append( terms[term_index] )
	return top_terms

filename = sys.argv[1]
(A,terms,snippets) = joblib.load( filename )
print( "Loaded %d X %d document-term matrix" % (A.shape[0], A.shape[1]) )

k = 10 # how many topics

model = decomposition.NMF( init="nndsvd", n_components=k ) 
# apply the model and extract the two factor matrices
W = model.fit_transform( A )
H = model.components_

descriptors = []
for topic_index in range(k):
	descriptors.append( get_descriptor( terms, H, topic_index, 10 ) )
	str_descriptor = ", ".join( descriptors[topic_index] )
	print("Topic %02d: %s" % ( topic_index+1, str_descriptor ) )


plt.style.use("ggplot")
matplotlib.rcParams.update({"font.size": 14})
plot_top_term_weights( terms, H, 6, 15 )