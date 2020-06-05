import json

def SearchFormChoices():
    filepath = 'static/select_form_values.json'
    with open(filepath, 'r') as file:
        choices = json.load(file)
        
    return choices

def TagVectors():
    filepath = 'static/tag_vectors.json'
    with open(filepath, 'r') as file:
        tag_vectors = json.load(file)
        
    return tag_vectors

def Games():
    filename = 'static/processed_games.json'
    with open(filename, 'r') as file:
        games = json.load(file)
        
    return games

def TagCorpus():
    filepath = 'static/tag_corpus.json'
    with open(filepath, 'r') as file:
        tag_corpus = json.load(file)

    return tag_corpus

def BagOfTags():
    filepath = 'static/bag_of_tags.json'
    with open(filepath, 'r') as file:
        bag_of_tags = json.load(file)
    
    return bag_of_tags