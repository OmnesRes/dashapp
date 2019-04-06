
# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objs as go
from dash.dependencies import Input, Output

external_stylesheets = ["https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css",
                        {'rel':"stylesheet",
                     'href':"https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css",
                     'integrity':"sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T",
                     'crossorigin':"anonymous"}]




external_scripts = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets,external_scripts=external_scripts)


##load functions and data
from misc import *

##OncoPrint

data = [go.Scatter(
    x=range(0,len(patients)),
    y=[1]*len(patients),
    text=patients,
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
            range=[-1,len(patients)+1],
            ),
    shapes=[dict(type='line',
                x0=i,
                y0=0,
                x1=i,
                y1=1,
                line = dict(color='green',
                            width=10))\
        for i in range(0,len(patients))],
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

app.layout = html.Div(children=[

    html.Div(className='col s12',children=[
        html.Form(className='col s12',children=[
            html.Div(className='row',children=[
                html.Div(className='col s4'),
                html.Div(className='col s4',children=[
                    html.Div(className='col s2'),
                    html.Div(className='input-field col s4',children=[
                        dcc.Input(id='lower', type='text',placeholder='50'),
                        html.Label(htmlFor='lower',children='Lower')]),
                    html.Div(className='input-field col s4',children=[
                        dcc.Input(id='upper', type='text',placeholder='50'),
                        html.Label(htmlFor='upper',children='Upper')]),
                    html.Div(className='col s2')
                    ]),
                html.Div(className='col s4')])
            ]),

    html.Div(id='debugging',style=dict(textAlign='center',fontSize=24,color='red')),
    html.Div(id='temp_value',style={'display': 'none'},children='50'),
        

    html.Div(children=[
        html.Div(style={'textAlign': 'center'},children=[html.H3('Kaplan'),
                dcc.Graph(className='col-sm-6',style={'margin':'0 auto'},id='kaplan',
                config=dict(displayModeBar=False))]
                 )]
             ),

    html.Div(className='row',style=dict(marginTop=40),children=[
        html.Div(className='col-sm-3'),
        html.Div(className='col-sm-3',children=[
            html.Div(className='form-group',children=[
                dcc.Textarea(style=dict(fontFamily='Courier',fontSize=14),id='lower_patients',className="form-control",rows=5)],
                ),
            ]),
        html.Div(className='col-sm-3',children=[
            html.Div(className='form-group',children=[
                dcc.Textarea(style=dict(fontFamily='Courier',fontSize=14),id='upper_patients',className="form-control",rows=5)],
                ),
        html.Div(className='col-sm-3')]
            )]
        ),


    html.Div(style={'textAlign': 'center'},children=[html.H3('OncoPrint'),
            dcc.Graph(id='oncoprint',
            style={'overflowX': 'scroll', 'width': '1500','margin':'0 auto'},
            config=dict(displayModeBar=False))]),
    ])

])




@app.callback(
    [Output('kaplan', 'figure'),
     Output('lower_patients', 'value'),
     Output('upper_patients', 'value'),
     Output('oncoprint','figure')],
    [Input('lower', 'value'),Input('upper', 'value')])

def update_kaplan(lower,upper):
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

    trace1 = go.Scatter(
        x=[0]+[i[0] for i in k_plot[0]]+x_end,
        y=[i[1] for i in k_plot[0]]+[k_plot[1][-1][2]]+y_end,
        hoverinfo='text+x+y',
        text=['']+[i[-1] for i in k_plot[1]],
        mode='lines',
        name='Low Expression<br>N='+str(len(bottom)),
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

    trace3 = go.Scatter(
        x=[0]+[i[0] for i in k_plot[0]]+x_end,
        y=[i[1] for i in k_plot[0]]+[k_plot[1][-1][2]]+y_end,
        hoverinfo='text+x+y',
        text=['']+[i[-1] for i in k_plot[1]],
        mode='lines',
        legendgroup='higher',
        name='High Expression<br>N='+str(len(top)),
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
                showticklabels=False,
                     ),
        xaxis = dict(zeroline = False,
                showgrid = False,
                showticklabels=False,
                rangemode= 'nonnegative'),
        hoverlabel=dict(bgcolor='white',
                        font=dict(color='black',size=24)),
        legend=dict(x=.75,y=1),
        margin=go.layout.Margin(
            l=5,
            r=0,
            b=0,
            t=0,
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

    return kaplan_plot,lower_patients,upper_patients,oncoprint



    
@app.callback(
    Output('debugging', 'children'),
    [Input('lower', 'value'),Input('upper', 'value')])
def error_message(lower,upper): 
    lower=int(lower)
    upper=int(upper)
    if lower+upper>100:
        return "warning, your values exceed 100"

server=app.server

if __name__ == '__main__':
    app.run_server(debug=True)