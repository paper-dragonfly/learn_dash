#CURRENTLY NOT WORKING :( CANT RETURN DF AS COMPONENT PROPERTY 

# Table

# import libraries
from dash import Dash, dcc, html, Output, Input
import requests 
import dash_bootstrap_components as dbc
import pdb
import pandas as pd

# create dash app
app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP]) #external_stylesheet very helpful with formatting

#build components
mytitle = dcc.Markdown(children='## Search Kid\'s Pets')
user_input = dcc.Input(value='write name here', type='text')
myresults = dcc.Markdown(children='result appears here',style={'color':'purple'})

df = pd.DataFrame(data=
    {
        "Pet Name": [],
        "Pet Type": [],
    }
)

pettable = dbc.Table.from_dataframe(df=df, striped=True, bordered=True, hover=True)

# organize components in a layout
app.layout = dbc.Container([ 
    dbc.Row([mytitle]), 
    dbc.Row([
        dbc.Col(children=user_input, width=4, style={"background-color":'green'}),
        dbc.Col(children=myresults, width = 8, style={'background-color':'pink'})
        ]),
    dbc.Row([pettable])
    ])

# Callback allows components to become interactive
@app.callback(
    Output(myresults, component_property='children'),
    Output(pettable,component_property='df'),
    Input(user_input, component_property='value'),
)
def display_names(user_input):  # function arguments come from the component property of the Input 
    sqldata:dict = requests.get('http://localhost:8050/petinfo').json() #{'pets_table':[(id, name, type, age, owner),(...,...,...)]}
    name_pets = []
    for i in range(len(sqldata['pets_table'])):
        row = sqldata['pets_table'][i]
        if row[4] == user_input: #if owner == user_input
            name_pets.append([row[1],row[2]]) #append (pet_name, pet_type)
    pets = str(name_pets)

    return f'{user_input} has these pets: {pets}',  pd.DataFrame(data=
    {
        "Pet Name": ['k'],
        "Pet Type": ['j'],
    }
) # returned objects are assigned to the component property of the Output

if __name__ == '__main__':
    app.run_server(debug=True, port=8052)