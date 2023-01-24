from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

app = Dash(__name__)

app.layout = html.Div(
    style={
            'background-image': 'url(“diginex.png”)',
        },
    children = [
                    html.H1('Hello World'), 
                    html.P('This image has an image in the background')
    ])
 



if __name__ == '__main__':
    app.run_server(debug=True)