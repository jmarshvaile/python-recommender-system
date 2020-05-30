import json

def SearchFormChoices():
    filepath = 'static/select_form_values.json'
    with open(filepath, 'r') as file:
        choices = json.load(file)
        
    return choices