# libs
import json
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
from data import actor_genre, actor_amount, actor_rating

app = dash.Dash()

# read file
with open('../data/data.json') as f:
    data = json.load(f)
# retrieve data
actor_genre = actor_genre(data)
actor_amount = actor_amount(data)
actor_rating = actor_rating(data)
# df = pd.DataFrame.from_dict(actor_genre)

category = ['Actor-Genre', 'Actor-Movies/Year', 'Actor-Rating']
global category_selected
category_selected = 'Actor-Genre'

# app layout
app.layout = html.Div([
    html.Div([
        dcc.RadioItems(
            id='category-dropdown',
            options=[{'label': k, 'value': k} for k in category],
            value=category_selected,
        )
    ], style={'display': 'inline-block', 'width': '15%'}),
    html.Div([    
        html.H1(id='category-selected'),
        html.Div(children='''
            Select actor name:
        '''),
        dcc.Dropdown(
            id='actor-dropdown',
            options=[{'label': k, 'value': k} for k in actor_genre.keys()],
            value='Denzel Washington'
        ),
        dcc.Graph(
            id='graph',
        )
    ], style={'display': 'inline-block', 'width': '85%'}),
], style={'height': '100%', 'width': '100%', 'fontFamily': 'Helvetica'})


#---- App Callback ----#
# choose category
@app.callback(
    Output('category-selected', 'children'),
    [Input('category-dropdown', 'value')]
)
def change_category(input_value):
    global category_selected
    category_selected = input_value
    return input_value

@app.callback(
    Output('actor-dropdown', 'value'),
    [Input('category-dropdown', 'value')]
)
def reset_graph(input_value):
    return 'Denzel Washington'


# generate graph
@app.callback(
    Output('graph', 'figure'),
    [Input('actor-dropdown', 'value')]
)
def create_graph(input_value):
    if category_selected=='Actor-Genre':
        data = actor_genre
        graph_type = 'bar'
        yaxis_title = 'Amount of Movies'
    elif category_selected=='Actor-Rating':
        data = actor_rating
        graph_type = 'chart'
        yaxis_title = 'Average Rating'
    else:
        data = actor_amount
        graph_type = 'chart'
        yaxis_title = 'Amount of Movies'
    figure = {
        'data': [
            {'x': [x for x in data[input_value].keys()], 'y': [y for y in data[input_value].values()], 'type': graph_type, 'name': 'movies'}
        ],
        'layout': go.Layout(
            yaxis={'title': yaxis_title},
        )
    }

    return figure


if __name__ == '__main__':
    app.run_server(debug=True)