import plotly
import plotly.graph_objs as go
import numpy as np


##read some data from OncoLnc
f=open('KIRC_29980_100_0.csv')
f.readline()
patients,days,status,expression=zip(*[i.split(',')[:-1] for i in f])


##This trace is needed for the patient names to show up on hover, but I made the markers invisible
data = [go.Scatter(
    x=range(0,len(patients)),
    y=[5.5]*len(patients),
    text=patients,
    hoverinfo='text',
    mode='markers',
    marker=dict(opacity=0)
    )]


##The vertical lines are made here with the shapes option:
layout = go.Layout(title = 'Oncoprint',

    yaxis = dict(zeroline = False,
            showgrid = False,
            range=[0,10],
            showticklabels=False,
            fixedrange=True),
    xaxis = dict(zeroline = False,
            showgrid = False,
            range=[-1,120],
            showticklabels=False,),
    shapes=[dict(type='line',
                x0=i,
                y0=4.5,
                x1=i,
                y1=5.5,
                line = dict(color='green',
                            width=10))\
        for i in range(0,len(patients))],
    dragmode='pan',
    hoverlabel=dict(bgcolor='white',
                    font=dict(color='black',size=24))
)

fig = go.Figure(data=data, layout=layout)
plotly.offline.plot(fig,auto_open=False,filename='oncoprint.html')
