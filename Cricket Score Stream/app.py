from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import requests
import json
from dash.dependencies import Input, Output, State
import datetime as dt
from flags_png import logo_icons

match_details = {
    'series_name':'',
    'match_name':'',
    'venue':'',
    'match_date':'',
    'time':'',
    'team1':'',
    'team2_code':'',
    'team2':'',
    'team2_code':''
}

live_match_details = {
    'batting':'',
    'bowling':'',
    'innings':''
}


## API credentials
url = "https://cricket-live-data.p.rapidapi.com/match/2697317"

headers = {
    'X-RapidAPI-Key': '992aa0cdeamsh49c0b706894f155p1b21e0jsnbc60bc481a51',
    'X-RapidAPI-Host': 'cricket-live-data.p.rapidapi.com'
}


### Get basic details about the match, like series name, venue, which teams are playing etc (ADD match type)
def getbasicinfo():
    response = requests.request("GET", url, headers=headers)
    json_data = response.json()
    # print(json_data)
    match_details['series_name'] = json_data['results']['fixture']['series']['series_name']
    match_details['match_name'] = json_data['results']['fixture']['match_title']
    match_details['venue'] = json_data['results']['fixture']['venue']
    match_details['match_date'] = json_data['results']['fixture']['start_date'].split('T')[0]
    match_details['team1'] = json_data['results']['fixture']['home']['name']
    match_details['team1_code'] = json_data['results']['fixture']['home']['code'] 
    match_details['team2'] = json_data['results']['fixture']['away']['name']
    match_details['team2_code'] = json_data['results']['fixture']['away']['code']

# getbasicinfo() ## Run as and when scheduled.
getbasicinfo()
app = Dash(__name__, update_title=None)
app.title = match_details['series_name']
server = app.server

app.layout = html.Div(
    children=[  
        ## Background Stage
        html.Div(
            id='background',
            className='background_img'
        ),      
        # Head Bar
        html.Div(
            id='Head Bar',
            children=[
                html.Div(
                    id='Team1 Logo',
                    children=[
                        html.Img(
                            src=app.get_asset_url(
                                logo_icons[match_details['team1'].lower()]),
                            style={
                                'height': '100%',
                            }
                        )
                    ],
                    style={
                        'height': '100%',
                        'width': '30%',
                        # 'border': '1px solid #ffffff',
                        'float': 'left',
                        'display': 'flex',
                        'position': 'relative',
                        'opacity': '1'
                    }),
                html.Div(
                    match_details['series_name'],
                    id='Series Name',
                    style={
                        'height': '100%',
                        'width': '40%',
                        # 'border': '1px solid #ffffff',
                        # 'float': 'left',
                        'display': 'flex',
                        'position': 'absolute',
                        'justify-content': 'center',
                        'align-items': 'end',
                        'font-size': '40px',
                        'font-weight': 'bold',
                        'left': '30%'
                    }),
                html.Div(
                    id='Team2 Logo',
                    children=[
                        html.Img(
                            src=app.get_asset_url(
                                logo_icons[match_details['team2'].lower()]),
                            style={
                                'height': '100%',
                                'position': 'absolute',
                                'right': '0px'
                            }
                        )
                    ],
                    style={
                        'height': '100%',
                        'width': '30%',
                        # 'border': '1px solid #ffffff',
                        'float': 'right',
                        'display': 'flex',
                        'position': 'relative',
                        'opacity': '1',
                    }),
            ],
            style={
                'height': '10%',
                'width': '100%',
                'position': 'absolute'}
        ),
    ]   
)


if __name__ == '__main__':
    app.run_server(debug=True)
