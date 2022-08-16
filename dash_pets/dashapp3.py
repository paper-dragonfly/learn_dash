#INFO
# Dash app with request to flask API
# Lists childrens names
# takes child name as input (campitalization ignored)
# Returns info on all pets owned by that child 
# Add a pet by filling out form fields and clicking submit

from dash import Dash, dcc
from dash.dependencies import Output, Input, State
import dash_bootstrap_components as dbc
import pandas as pd
import requests

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP]) 

sqldata:dict = requests.get('http://localhost:8050/petinfo').json() #{'pets_table':[(id, name, type, age, owner),(...,...,...)]}

kid_names=[]
for i in range(len(sqldata['pets_table'])):
    if sqldata['pets_table'][i][4].capitalize() not in kid_names:
        kid_names.append(sqldata['pets_table'][i][4].capitalize())
kid_names = ', '.join(kid_names)

app.layout = dbc.Container([
    # Intro
    dbc.Row(children=dcc.Markdown(id='header', children='# Search Pets by Kid')),
    dbc.Row(children=dcc.Markdown(id='h2names',children='### Kids in Grade 2 with Pets')),
    dbc.Row(children=dcc.Markdown(id='kid_names', children=kid_names )),
    #Pet search + results table
    dbc.Row(children=dcc.Markdown(id='search_bar', children='#### Write child\'s name to see info about their pets')),
    dbc.Row(children=dcc.Input(id='userinput', value='')),
    dbc.Row(id= 'mytable', children = None),
    # add pet
    dbc.Row(children=dcc.Markdown(id = 'h3newpet', children = '### Add Pet')),
    dbc.Row(children=dcc.Markdown(id='pet_name', children = 'Pet Name')),
    dbc.Row(children=dcc.Input(id='ui_pet_name', value = '')),
    dbc.Row(children=dcc.Markdown(id='pet_type', children= 'Pet Type')),
    dbc.Row(children=dcc.Input(id='ui_pet_type', value = '')),
    dbc.Row(children=dcc.Markdown(id='pet_age', children = 'Pet Age')),
    dbc.Row(children=dcc.Input(id='ui_pet_age', value='', type='number')),
    dbc.Row(children=dcc.Markdown(id='pet_owner', children = 'Name of child that owns pet')),
    dbc.Row(children=dcc.Input(id='ui_pet_owner', value='')),
    dbc.Row(children=dbc.Button(id='submit_button', children='submit', n_clicks=0,color='primary')),
    # search pets by form 
    dcc.Markdown(id='h4', children='#### Search DB - fill some or all feilds'),
    dbc.Row([
        dbc.Col(children=dbc.Label(children='Pet Name', html_for='ui_pname'), width=3),
        dbc.Col(children=dcc.Input(id='ui_pname', value=""), width=9)]),
    dbc.Row([
        dbc.Col(children=dbc.Label(children='Pet Type', html_for='ui_ptype'), width=3),
        dbc.Col(children= dcc.Input(id='ui_ptype', value=""), width=9)]),
    dbc.Row(children=dbc.Button(id='submit-button2', children='search', n_clicks=0, color='primary')),
    dbc.Row(id='table2', children=None)  
])

# Pets by Kid Table
@app.callback(
    Output('mytable','children'),
    Input('userinput','value')
)
def make_table (usertxt):
    sqldata:dict = requests.get('http://localhost:8050/petinfo').json()
    data = sqldata['pets_table']
    results_table = {'pet_name':[],'pet_type':[],'pet_age':[]}
    for i in range(len(data)):
        if data[i][4] == usertxt.lower():
            results_table['pet_name'].append(data[i][1])
            results_table['pet_type'].append(data[i][2])
            results_table['pet_age'].append(data[i][3])
    df = pd.DataFrame(results_table)
    return dbc.Table.from_dataframe(df, striped=True, bordered=True)

# Add Pet
@app.callback(
    Output('submit_button', 'color'),
    Input('submit_button', 'n_clicks'),
    State('ui_pet_name','value'),
    State('ui_pet_type','value'),
    State('ui_pet_age','value'),
    State('ui_pet_owner','value')
)
def change_color(n_clicks, pname, ptype, page, powner):
    if pname and ptype and page and powner:
        data = {'pet_name':pname, 'pet_type':ptype, 'pet_age':page, 'pet_owner':powner}
        flask_resp = requests.post('http://localhost:8050/addpet', json=data).json()
        print('FLASK RESPONSE', flask_resp)
        if flask_resp['status_code'] == 200:
            return 'success'
        else:
            return 'danger'
    else:
        return 'secondary'

#Search Database by Form Feilds
# TODO: figure out how to use button in this instance
# TODO: figure out git ask NICO
@app.callback(
    Output('table2', 'children'),
    # Input('submit-button2', 'n-clicks'),
    Input('ui_pname', 'value'),
    Input('ui_ptype', 'value')
)
def search_db(pname, ptype):
    sqldata:dict = requests.get('http://localhost:8050/petinfo').json()
    data = sqldata['pets_table']
    feild_data = [pname, ptype]
    if '' in feild_data:
        feild_data.remove("")
    results_table = {'pet_name':[],'pet_type':[],'pet_age':[], 'owner_name':[]}
    for i in range(len(data)):
        if data[i][1] == pname and data[i][2] == ptype:
            results_table['pet_name'].append(data[i][1])
            results_table['pet_type'].append(data[i][2])
            results_table['pet_age'].append(data[i][3])
            results_table['owner_name'].append(data[i][4])
    df = pd.DataFrame(results_table)
    return dbc.Table.from_dataframe(df, striped=True, bordered=True)

if __name__ == '__main__':
    app.run_server(debug=True, port=8055)