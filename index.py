from flask import Flask, render_template, request
from scipy.sparse import csr_matrix
import numpy as np
from sklearn.neighbors import NearestNeighbors
import pandas as pd
import csv

class MC:
    ratings = pd.read_csv("Event-ratings.csv")
    events = pd.read_csv("Events.csv")

    def create_matrix(df):
    
        N = len(df['User_ID'].unique())
        M = len(df['Event_ID'].unique())

        user_mapper = dict(zip(np.unique(df["User_ID"]), list(range(N))))
        event_mapper = dict(zip(np.unique(df["Event_ID"]), list(range(M))))
    
        user_inv_mapper = dict(zip(list(range(N)), np.unique(df["User_ID"])))
        event_inv_mapper = dict(zip(list(range(M)), np.unique(df["Event_ID"])))

        user_index = [user_mapper[i] for i in df['User_ID']]
        event_index = [event_mapper[i] for i in df['Event_ID']]

        X = csr_matrix((df["Rating"], (event_index, user_index)), shape=(M, N))
    
        return X, user_mapper, event_mapper, user_inv_mapper, event_inv_mapper

    X, user_mapper, event_mapper, user_inv_mapper, event_inv_mapper = create_matrix(ratings)

    def find_similar_events(event_id, X, k, metric='cosine', show_distance=False):

        neighbour_ids = []
    
        event_ind = MC.event_mapper[event_id]
        event_vec = X[event_ind]
        k+=1
        kNN = NearestNeighbors(n_neighbors=k, algorithm="brute", metric=metric)
        kNN.fit(X)
        event_vec = event_vec.reshape(1,-1)
        neighbour = kNN.kneighbors(event_vec, return_distance=show_distance)
        for i in range(0,k):
            n = neighbour.item(i)
            neighbour_ids.append(MC.event_inv_mapper[n])
        neighbour_ids.pop(0)
        return neighbour_ids

    event_titles = dict(zip(events['Event_ID'], events['Event_description']))
