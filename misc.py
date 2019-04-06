

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
f=open('donson.csv')
f.readline()
patients,days,status,expression=zip(*[i.split(',')[:-1] for i in f])
patient_data=[[int(i),0 if j=='Alive' else 1,float(k),l] for i,j,k,l in zip(days,status,expression,patients)]
patient_data.sort(key=lambda x:x[2])

