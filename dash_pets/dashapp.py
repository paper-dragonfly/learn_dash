#import libraries
from dash import Dash, dcc, html, Output, Input
import requests 
import dash_bootstrap_components as dbc
import pdb
import pandas as pd

# create dash app
app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP]) #external_stylesheet very helpful with formatting

#build components
mytitle = dcc.Markdown(children='## Search Kid\'s Pets')
user_input = dcc.Input(value='jane', type='text')
myresults = dcc.Markdown(children='house',style={'color':'blue'})


# organize components in a layout - eg creating columns
app.layout = dbc.Container([ 
    dbc.Row([mytitle]), 
    dbc.Row([
        dbc.Col(children=user_input, width=4, style={"background-color":'green'}),
        dbc.Col(children=myresults, width = 8, style={'background-color':'pink'})
        ])
    ])

# Callback allows components to become interactive
@app.callback(
    Output(myresults, component_property='children'),
    Input(user_input, component_property='value'),
)
def display_names(user_input):  # function arguments come from the component property of the Input 
    sqldata = requests.get('http://localhost:8050/kids').json()
    name_pets = []
    for i in range(len(sqldata['pets_table'])):
        row = sqldata['pets_table'][i]
        if row[4] == user_input:
            name_pets.append([row[1],row[2]])
        pets = str(name_pets)

    return f'{user_input} has these pets: {pets}'  # returned objects are assigned to the component property of the Output

if __name__ == '__main__':
    app.run_server(debug=True, port=8052)