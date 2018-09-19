'''
LDA is a probabilistic topic model that assumes documents 
are a mixture of topics and that each word in the document 
is attributable to the document's topics.

Each topic has a set of words that defines it, 
along with a certain probability.
'''

import itertools
import dend_annotate
import gensim

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from gensim.matutils import jensen_shannon
from scipy.cluster import hierarchy as sch
from scipy import spatial as scs

from gensim import corpora, models, similarities, matutils
from gensim.parsing.preprocessing import remove_stopwords, strip_punctuation
from gensim.models import Phrases
from gensim.models.phrases import Phraser
from collections import defaultdict
from pprint import pprint

from scipy.spatial.distance import pdist, squareform
import plotly.offline as py
from plotly.graph_objs import *
import plotly.figure_factory as ff


#function to compare probability values of categories 
#to a given value (in this code, the closest value to 1)
#returns index of category

def find_nearest_topic(array, values):
    indices = np.abs(np.subtract.outer(array, values)).argmin(0)
    return indices

def js_dist(X):
    return pdist(X, lambda u, v: jensen_shannon(u, v))

number_of_topics = sys.argv[-1]
 
#load edited dictionary.
dictionary = corpora.Dictionary.load_from_text('abstract_dictionary')

#load corpus from disk
corpus = corpora.MmCorpus('abstract_text_corpus.mm')

#Create LDA model using Gensim. Change topics to desired number, other parameters 
#(higher numbers = longer runtime; passes, update_every perams both default to 1)
#add chunksize param to analyze portion of corpus
lda = models.LdaModel(corpus, alpha = 'auto', eta = 'auto',
                            num_topics = number_of_topics,
							iterations = 400,
                            id2word=dictionary, 
                            update_every=1, 
                            passes=50)

lda.save('lda_model')
lda = models.ldamodel.LdaModel.load('lda_model')

#get topic distributions
topic_dist = lda.state.get_lambda()

#get topic terms
num_words = 300
topic_terms = [{w for (w, _) in lda.show_topic(topic, topn=num_words)} for topic in range(topic_dist.shape[0])]

# no. of terms to display in annotation
n_ann_terms = 10

# define method for distance calculation in clusters
linkagefun=lambda x: sch.linkage(x, 'single')

#get text annotations
#need to have the dend_annotate file in same directory
annotation = dend_annotate.text_annotation(topic_dist, topic_terms, n_ann_terms, linkagefun)

#plot dendrogram
dendro = ff.create_dendrogram(topic_dist, distfun=js_dist, labels=range(1, 16), linkagefun=linkagefun, hovertext=annotation)
dendro['layout'].update({'width': 1000, 'height': 600})
py.plot(dendro)
						
#shows most significant words in each topic (defaults to 10)
#topics returned are arbitrary in order
topics_matrix = lda.show_topics(formatted = False, num_words = 25) #delete num_words to reduce vocab display
topics_matrix = np.array(topics_matrix, dtype=object)
topic_words = topics_matrix[:, 1]

for i in topic_words:
	pprint([str(word) for word in i])

#compare corpus to the lda model 
#assigns topic probability distribution for each doc in corpus
vec_lda = lda[[corpus[i] for i in range(len(corpus))]]
vec_lda = lda.get_document_topics(corpus)
	
#build dictionary with topic number as key and topic words as values
categories = {}
i = 0
#Convert individual document in BoW format into dense numpy array for each topic
#the array value closest to 1 indicates most likely topic assignment
while i < len(vec_lda):
	get_topic_sims = gensim.matutils.sparse2full(vec_lda[i], lda.num_topics) 
	categories.update({str(find_nearest_topic(get_topic_sims, 1)) + '-' + str(i) : 
	                   str(lda.print_topic(find_nearest_topic(get_topic_sims, 1)))})
	i += 1

#assign those topics to the items in the corpus you compared to LDA model
#create a dataframe with original title / abstract data
category_frame = pd.DataFrame(list(categories.items()), columns = ['category number', 'category words'])
df = df.reset_index(drop = True)
categorized_docs = pd.concat([df, category_frame], axis = 1)
categorized_docs['category number'] = categorized_docs['category number'].str.extract('(\d.)')

#save to excel
writer = pd.ExcelWriter('categorized_ai_docs.xlsx', engine = 'xlsxwriter')
categorized_docs.to_excel(writer, encoding ='ISO-8859-1')
writer.save()


'''
#get cluster number labels and total number of clusters based on assigned categories
labels = list(itertools.chain.from_iterable(categorized_docs[['category number']].as_matrix().tolist()))
num_clusters = np.unique(categorized_docs['category number']).shape[0]

#generate tfidf
tfidf_model = models.TfidfModel(corpus, dictionary = dictionary)
corpus_X = tfidf_model[corpus]
eca_tfidf = matutils.corpus2csc(corpus_X).transpose()

#assign number of clusters, fit tfidf to kmeans
km = KMeans(n_clusters = num_clusters)
km.fit(eca_tfidf)

#record clusters
clusters = km.labels_.tolist()
centers = km.cluster_centers_

docs = {'Title': titles, 'EID': eids, 'Abstract': abs, 'Cluster': clusters, 'Citations': cites, 'Labels': labels}
cdocframe = pd.DataFrame(docs, index = [clusters], columns = ['Title', 'EID', 'Abstract', 'Cluster', 'Citations', 'Labels'])
'''
