# libs
import ast
import json
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from data import actor_genre, actor_amount, actor_rating, actor_studio

app = dash.Dash()

# read file
with open('../data/data.json') as f:
    data = json.load(f)
# retrieve data
actor_genre, actor_movies_genre = actor_genre(data)
actor_amount, actor_movies_year = actor_amount(data)
actor_rating = actor_rating(data)
actor_studio, actor_movies_studio = actor_studio(data)

category = ['Actor-Genre', 'Actor-Movies/Year', 'Actor-Rating', 'Actor-Studio']
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
    ], style={'display': 'block', 'width': '100%', 'align-items': 'center'}),
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
        ),
        html.Div(id='movies')
    ], style={'display': 'block', 'width': '100%'}),
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
    elif category_selected=='Actor-Movies/Year':
        data = actor_amount
        graph_type = 'chart'
        yaxis_title = 'Amount of Movies'
    elif category_selected=='Actor-Studio':
        data = actor_studio
        graph_type = 'bar'
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

# clicked graph
@app.callback(
    Output('movies', 'children'),
    [Input('graph', 'clickData'),
    Input('actor-dropdown', 'value')]
)
def show_movies(clickData, actor):
    data = json.dumps(clickData)
    data = ast.literal_eval(data)
    number = 1
    x = data['points'][0]['x']
    children = [html.H3(children='Movies from {}:'.format(x))]
    if category_selected == 'Actor-Rating' or category_selected == 'Actor-Movies/Year':
        for movie in actor_movies_year[actor][x]:
            string = str(number) + '. ' + movie
            children.append(html.P(
                children=string
            ))
            number += 1
    elif category_selected == 'Actor-Genre':
        for movie in actor_movies_genre[actor][x]:
            string = str(number) + '. ' + movie
            children.append(html.P(
                children=string
            ))
            number += 1
    elif category_selected == 'Actor-Studio':
        for movie in actor_movies_studio[actor][x]:
            string = str(number) + '. ' + movie
            children.append(html.P(
                children=string
            ))
            number += 1
        
    return children


if __name__ == '__main__':
    app.run_server(debug=True)