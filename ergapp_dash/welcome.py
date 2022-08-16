from dash import Dash, dcc, html, Input, Output                # pip install dash
import dash_bootstrap_components as dbc  # pip install dash-bootstrap-components

# Build your components
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
welcome = dcc.Markdown(children="# Welcome to ErgLog")
# user_choice = dcc.RadioItems(options=['Login','Create New User'], value='')
login_btn = html.Button(children='Login')
new_user_btn = html.Button(children='Create New User')


# Customize your own Layout
app.layout = dbc.Container([welcome, login_btn, new_user_btn ])

# Callback allows components to interact
@app.callback(
    Output(mytext, component_property='children'),
    Output(mytext, component_property='style'),
    Input(myinput, component_property='value'),
    Input(txtcolor, component_property='value')
)
def update_title(user_input, color_choice):  # function arguments come from the component property of the Input 
    return user_input, {'color':color_choice}  # returned objects are assigned to the component property of the Output

# Run app
if __name__=='__main__':
    app.run_server(debug=True, port=8070)