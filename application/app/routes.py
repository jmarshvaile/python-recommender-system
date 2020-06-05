import re
import json
import numpy as np
from sys import stderr
from sklearn.metrics.pairwise import cosine_similarity
from sklearn import decomposition
from matplotlib import pyplot as plt
from flask import render_template, flash, redirect, url_for, request, session
import io
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from collections import defaultdict


from app import app
from app.data import SearchFormChoices, TagCorpus, TagVectors, Games, BagOfTags
from app.forms import GameSelectForm, TagSelectForm

game_choices = None
tag_corpus = None
tag_vectors = None
games = None
bag_of_tags = None
selected_game_id = None
selected_game_index = None
selected_game = None
recommended_game_id = None
recommended_game_index = None
recommended_game = None
selected_tag_id = None
selected_tag_index = None
selected_tag = None
X_labeled = None
X = None
Y = None
X_pca = None
plots = [None, None]

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index(): 
    global game_choices
    global tag_corpus
    global tag_vectors
    global games
    global bag_of_tags
    global selected_game_id
    global selected_game_index
    global selected_game
    global recommended_game_id
    global recommended_game_index
    global recommended_game
    global selected_tag_id
    global selected_tag_index
    global selected_tag
    global X_labeled
    global X
    global Y
    global X_pca
    global plots
    
    def get_fig_url(fig):
        # Convert plot to PNG image
        pngImage = io.BytesIO()
        FigureCanvas(fig).print_png(pngImage)

        # Encode PNG image to base64 string
        pngImageB64String = "data:image/png;base64,"
        pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')

        return pngImageB64String

    def get_similarity(tag_vectors):
        X_labeled = list(zip(*tag_vectors.items()))
        X = np.array(X_labeled[1])
        Y = cosine_similarity(X)
        # Creating a mask so argmax does not cause product to return itself.
        n = len(Y)
        Y_mask = [list([False] * n) for y in Y]
        for i in range(n):
            Y_mask[i][i] = True
        Y = np.ma.MaskedArray(Y, Y_mask)
        
        return X_labeled, X, Y
    
    # Import data for game search and analysis.
    if game_choices is None:
        game_choices = SearchFormChoices()
    if tag_corpus is None:
        tag_corpus = TagCorpus()
    if tag_vectors is None:
        tag_vectors = TagVectors()
    if games is None:
        games = Games()
    if bag_of_tags is None:
        bag_of_tags = BagOfTags()

    # Create forms for user to select a game or meta tag.
    game_select_form = GameSelectForm()
    game_select_form.game_select.choices = [('', '')] + game_choices
    tag_select_form = TagSelectForm()
    tag_select_form.tag_select.choices =  [('', '')] + [(t, t) for t in tag_corpus]
    
    # Redirect on user submission and save form data to global variable.
    if game_select_form.validate_on_submit():
        selected_game_id = game_select_form.game_select.data
    if tag_select_form.validate_on_submit():
        selected_tag_id = tag_select_form.tag_select.data
    
    game_select_form.game_select.data = selected_game_id
    tag_select_form.tag_select.data = selected_tag_id
    
    # Get important variables.
    if selected_game_id is not None:
        X_labeled, X, Y = get_similarity(tag_vectors)
        
        selected_game_index = list(tag_vectors.keys()).index(selected_game_id)
        selected_game = [g for g in games if g['id'] == selected_game_id][0]
        selected_game_tags = set(selected_game['genres'] + selected_game['tags'] + selected_game['specs'])
        recommended_game_index = np.argmax(Y[selected_game_index])
        recommended_game_id = X_labeled[0][recommended_game_index]
        recommended_game = [g for g in games if g['id'] == recommended_game_id][0]
        recommended_game_tags = set(recommended_game['genres'] + recommended_game['tags'] + recommended_game['specs'])
        
        # PCA.
        X = np.array(list(tag_vectors.values()))
        selected_vector_index = [i for i, id_ in enumerate(tag_vectors) if id_ == selected_game_id][0]
        recommended_vector_index = [i for i, id_ in enumerate(tag_vectors) if id_ == recommended_game_id][0]
        pca = decomposition.PCA(n_components=2)
        pca.fit(X)
        X = pca.transform(X)
        x, y = X.T
        i, j = X[selected_vector_index].T
        k, m = X[recommended_vector_index].T
        z = Y[selected_vector_index]
        q4 = z >= np.quantile(z, .75)
        
        # PCA plots.
        # Plot 1: Selected and Recommended with top quartile conveyed.
        fig, ax = plt.subplots(figsize=(10,10))
        ax.scatter(x, y, zorder=0, facecolors='whitesmoke', edgecolors='whitesmoke', linewidth=2)
        ax.plot([i, k], [j, m], zorder=3, c='tab:blue')
        ax.scatter(i, j, zorder=4, s=100, marker='o', facecolors='black', 
                   edgecolors='black', linewidth=2, label='You Selected')
        ax.scatter(k, m, zorder=5, s=100, marker='D', facecolors='white', 
                   edgecolors='tab:blue', linewidth=3, label='We Recommended')
        ax.scatter(x[q4], y[q4], zorder=1, facecolors='none', 
                   edgecolors='lightgray', linewidth=2, label='Cosine Similarity: Top Quartile')
        
        ax.legend(fontsize=20, loc='upper right')
        ax.axes.xaxis.set_visible(False)
        ax.axes.yaxis.set_visible(False)
        plt.setp(ax.spines.values(), color='lightgray')
        fig.tight_layout()

        plots[0] = get_fig_url(fig)
        
        pca_variance = np.array([np.abs(i[0]) + np.abs(i[1]) for i in pca.components_.T])
        pca_order = pca_variance.argsort()[::-1]
        selected_game_tag_filter = np.array(tag_vectors[selected_game_id]).astype(bool)[pca_order]
        selected_game_tag_choices = np.array(tag_corpus)[pca_order]
        selected_game_tag_choices = selected_game_tag_choices[selected_game_tag_filter]
        recommended_game_tag_filter = np.array(tag_vectors[recommended_game_id]).astype(bool)[pca_order]
        recommended_game_tag_choices = np.array(tag_corpus)[pca_order]
        recommended_game_tag_choices = recommended_game_tag_choices[recommended_game_tag_filter]
        
        tag_choices = [tag for tag in selected_game_tag_choices if tag in recommended_game_tag_choices]
        tag_select_form.tag_select.choices =  [('', '')] + [(t, t) for t in tag_choices]

        if selected_tag_id is not None:
            with_tag_game = [id_ for id_, tags in bag_of_tags.items() if selected_tag_id in tags]
            with_tag_index = [X_labeled[0].index(game) for game in with_tag_game]
            # Plot: Selected and Recommended with top quartile conveyed.
            fig, ax = plt.subplots(figsize=(10,10))
            ax.scatter(x, y, zorder=0, facecolors='whitesmoke', edgecolors='whitesmoke', linewidth=2)
            ax.plot([i, k], [j, m], zorder=3, c='tab:blue')
            ax.scatter(i, j, zorder=4, s=100, marker='o', facecolors='black', edgecolors='black', linewidth=2, label='You Selected')
            ax.scatter(k, m, zorder=5, s=100, marker='D', facecolors='white', edgecolors='tab:blue', linewidth=3, label='We Recommended')
#             ax.scatter(x[q4], y[q4], zorder=1, facecolors='none', 
#                        edgecolors='lightgray', linewidth=2, label='Cosine Similarity: Top Quartile')
            ax.scatter(x[with_tag_index], y[with_tag_index], zorder=1, facecolors='none', 
                       edgecolors='lightgray', linewidth=2, label="Tagged " + selected_tag_id)
            
            ax.legend(fontsize=20, loc='upper right')
            ax.axes.xaxis.set_visible(False)
            ax.axes.yaxis.set_visible(False)
            plt.setp(ax.spines.values(), color='lightgray')
            fig.tight_layout()

            plots[1] = get_fig_url(fig)

    return render_template('index.html', title='Home', game_select_form=game_select_form, 
                           tag_select_form=tag_select_form, plots=plots, selected_game=selected_game,
                           recommended_game=recommended_game, recommended_game_tags=recommended_game_tags,
                           selected_game_tags=selected_game_tags)