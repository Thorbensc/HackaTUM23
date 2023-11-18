import nltk
from sentence_transformers import SentenceTransformer, util
import numpy as np
import torch
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
from scipy.spatial import distance
from chunking import LogChunker

class LogSummarizer:

    def __init__(self,log_data) -> None:
        self.log_data = log_data
        self.chunker = LogChunker()

        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        self.embedder.max_seq_length = 512
        self.corpus = self.chunker.split_context(self.log_data)
        self.corpus_embeddings = self.embedder.encode(self.corpus)

    def summarize(self,num_clusters=20) -> str:
        if len(self.corpus) < num_clusters:
            num_clusters = len(self.corpus)
            
        clustering_model = KMeans(n_clusters=num_clusters)
        y_kmeans = clustering_model.fit_predict(self.corpus_embeddings)

        my_list=[]
        for i in range(num_clusters):
            my_dict={}
            for j in range(len(y_kmeans)):
                if y_kmeans[j]==i:
                    my_dict[j] =  distance.euclidean(clustering_model.cluster_centers_[i],self.corpus_embeddings[j])
            min_distance = min(my_dict.values())
            my_list.append(min(my_dict, key=my_dict.get))
        
        summary = ""
        for i in sorted(my_list):
            summary += self.corpus[i] + "\n"

        return summary