
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

layout = go.Layout(title = 'Gene Expression',

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

histogram_expression = go.Figure(data=data, layout=layout)



data = [go.Histogram(
    x=[i[6] for i in patient_data],
    nbinsx=100,
    hoverinfo='none'
    )]

layout = go.Layout(

    yaxis = dict(zeroline = False,
            showgrid = False,
            showticklabels=False,
            title="Count",
            fixedrange=True),
    xaxis = dict(zeroline = False,
            showgrid = False,
            showticklabels=True,
            title="Age",
            fixedrange=True,
            ),
    hoverlabel=dict(bgcolor='white',
                    font=dict(color='black',size=24)),
    dragmode='select',
    selectdirection='h',
    margin=go.layout.Margin(
                r=0,
                b=120,
                t=0,
                l=20
    )
)

histogram_age = go.Figure(data=data, layout=layout)



labels=['Male','Female']
values=[len([i for i in patient_data if i[5]==0]),len([i for i in patient_data if i[5]==1])]

data=[go.Pie(labels=labels,
             values=values,
             hoverinfo='label+percent',
             textinfo='value')]
layout = go.Layout(margin=go.layout.Margin(
                    pad=0,
                    r=0,
                    b=0,
                    t=0
                    ),
                   legend=dict(x=.6,
                        y=.95,
                        orientation='v'),
                   )
pie_sex=go.Figure(data=data, layout=layout)



labels=['Grade 1','Grade 2', 'Grade 3', 'Grade 4']
values=[len([i for i in patient_data if i[4]==1]),len([i for i in patient_data if i[4]==2]),
        len([i for i in patient_data if i[4]==3]),len([i for i in patient_data if i[4]==4])]

data=[go.Pie(labels=labels,
             values=values,
             hoverinfo='label+percent',
             textinfo='value')]
layout = go.Layout(margin=go.layout.Margin(
                    pad=0,
                    r=0,
                    b=0,
                    t=0
                    ),
                   legend=dict(x=.8,
                        y=.95,
                        orientation='h'),
                   )

pie_grade=go.Figure(data=data, layout=layout)



app.layout = html.Div(children=[
    html.Div(className='row',children=[


        html.Div(className='col-sm-3',style={'padding-left':'50px'},children=[
            'Summary Reports',
            dcc.Dropdown(id='selections',
                         options=[
                            {'label': 'Expression', 'value': 'exp'},
                            {'label': 'Demographics', 'value': 'dem'}
                         ],
                         value=['surv', 'exp', 'dem'],
                         multi=True
            ),
        ]),
        html.Div(className='col-sm-3'
        ),
        html.Div(className='col-sm-6',style={'padding-left':'50px'},children=[
            'Selections',
            dcc.Dropdown(id='selection',
                         options=[
                         ],
                         value=[],
                         multi=True
            ),
        ]),
    ]),

    html.Div(id='debugging',style=dict(textAlign='center',fontSize=24,color='red')),
    html.Div(id='temp_value',style={'display': 'none'},children='50'),
    html.Div(className='row',children=[
        html.Div(className='col-sm-6',children=[
            html.Div(id='demographics',style={'display': 'none'},className='row',children=[
                    html.Div(className='col-sm-4',style={'padding': '0'},children=[html.Div('Age',style={'text-align':'center'}),
                                                                                            dcc.Graph(id='age',figure=histogram_age,config=dict(displayModeBar=False))]),
                    html.Div(className='col-sm-4',style={'padding': '0'},children=[html.Div('Sex',style={'text-align':'center'}),
                                                                                   dcc.Graph(id='sex',figure=pie_sex,config=dict(displayModeBar=False))]),
                    html.Div(className='col-sm-4',style={'padding': '0'},children=[html.Div('Grade',style={'text-align':'center'}),
                                                                                   dcc.Graph(id='grade',figure=pie_grade,config=dict(displayModeBar=False))]),
            ]),
            html.Div(className='col-sm-12',children=[
                html.Div(id='expression',style={'display': 'none'},className='col-sm-12',children=[
                    html.Div(dcc.Graph(id='histogram',figure=histogram_expression,config=dict(displayModeBar=False)))
                ]),
            ])
        ]),

        html.Div(className='col-sm-6',style={'padding-left':'50px'},children=[
            dcc.Tabs(id="tabs", value='kaplan', children=[
                dcc.Tab(label='Survival', value='kaplan'),
                dcc.Tab(label='Expression', value='box'),
                dcc.Tab(label='Data', value='data'),
                dcc.Tab(label='OncoPrint', value='oncoprint')
            ]),
            html.Div(id='forms',style={'display': 'none'},className='col-sm-12',children=[
                    html.Form(className='col-sm-12',children=[
                        html.Div(className='row',children=[
                            html.Div(className='col-sm-4'),
                            html.Div(className='col-sm-4',children=[
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
            html.Div(id='tabs-content')
        ]),
    ]),
])




@app.callback(
    Output('demographics','style'),
    [Input('selections', 'value')]
    )

def show_expression(selections):
    if 'dem' in selections:
        style={'margin': '0 auto'}
    else:
        style={'display': 'none'}
    return style
        


@app.callback(
    Output('expression','style'),
    [Input('selections', 'value')]
    )

def show_expression(selections):
    if 'exp' in selections:
        style={'margin': '0 auto'}
    else:
        style={'display': 'none'}
    return style
        

        
@app.callback(
    [Output('tabs-content','children'),
     Output('forms','style')],
    [Input('lower', 'value'),
     Input('upper', 'value'),
     Input('histogram', 'selectedData'),
     Input('tabs', 'value'),
     Input('selections', 'value')
     ]
    )

def update_tabs(lower,upper,selection,tabs,selections):
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

    if tabs=='kaplan':

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
        return html.Div(style={'textAlign': 'center'},children=[html.H3('Kaplan'),
                    dcc.Graph(figure=kaplan_plot,
                              style={'margin':'0 auto'},
                              config=dict(displayModeBar=False)
                              )
                ]), None

        

    elif tabs=='data':
        first_line='{0:<15} {1:<5} {2:>9} {3:>12}  {4:>14}  {5:>16}  {6:>18}'.format('Patient','Days','Status', 'Grade', 'Sex', 'Age', 'Expression\n')
        lower_patients=first_line+''.join(['{0:<15} {1:<5} {2:>9} {3:>12}  {4:>14}  {5:>16}  {6:>18}\n'.format(i[3],str(i[0]),'Alive' if i[1]==0 else 'Dead',i[4],i[5],i[6],i[2]) for i in bottom])
        upper_patients=first_line+''.join(['{0:<15} {1:<5} {2:>9} {3:>12}  {4:>14}  {5:>16}  {6:>18}\n'.format(i[3],str(i[0]),'Alive' if i[1]==0 else 'Dead',i[4],i[5],i[6],i[2]) for i in top])
        return [html.Div(className='col-sm-12',style={'margin-top':'20'},children=[
                   html.Div(className='form-group',children=[
                            dcc.Textarea(value=lower_patients,
                                style=dict(fontFamily='Courier',fontSize=14),
                                className="form-control",
                                rows=10
                            )],
                        ),
                    ]),
                html.Div(className='col-sm-12',children=[
                    html.Div(className='form-group',children=[
                        dcc.Textarea(value=upper_patients,
                            style=dict(fontFamily='Courier',fontSize=14),
                            className="form-control",
                            rows=10
                        )],
                    ),
                ])],{'display': 'none'}
    elif tabs=='box':
        y0 = [i[2] for i in bottom]
        y1 = [i[2] for i in top]

        if toggle==True:
            trace0_name="Selected"
        else:
            trace0_name="Lower"

            
        trace0 = go.Box(
            y=y0,
            fillcolor='blue',
            name=trace0_name
        )

        if toggle==True:
            trace1_name="Not Selected"
        else:
            trace1_name="Higher"


        trace1 = go.Box(
            y=y1,
            fillcolor='red',
            name=trace1_name
        )


        data = [trace0, trace1]

        layout = go.Layout(title = 'Boxplot',

            yaxis = dict(zeroline = False,
                    showgrid = False,
                    showticklabels=True,
                    title="Reads",
                    fixedrange=True),
            xaxis = dict(zeroline = False,
                    showgrid = False,
                    showticklabels=True,
                    fixedrange=True,
                    ),
            hoverlabel=dict(bgcolor='white',
                            font=dict(color='black',size=24)),
        )

        boxplot = go.Figure(data=data, layout=layout)
        return html.Div(style={'textAlign': 'center'},children=[html.H3('Box Plot'),
                    dcc.Graph(figure=boxplot,
                    )
                ]),{'display': 'none'}

        


    else:
        data = [go.Scatter(
        x=list(range(0,len(bottom+top))),
        y=[1]*len(patients),
        text=[i[3] for i in bottom+top],
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
        return html.Div(style={'textAlign': 'center'},children=[html.H3('OncoPrint'),
                    dcc.Graph(figure=oncoprint,
                    style={'overflowX': 'scroll', 'width': '800','margin':'0 auto'},
                    config=dict(displayModeBar=False)
                    )
                ]),{'display': 'none'}





@app.callback(
    [Output('selection', 'options'),
     Output('selection', 'value')],
    [Input('sex', 'clickData'),
     Input('grade', 'clickData'),
     Input('age', 'selectedData'),
     Input('histogram', 'selectedData')],
    [State('selection', 'options'),
     State('selection', 'value')])

def update_selection(selection1,selection2,selected1,selected2,options,value):
    selections=[i for i in [selection1,selection2] if i!=None]
    for selection in selections:
        if selection['points'][0]['label'] not in [j for i in options for j in i.values()]:
            options.append({'label':selection['points'][0]['label'],'value':selection['points'][0]['label']})
        if selection['points'][0]['label'] not in value:
            value.append(selection['points'][0]['label'])
    if selected1:
        x_min=str(round(selected1['range']['x'][0]))
        x_max=str(round(selected1['range']['x'][1]))
        if 'Age' in [j[:3] for i in options for j in i.values()]:
            for index,i in enumerate(options):
                if 'Age' in i['label']:
                    options_index=index
            options[options_index]={'label':'Age '+x_min+'<'+x_max,\
                                    'value':'Age_'+x_min+'_'+x_max}

            for index,i in enumerate(value):
                if 'Age' in i:
                    values_index=index
            value[values_index]='Age_'+x_min+'_'+x_max
        else:
            options.append({'label':'Age '+x_min+'<'+x_max,\
                            'value':'Age_'+x_min+'_'+x_max})
            value.append('Age_'+x_min+'_'+x_max)

    if selected2:
        x_min=str(round(selected2['range']['x'][0]))
        x_max=str(round(selected2['range']['x'][1]))
        if 'Expression' in [j[:len('Expression')] for i in options for j in i.values()]:
            for index,i in enumerate(options):
                if 'Expression' in i['label']:
                    options_index=index
            options[options_index]={'label':'Expression '+x_min+'<'+x_max,\
                                    'value':'Expression_'+x_min+'_'+x_max}

            for index,i in enumerate(value):
                if 'Expression' in i:
                    values_index=index
            value[values_index]='Expression_'+x_min+'_'+x_max
        else:
            options.append({'label':'Expression '+x_min+'<'+x_max,\
                            'value':'Expression_'+x_min+'_'+x_max})
            value.append('Expression_'+x_min+'_'+x_max)
    


    
                    
    return options,value



    
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
##
##@app.callback(
##    Output('debugging', 'children'),
##    [Input('sex', 'clickData')])
##def error_message(selection): 
##    return str(selection['points'][0]['label'])







server=app.server

if __name__ == '__main__':
    app.run_server(debug=True)
