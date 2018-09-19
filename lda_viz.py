import itertools
import utils_opioids
import gensim
import nltk

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from gensim.matutils import jensen_shannon
import networkx as nx
import itertools as itt
from scipy.spatial.distance import pdist, squareform
import plotly.offline as py
from plotly.graph_objs import *
import plotly.figure_factory as ff
from gensim import corpora, models, similarities, matutils


def distance(X, dist_metric):
	return squareform(pdist(X, lambda u, v: dist_metric(u, v)))

lda = models.ldamodel.LdaModel.load('lda_10')

topic_dist = lda.state.get_lambda()
num_words = 50
topic_terms = [{w for (w, _) in lda.show_topic(topic, topn=num_words)} for topic in range(topic_dist.shape[0])]

topic_distance = distance(topic_dist, jensen_shannon)
edges = [(i, j, {'weight': topic_distance[i, j]}) for i, j in itt.combinations(range(topic_dist.shape[0]), 2)]
k = np.percentile(np.array([e[2]['weight'] for e in edges]), 20)
edges = [e for e in edges if e[2]['weight'] < k]

G = nx.Graph()
G.add_nodes_from(range(topic_dist.shape[0]))
G.add_edges_from(edges)

graph_pos = nx.spring_layout(G)
node_trace = Scatter(
						x = [], 
						y = [], 
						text = [], 
						mode = 'markers', 
						hoverinfo='text', 
						marker = Marker(
										showscale=True, 
										colorscale = 'YIGnBu', 
										reversescale=True, 
										color = [], 
										size = 10, 
										colorbar = dict(thickness=15, xanchor='left'),
										line=dict(width=2)))


edge_trace = Scatter(x = [], 
					 y = [], 
					 text = [], 
					 line = Line(width=0.5, color='#888'), 
					 hoverinfo='text', mode='lines')

n_ann_terms = 10

for edge in G.edges():
	x0, y0 = graph_pos[edge[0]]
	x1, y1 = graph_pos[edge[1]]
	pos_tokens = topic_terms[edge[0]] & topic_terms[edge[1]]
	neg_tokens = topic_terms[edge[0]].symmetric_difference(topic_terms[edge[1]])
	pos_tokens = list(pos_tokens)[:min(len(pos_tokens), n_ann_terms)]
	neg_tokens = list(neg_tokens)[:min(len(neg_tokens), n_ann_terms)]
	annotation = "<br>".join((": ".join(("+++", str(pos_tokens))), ": ".join(("---", str(neg_tokens)))))
	x_trace = list(np.linspace(x0, x1, 10))
	y_trace = list(np.linspace(y0, y1, 10))
	text_annotation = [annotation] * 10
	x_trace.append(None)
	y_trace.append(None)
	text_annotation.append(None)
	edge_trace['x'] += x_trace
	edge_trace['y'] += y_trace
	edge_trace['text'] += text_annotation

	
for node in G.nodes():
	x, y = graph_pos[node]
	node_trace['x'].append(x)
	node_trace['y'].append(y)
	node_info = ''.join((str(node+1), ': ', str(list(topic_terms[node])[:n_ann_terms])))
	node_trace['text'].append(node_info)

	
for node, adjacencies in enumerate(G.adjacency()):
	node_trace['marker']['color'].append(len(adjacencies))

	
fig = Figure(data=Data([edge_trace, node_trace]),
			 layout=Layout(showlegend=False, 
			 hovermode='closest', 
			 xaxis=XAxis(showgrid=True, zeroline=False, showticklabels=True),
			 yaxis=YAxis(showgrid=True, zeroline=False, showticklabels=True)))

py.plot(fig)