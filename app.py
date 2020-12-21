#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 13:00:30 2020

@author: nathanaelyoewono
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from summ import SumTextOne, SumTextTwo
from scrape_wikipedia import Scrape

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# interactive input output on date
@app.callback(Output('title_chosen', 'children'),
    Input('input_link','value')
)
def chosen_title(title):
    title = title.split('/')[-1].replace('_', ' ')
    return f"Title: {title}"

app.layout = html.Div([
    
    # Title
    html.H1(children='Text Summarization', 
            style={
                'textAlign': 'center',
                'paddingTop': '20px'
                }
            ),
    
    html.H4(children='Extraction Method', 
            style={
                'textAlign': 'center',
                'paddingTop':'1px',
                'font-style': 'italic'
                }
            ),
    
    # link text box
    html.Div(children=[
        
        html.Label('Text Input',
                   style={
                       'marginLeft':'50px',
                       'fontSize':'24px',
                       }),
        dcc.Input(value='https://en.wikipedia.org/wiki/Wikipedia', 
                  type='text',
                  id='input_link',
                  style={
                      'marginLeft':'50px',
                      'width': '30%'
                      })
        ]),
    
    # summary output
    html.Div(children=[
        
        html.Div(children='Summary Output',
                 style={
                     'paddingTop': '50px',
                     'marginLeft':'50px',
                     'fontSize':'24px',
                     }
                ),
        
        html.Div(id='title_chosen',
                 style={
                     'paddingTop': '25px',
                     'marginLeft':'50px',
                     'fontSize':'20px',
                     })
        
        ]),
    
    
    
])

if __name__ == '__main__':
    app.run_server(debug=True)