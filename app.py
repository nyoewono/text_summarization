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

import time

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# interactive input output on date
@app.callback([Output('title_chosen', 'children'),
               Output('result_one', 'value'),
               Output('result_two', 'value'),
               Output('sent_slider', 'max')],
    [Input('input_link','value'),
     Input('threshold_slider', 'value'),
     Input('sent_slider', 'value')]
)
def sum_result(title, threshold, k):
    
    #threshold=2
    #k=5
    
    # get the article title
    title = title.split('/')[-1].replace('_', ' ')
    
    # scrape the article in wikipedia
    scraper = Scrape(title)
    article = scraper._fetch_article()
    
    # summarize the article
    summarizer_one = SumTextOne(article)
    summarizer_two = SumTextTwo(article)
    
    sum_one = summarizer_one.summarize(threshold)
    sum_two = summarizer_two.summarize(k)
    
    if sum_one == '' or sum_two == '':
        sum_one = 'Result not found'
        sum_two = 'Result not found'
    #print(summarizer_one.summarize(threshold))
    max_sent = summarizer_two._get_num_sent()
    
    time.sleep(3)
    
    
    return f"Title: {title}", sum_one, sum_two, max_sent

@app.callback(Output('num_sent_chosen', 'children'),
              Input('sent_slider', 'value'))
def sent_chosen(k):
    return f'Number of sentence chosen: {k}'

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
                     }
                 ),
        
        html.Div(children=[
            
            # summary algo one
            html.Div(children='SumTextOne',
                 style={
                     'paddingTop': '15px',
                     'marginLeft':'50px',
                     'fontSize':'20px',
                     }
                 ),
            html.Div(children='Pick threshold',
                     style={
                         'marginLeft':'50px'
                         
                         }),
            dcc.Dropdown(
                id='threshold_slider',
                options=[
                    {'label': '1', 'value': 1},
                    {'label': '1.5', 'value': 1.5},
                    {'label': '2', 'value': 2},
                    {'label': '2.5', 'value': 2.5},
                    {'label': '3', 'value': 3}
                ],
                value=2,
                style={'width':'20%', 'marginLeft':'25px',}),
            dcc.Loading(children=[
                dcc.Textarea(
                    id='result_one',
                    value='Result from SumTextOne algorithm',
                    style={'width': '90%', 
                           'height': 300,
                           'marginLeft':'50px',
                           'marginRight':'50px',
                           'marginTop':'10px'},
                    )
                ],
                id="loading-1",
                type="default")
            ,
            
            # summary algo two
            html.Div(children='SumTextTwo',
                 style={
                     'paddingTop': '15px',
                     'marginLeft':'50px',
                     'fontSize':'20px',
                     }
                 ),
            dcc.Slider(
                id='sent_slider',
                min=0,
                value=5,
                included=False,
            ),
            html.Div(id='num_sent_chosen',
                     style={
                        'marginLeft':'50px'
                         }),
            dcc.Loading(children=[
                dcc.Textarea(
                    id='result_two',
                    value='Result from SumTextTwo algorithm',
                    style={'width': '90%', 
                           'height': 300,
                           'marginLeft':'50px',
                           'marginRight':'50px'},
                    )
                ],
                id="loading-2",
                type="default")
            ])
            
        ]),
    
    
    
    
])

if __name__ == '__main__':
    app.run_server(debug=True)