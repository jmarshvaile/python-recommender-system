import re
import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn import decomposition
from matplotlib import pyplot as plt
from flask import render_template, flash, redirect, url_for, request
import io
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from collections import defaultdict

from app import app
from app.data import SearchFormChoices
from app.forms import GameSelectForm, TagSelectForm

# def get_fig_url(fig):
#     # Convert plot to PNG image
#     pngImage = io.BytesIO()
#     FigureCanvas(fig).print_png(pngImage)
    
#     # Encode PNG image to base64 string
#     pngImageB64String = "data:image/png;base64,"
#     pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
    
#     return pngImageB64String



choices = SearchFormChoices()
    
@app.route('/')
@app.route('/index')
def index():
    choices = SearchFormChoices()
    
    flash([item for item in request.form])
    flash('game_select' in request.form.keys())
    flash('tag_select' in request.form.keys())
    
    if 'game_select' not in request.form.keys():
        game_select_form = GameSelectForm()
        game_select_form.game_select.choices = [('', '')] + choices
        
    if 'tag_select' not in request.form.keys()
        tag_select_form = TagSelectForm()
        tag_select_form.tag_select.choices = [('', '')] + choices
    
    return render_template('index.html', title='Home', game_select_form=game_select_form, tag_select_form=tag_select_form)

@app.route('/search', methods=['POST'])
def search():
    choices = SearchFormChoices()
    
    flash([item for item in request.form])
    flash('game_select' in request.form.keys())
    flash('tag_select' in request.form.keys())
    
    if 'game_select' not in request.form.keys():
        game_select_form = GameSelectForm()
        game_select_form.game_select.choices = [('', '')] + choices
        
    if 'tag_select' not in request.form.keys()
        tag_select_form = TagSelectForm()
        tag_select_form.tag_select.choices = [('', '')] + choices
    
    if game_select_form.validate_on_submit():
        return redirect(url_for('index'))
    
    return render_template('index.html', title='Home', game_select_form=game_select_form, tag_select_form=tag_select_form)

@app.route('/tags', methods=['POST'])
def tags():
    choices = SearchFormChoices()
    
    flash([item for item in request.form])
    flash('game_select' in request.form.keys())
    flash('tag_select' in request.form.keys())
    
    if 'game_select' not in request.form.keys():
        game_select_form = GameSelectForm()
        game_select_form.game_select.choices = [('', '')] + choices
        
    if 'tag_select' not in request.form.keys()
        tag_select_form = TagSelectForm()
        tag_select_form.tag_select.choices = [('', '')] + choices
    
    if tag_select_form.validate_on_submit():
        return redirect(url_for('index'))
    
    return render_template('index.html', title='Home', game_select_form=game_select_form, tag_select_form=tag_select_form)

# @app.route('/search_t', methods=['GET', 'POST'])
# def search():
#     filepath = 'static/select_form_values.json'
#     with open(filepath, 'r') as file:
#         choices = json.load(file)
        
#     form = SelectForm()
#     form.select.choices = [('', '')] + choices
#     form.submit.label.text = 'Find Similar'
    
#     form2 = SelectForm()
#     form2.select.choices = [('', '')] + choices
#     form2.submit.label.text = 'Show Tag'
    
# #     if form.validate_on_submit():
# #         return render_template('search_t.html', form=form, form2=form2)
#     return render_template('search_t.html', form=form, form2=form2)

# def find_similar():
#     #     Find Best Fit: Cosine Similarity
#     selected = None
#     recommended = None
#     plots = None
#     tag_form = SelectForm2()
#     if form.validate_on_submit():
#         filepath = 'static/tag_vectors.json'
#         with open(filepath, 'r') as file:
#             tag_vectors = json.load(file)

#         X_labeled = list(zip(*tag_vectors.items()))
#         X = np.array(X_labeled[1])
#         Y = cosine_similarity(X)
        
#         # Creating a mask so argmax does not cause product to return itself.
#         n = len(Y)
#         Y_mask = [list([False] * n) for y in Y]
#         for i in range(n):
#             Y_mask[i][i] = True
#         Y = np.ma.MaskedArray(Y, Y_mask)
        
#         selected_id = form.select.data
#         selected_index = X_labeled[0].index(selected_id)
#         recommended_index = np.argmax(Y[selected_index])
#         recommended_id = X_labeled[0][recommended_index]
        
#         filename = 'static/processed_games.json'
#         with open(filename, 'r') as file:
#             games = json.load(file)
            
#         selected = [game for game in games if game['id'] == selected_id][0]
#         recommended = [game for game in games if game['id'] == recommended_id][0]
        
#         # PCA
        
#         X = np.array(list(tag_vectors.values()))

#         selected_vector_index = [i for i, id_ in enumerate(tag_vectors) if id_ == selected_id][0]
#         recommended_vector_index = [i for i, id_ in enumerate(tag_vectors) if id_ == recommended_id][0]
        
#         pca = decomposition.PCA(n_components=2)
#         pca.fit(X)
#         X = pca.transform(X)
#         x, y = X.T
#         i, j = X[selected_vector_index].T
#         k, m = X[recommended_vector_index].T
        
#         z = Y[selected_vector_index]
#         q4 = z >= np.quantile(z, .75)
        
#         plots = []
        
#         # Plot: Selected and Recommended with top quartile conveyed.
#         fig, ax = plt.subplots(figsize=(10,10))
#         ax.scatter(x, y, zorder=0, facecolors='whitesmoke', edgecolors='whitesmoke', linewidth=2)
#         ax.plot([i, k], [j, m], zorder=3, c='tab:blue')
#         ax.scatter(i, j, zorder=4, s=100, marker='o', facecolors='black', edgecolors='black', linewidth=2, label='You Selected')
#         ax.scatter(k, m, zorder=5, s=100, marker='D', facecolors='white', edgecolors='tab:blue', linewidth=3, label='We Recommended')
#         ax.scatter(x[q4], y[q4], zorder=1, facecolors='none', edgecolors='lightgray', linewidth=2, label='Cosine Similarity: Top Quartile')
#         ax.legend(fontsize=20, loc='upper right')

#         ax.axes.xaxis.set_visible(False)
#         ax.axes.yaxis.set_visible(False)
#         plt.setp(ax.spines.values(), color='lightgray')
#         fig.tight_layout()
        
#         plots.append(get_fig_url(fig))
#         plt.clf()
        
#         # Tag filter for plot.
        
#         filepath = 'static/tag_corpus.json'
#         with open(filepath, 'r') as file:
#             tag_corpus = json.load(file)

#         pca_variance = np.array([np.abs(i[0]) + np.abs(i[1]) for i in pca.components_.T])
#         pca_order = pca_variance.argsort()[::-1]

#         selected_tag_filter = np.array(tag_vectors[selected_id]).astype(bool)[pca_order]
#         selected_tag_choices = np.array(tag_corpus)[pca_order]
#         selected_tag_choices = selected_tag_choices[selected_tag_filter]

#         recommended_tag_filter = np.array(tag_vectors[recommended_id]).astype(bool)[pca_order]
#         recommended_tag_choices = np.array(tag_corpus)[pca_order]
#         recommended_tag_choices = recommended_tag_choices[recommended_tag_filter]

#         tag_choices = [tag for tag in selected_tag_choices if tag in recommended_tag_choices]
        
#         tag_form = SelectForm()
#         tag_form.select.choices = tag_choices
#         tag_form.submit.label.text = 'Show Games With Tag'
        
#         if tag_form.validate_on_submit():
#             selected_tag = tag_form.select.data
            
#             filepath = 'data/bag_of_tags.json'
#             with open(filepath, 'r') as file:
#                 bag_of_tags = json.load(file)
            
#             with_tag_game = [id_ for id_, tags in bag_of_tags.items() if selected_tag in tags]
#             with_tag_index = [X_labeled[0].index(game) for game in with_tag_game]
            
#             # Plot: Selected and Recommended with top quartile conveyed.
#             fig, ax = plt.subplots(figsize=(10,10))
#             ax.scatter(x, y, zorder=0, facecolors='whitesmoke', edgecolors='whitesmoke', linewidth=2)
#             ax.plot([i, k], [j, m], zorder=3, c='tab:blue')
#             ax.scatter(i, j, zorder=4, s=100, marker='o', facecolors='black', edgecolors='black', linewidth=2, label='You Selected')
#             ax.scatter(k, m, zorder=5, s=100, marker='D', facecolors='white', edgecolors='tab:blue', linewidth=3, label='We Recommended')
#             ax.scatter(x[q4], y[q4], zorder=1, facecolors='none', 
#                        edgecolors='lightgray', linewidth=2, label='Cosine Similarity: Top Quartile')
#             ax.scatter(x[with_tag_index], y[with_tag_index], zorder=0, facecolors='tab:orange', edgecolors='tab:orange', linewidth=2)
#             ax.legend(fontsize=20, loc='upper right')

#             ax.axes.xaxis.set_visible(False)
#             ax.axes.yaxis.set_visible(False)
#             plt.setp(ax.spines.values(), color='lightgray')
#             fig.tight_layout()

#             plots.append(get_fig_url(fig))
            
#             return render_template('search.html', title='Search', form=form, tag_form=tag_form, 
#                            selected=selected, recommended=recommended, plots=plots)
#     return render_template('search.html', title='Search', form=form, tag_form=tag_form, 
#                            selected=selected, recommended=recommended, plots=plots)