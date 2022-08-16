#INFO
# Dash app, no flask connection
# takes pet type (dog/cat) as input and returns owner_name, owner_age, pet_type
# breakthrough in updating table info based on user_input

from dash import Dash, dcc, Output, Input
import dash_bootstrap_components as dbc
import pandas as pd

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP]) 

app. layout = dbc.Container([
    dbc.Row(children=dcc.Markdown(id='header', children='# Pet Table')),
    dbc.Row(children=dcc.Markdown(id='input_explained', children='#### Write pet type here to see info on owner')),
    dbc.Row(children=dcc.Input(id='userinput', value='')),
    dbc.Row(id= 'mytable', children = None)
])

@app.callback(
    Output('mytable','children'),
    Input('userinput','value')
)
def make_table (usertxt):
    data = {'name':['jane','sam','fred'], 'age':[15,4,22], 'pet':['dog','cat','dog']}
    d2 = {'name':[],'age':[],'pet':[]}
    for i in range(len(data['pet'])):
        if data['pet'][i] == usertxt:
            d2['name'].append(data['name'][i])
            d2['age'].append(data['age'][i])
            d2['pet'].append(data['pet'][i])

    df = pd.DataFrame(d2)
    # df = pd.DataFrame({'Name':['jane','sam','fred'], 'age':[15,4,22], 'pet':['dog','cat','dog']})

    return dbc.Table.from_dataframe(df, striped=True, bordered=True)

if __name__ == '__main__':
    app.run_server(debug=True, port=8055)