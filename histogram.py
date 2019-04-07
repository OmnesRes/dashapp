import plotly
import plotly.graph_objs as go
import numpy as np


##read some data from OncoLnc
f=open('donson.csv')
f.readline()
patients,days,status,expression=zip(*[i.split(',')[:-1] for i in f])


##This trace is needed for the patient names to show up on hover, but I made the markers invisible
data = [go.Histogram(
    x=expression,
    nbinsx=100,
    hoverinfo='none'
    )]


##The vertical lines are made here with the shapes option:
layout = go.Layout(title = 'Histogram',

    yaxis = dict(zeroline = False,
            showgrid = False,
            showticklabels=True,
            title="Count",
            fixedrange=True),
    xaxis = dict(zeroline = False,
            showgrid = False,
            showticklabels=True,
            title="Expression"),
    hoverlabel=dict(bgcolor='white',
                    font=dict(color='black',size=24))
)

fig = go.Figure(data=data, layout=layout)
plotly.offline.plot(fig,auto_open=False,filename='histogram.html')
