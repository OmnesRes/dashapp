import plotly
import plotly.graph_objs as go
import numpy as np

def kaplan(survtimes):
    h_coords=[]
    v_coords=[]
    lost=[]
    y=1
    x=0
    for i in survtimes:
        if i[1]!=1:
            lost.append([i[0],y,i[-1]])
        else:
            h_coords.append([i[0],y])
            y=1*len(survtimes[survtimes.index(i)+1:])/float(len(survtimes[survtimes.index(i):]))
            v_coords.append([i[0],h_coords[-1][-1],y,i[-1]])
            break
    newsurv=survtimes[survtimes.index(i)+1:]
    while len(newsurv)>0:
        newsurv,y,h_coords,v_coords,lost=loop(newsurv,y,h_coords,v_coords,lost)
    return (h_coords,v_coords,lost)



def loop(newsurv,y,h_coords,v_coords,lost):
    for j in newsurv:
        if j[1]!=1:
            lost.append([j[0],y,j[-1]])
        else:
            h_coords.append([j[0],y])
            y=y*len(newsurv[newsurv.index(j)+1:])/float(len(newsurv[newsurv.index(j):]))
            v_coords.append([j[0],h_coords[-1][-1],y,j[-1]])
            break
    newsurv=newsurv[newsurv.index(j)+1:]
    return (newsurv,y,h_coords,v_coords,lost)

##read some data from OncoLnc
f=open('KIRC_29980_100_0.csv')
f.readline()
patients,days,status,expression=zip(*[i.split(',')[:-1] for i in f])

survtimes=[[int(i),0 if j=='Alive' else 1,k] for i,j,k in zip(days,status,patients)]
survtimes.sort()


survtimes1=survtimes[:300]
survtimes2=survtimes[300:]

k_plot=kaplan(survtimes1)

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
    showlegend=False,
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
    marker=dict(opacity=1,symbol='line-ns-open',size=3,color='blue'),
    showlegend=False
    )

k_plot=kaplan(survtimes2)

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
    showlegend=False,
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
    marker=dict(opacity=1,symbol='line-ns-open',size=3,color='red'),
    showlegend=False
    )





data=[trace1,trace2,trace3,trace4]






####The vertical lines are made here with the shapes option:
layout = go.Layout(
    yaxis = dict(zeroline = False,
            showgrid = False,
##            range=[0,10],
            showticklabels=False,
##            fixedrange=True,
                 ),
    xaxis = dict(zeroline = False,
            showgrid = False,
##            range=[-1,120],
            showticklabels=False,),
##    dragmode='pan',
    hoverlabel=dict(bgcolor='white',
                    font=dict(color='black',size=24)),
    margin=go.layout.Margin(
        l=0,
        r=0,
        b=0,
        t=0,
        pad=0
    ),
    hovermode='closest',
)

kaplan = go.Figure(data=data, layout=layout)
##plotly.offline.plot(kaplan,auto_open=False,filename='kaplan_2.html')

