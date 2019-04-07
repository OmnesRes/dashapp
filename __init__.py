
# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
import json

external_stylesheets = ["https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css",
                        {'rel':"stylesheet",
                     'href':"https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css",
                     'integrity':"sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T",
                     'crossorigin':"anonymous"}]




external_scripts = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets,external_scripts=external_scripts)

app.config.supress_callback_exceptions = True
##load functions and data
from misc import *


data = [go.Histogram(
    x=expression,
    nbinsx=100,
    hoverinfo='none'
    )]

layout = go.Layout(title = 'Histogram',

    yaxis = dict(zeroline = False,
            showgrid = False,
            showticklabels=True,
            title="Count",
            fixedrange=True),
    xaxis = dict(zeroline = False,
            showgrid = False,
            showticklabels=True,
            title="Reads",
            fixedrange=True,
            ),
    hoverlabel=dict(bgcolor='white',
                    font=dict(color='black',size=24)),
    dragmode='select',
    selectdirection='h'
)

histogram = go.Figure(data=data, layout=layout)


app.layout = html.Div(children=[
    html.Div(className='col-sm-12',children=[


        html.Div(className='col-sm-3',children=[
            dcc.Dropdown(id='selections',
                         options=[
                            {'label': 'Survival', 'value': 'surv'},
                            {'label': 'Expression', 'value': 'exp'},
                         ],
                         value=['surv', 'exp'],
                         multi=True
            ),
        ]),
        html.Div(className='col-sm-9'
        ),
    ]),

    html.Div(id='debugging',style=dict(textAlign='center',fontSize=24,color='red')),
    html.Div(id='temp_value',style={'display': 'none'},children='50'),
    html.Div(className='row',children=[
        html.Div(id='survival',style={'display': 'none'},className='col-sm-12',children=[
                    html.Div(id='forms',className='col s12',children=[
                        html.Form(className='col s12',children=[
                            html.Div(className='row',children=[
                                html.Div(className='col s4'),
                                html.Div(className='col s4',children=[
                                    html.Div(className='input-field col s6',children=[
                                        dcc.Input(id='lower', type='text',placeholder='50',style=dict(textAlign='right')),
                                        html.Label(htmlFor='lower',children='Lower',style=dict(textAlign='right',width='50%'))]),
                                    html.Div(className='input-field col s6',children=[
                                        dcc.Input(id='upper', type='text',placeholder='50',style=dict(textAlign='right')),
                                        html.Label(htmlFor='upper',children='Upper',style=dict(textAlign='right',width='50%'))]),
                                    ]),
                                html.Div(className='col s4')
                            ])
                        ])
                    ]),
                    html.Div(id='graphs')
        ]),
        html.Div(id='expression',style={'display': 'none'},className='col-sm-12',children=[
            dcc.Graph(id='histogram',figure=histogram)
        ])
    ]),
    html.Div(id='output-data')
])



##@app.callback(
##    Output('output-data', 'children'),
##    [Input('histogram', 'selectedData')])
##def display_selected_data(selectedData):
##    return str(selectedData)




@app.callback(
    [Output('expression','style'),
     Output('expression','className')],
    [Input('selections', 'value')]
    )

def show_expression(selections):
    if 'exp' in selections:
        style={'margin': '0 auto'}
    else:
        style={'display': 'none'}
    if len(selections)==2:
        className='col-sm-6'
    else:
        className='col-sm-8'
    return style, className
        




@app.callback(
    [Output('survival','style'),
     Output('survival','className')],
    [Input('selections', 'value')]
    )

def show_survival(selections):
    if 'surv' in selections:
        style={'margin': '0 auto'}
    else:
        style={'display': 'none'}
    if len(selections)==2:
        className='col-sm-6'
    else:
        className='col-sm-8'
    return style, className
        

@app.callback(
    Output('graphs','children'),
    [Input('lower', 'value'),
     Input('upper', 'value'),
     Input('histogram', 'selectedData'),
     Input('selections', 'value')],
    )

def update_kaplan(lower,upper,selection,selections):
    toggle=False
    try:
        if 'exp' not in selections:
            lower=int(lower)
            upper=int(upper)
            bottom=sorted(patient_data[:int(len(patient_data)*lower/100.0)])
            top=sorted(patient_data[-1*int(len(patient_data)*upper/100.0):])
        else:
            lower=selection['range']['x'][0]
            upper=selection['range']['x'][1]
            bottom=sorted([i for i in patient_data if i[2]>lower and i[2]<upper])
            top=sorted([i for i in patient_data if i[2]<lower or i[2]>upper])
            toggle=True
            
    except:
        if lower==None and upper==None:
            lower=50
            upper=50
        else:
            lower=int(lower)
            upper=int(upper)

        bottom=sorted(patient_data[:int(len(patient_data)*lower/100.0)])
        top=sorted(patient_data[-1*int(len(patient_data)*upper/100.0):])

    k_plot=kaplan(bottom)

    if k_plot[-1][-1][0]>k_plot[0][-1][0]:
        x_end=[k_plot[-1][-1][0]]
        y_end=[k_plot[-1][-1][1]]
    else:
        x_end=[]
        y_end=[]

    if toggle==True:
        selection['range']['x'][0]
        trace1_label='Selected<br>N='
    else:
        trace1_label='Low Expression<br>N='
    trace1 = go.Scatter(
        x=[0]+[i[0] for i in k_plot[0]]+x_end,
        y=[i[1] for i in k_plot[0]]+[k_plot[1][-1][2]]+y_end,
        hoverinfo='text+x+y',
        text=['']+[i[-1] for i in k_plot[1]],
        mode='lines',
        name=trace1_label+str(len(bottom)),
        showlegend=True,
        legendgroup='lower',
        line=dict(color='blue',
                  dash='solid',
                  shape='hv',
                  width=1.5,)
        )

    trace2 = go.Scatter(
        x=[i[0] for i in k_plot[2]],
        y=[i[1] for i in k_plot[2]],
        text=[i[-1] for i in k_plot[2]],
        hoverinfo='text+x+y',
        mode='markers',
        legendgroup='lower',
        marker=dict(opacity=1,symbol='line-ns-open',size=3,color='blue'),
        showlegend=False
        )

    k_plot=kaplan(top)

    if k_plot[-1][-1][0]>k_plot[0][-1][0]:
        x_end=[k_plot[-1][-1][0]]
        y_end=[k_plot[-1][-1][1]]
    else:
        x_end=[]
        y_end=[]

    
    if toggle==True:
        selection['range']['x'][0]
        trace3_label='Not Selected<br>N='
    else:
        trace3_label='High Expression<br>N='
    trace3 = go.Scatter(
        x=[0]+[i[0] for i in k_plot[0]]+x_end,
        y=[i[1] for i in k_plot[0]]+[k_plot[1][-1][2]]+y_end,
        hoverinfo='text+x+y',
        text=['']+[i[-1] for i in k_plot[1]],
        mode='lines',
        legendgroup='higher',
        name=trace3_label+str(len(top)),
        showlegend=True,
        line=dict(color='red',
                  dash='solid',
                  shape='hv',
                  width=1.5,)
        )

    trace4 = go.Scatter(
        x=[i[0] for i in k_plot[2]],
        y=[i[1] for i in k_plot[2]],
        text=[i[-1] for i in k_plot[2]],
        hoverinfo='text+x+y',
        mode='markers',
        legendgroup='higher',
        marker=dict(opacity=1,symbol='line-ns-open',size=3,color='red'),
        showlegend=False
        )

    data=[trace1,trace2,trace3,trace4]

    layout = go.Layout(
        yaxis = dict(zeroline = False,
                showgrid = False,
                showticklabels=True,
                tickfont=dict(size=16),
                title=dict(text="Survival probability",font=dict(size=20)),
                     ),
        xaxis = dict(zeroline = False,
                showgrid = False,
                showticklabels=True,
                tickfont=dict(size=16),
                rangemode= 'nonnegative',
                title=dict(text='Days',font=dict(size=20))
                     ),
        hoverlabel=dict(bgcolor='white',
                        font=dict(color='black',size=24)),
        legend=dict(x=.75,
                    y=1,
                    font=dict(size=16)),
        margin=go.layout.Margin(
            r=0,
            t=0,
            b=50,
            l=60,
            pad=0
        ),
        hovermode='closest',
    )

    kaplan_plot = go.Figure(data=data, layout=layout)


    first_line='{0:<16}{1:<5}{2:>10}{3:>15}'.format('Patient','Days','Status','Expression\n')
    lower_patients=first_line+''.join(['{0:<15} {1:<5} {2:>9} {3:>14}\n'.format(i[-1],str(i[0]),'Alive' if i[1]==0 else 'Dead',i[2]) for i in bottom])
    upper_patients=first_line+''.join(['{0:<15} {1:<5} {2:>9} {3:>14}\n'.format(i[-1],str(i[0]),'Alive' if i[1]==0 else 'Dead',i[2]) for i in top])

    
    data = [go.Scatter(
    x=range(0,len(bottom+top)),
    y=[1]*len(patients),
    text=[i[-1] for i in bottom+top],
    hoverinfo='text',
    mode='markers',
    marker=dict(opacity=0)
    )]

    layout = go.Layout(
        autosize=False,
        width=7000,
        height=50,
        yaxis = dict(zeroline = False,
                showgrid = False,
                range=[-.1,1.1],
                showticklabels=False,
                fixedrange=True
                ),
        xaxis = dict(zeroline = False,
                showgrid = False,
                showticklabels=False,
                range=[-1,523],
                ),
        shapes=[dict(type='line',
                    x0=i,
                    y0=0,
                    x1=i,
                    y1=1,
                    line = dict(color='blue',
                                width=10))\
            for i in range(0,len(bottom))]+[
                dict(type='line',
                    x0=i,
                    y0=0,
                    x1=i,
                    y1=1,
                    line = dict(color='red',
                                width=10))\
            for i in range(len(bottom),len(bottom)+len(top))],
        hoverlabel=dict(bgcolor='white',
                        font=dict(color='black',size=24)),
        dragmode='pan',
        margin=go.layout.Margin(
            l=0,
            r=0,
            b=0,
            t=0,
            pad=0
        )
    )

    oncoprint = go.Figure(data=data, layout=layout)

    graphs=[html.Div(children=[
                html.Div(style={'textAlign': 'center'},children=[html.H3('Kaplan'),
                    dcc.Graph(figure=kaplan_plot,
                              #className='col-sm-12',
                              style={'margin':'0 auto'},
                              config=dict(displayModeBar=False)
                              )
                ]),
                 
                html.Div(className='row',style=dict(marginTop=40),children=[
                    html.Div(className='col-sm-6',children=[
                        html.Div(className='form-group',children=[
                            dcc.Textarea(value=lower_patients,
                                style=dict(fontFamily='Courier',fontSize=14),
                                className="form-control",
                                rows=5
                            )],
                        ),
                    ]),
                    html.Div(className='col-sm-6',children=[
                        html.Div(className='form-group',children=[
                            dcc.Textarea(value=upper_patients,
                                style=dict(fontFamily='Courier',fontSize=14),
                                className="form-control",
                                rows=5
                            )],
                        ),
                    ]),
                    html.Div(className='col-sm-3')
                ]),

                html.Div(style={'textAlign': 'center'},children=[html.H3('OncoPrint'),
                    dcc.Graph(figure=oncoprint,
                    style={'overflowX': 'scroll', 'width': '800','margin':'0 auto'},
                    config=dict(displayModeBar=False)
                    )
                ]),
            ])
        ]
    return graphs


    
##@app.callback(
##    Output('debugging', 'children'),
##    [Input('lower', 'value'),Input('upper', 'value')])
##def error_message(lower,upper): 
##    if lower==None and upper==None:
##        lower=50
##        upper=50
##    elif lower==None:
##        pass
##    elif upper==None:
##        pass
##    else:
##        lower=int(lower)
##        upper=int(upper)
##        if lower+upper>100:
##            return "warning, your values exceed 100"

server=app.server

if __name__ == '__main__':
    app.run_server(debug=True)
