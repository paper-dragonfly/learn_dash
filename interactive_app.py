# If you prefer to run the code online instead of on your computer click:
# https://github.com/Coding-with-Adam/Dash-by-Plotly#execute-code-in-browser

from dash import Dash, dcc, Output, Input  # pip install dash
import dash_bootstrap_components as dbc    # pip install dash-bootstrap-components

# Build your components
app = Dash(__name__, external_stylesheets=[dbc.themes.SOLAR])
mytext = dcc.Markdown(children='',style={'color':'purple'})
myinput = dbc.Input(value="# Hello World - let's build web apps in Python!")
txtcolor = dcc.RadioItems(options=['blue ','red ','green '], inline=False)

# Customize your own Layout
app.layout = dbc.Container([mytext, myinput, txtcolor])

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
    app.run_server(debug=True, port=8052) 