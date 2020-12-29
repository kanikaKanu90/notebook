#!/usr/bin/env python
# coding: utf-8

# In[39]:


import numpy as np
from bokeh.sampledata.iris import flowers
df = flowers 


# In[40]:


df = df.drop("species",axis=1)
arr = df.to_numpy()


# In[41]:


def pass_medoids(arr,rand_medoid):
# Use the following medoids if random medoid is set to false in the dashboard. These numbers are indices into the
# data array.
#     medoids = [24, 74, 124]
    if rand_medoid==False:
         ind = [24, 74, 124]
    elif rand_medoid==True:
          ind = np.random.randint(0, len(arr)-1 ,3)
    r=[]
    for i in ind:
        r1=arr[i]
        r.append(r1)
    return r


# In[42]:


#Function for measuring distance of data points from medoids 

def distance(dpArr,med_arr):
    m2=[]
    for k in dpArr:
        p=[]
        mj=[]
        if len(med_arr) == 4:
            mj.append(med_arr)  # if only one medoid is passed, converting it into array
            mj = np.asarray(mj)
            med_arr=mj
        for pm in med_arr :
#         d=arr[124]
          diff = abs(k-pm)
          dist = np.sum(diff)
          p.append(dist)
        m2.append(p)
    return m2


# In[43]:



#ClusterAssignment to data points

def Cluster_assignment(k,med_arr):  # k is the array of data points , med_arr is the mediod or the set of mediods passed
    m2=[]
    F=distance(k,med_arr)
    F = np.asarray(F)
    m1=F.argmin(axis=1)
    return m1


# In[44]:



def Cost_a(k,med_arr):
    m2=[]
#     if len([med_arr])==1:
#         med_arr=[med_arr]
    F=distance(k,med_arr)
    F = np.asarray(F)
    m2=F.min(axis=1)
    return m2


# In[45]:



def Cluster_cost(arr,meds):
    label= Cluster_assignment(arr,meds)
    dis2=[]
    dis = distance(arr,meds)
    new_med=meds
    avg_dsmlrty=[]*3
    print(set(label))
    for i in set(label):
        dpoint_cluster=arr[label==i]
        avg_dsmlrty.append(np.sum(Cost_a(dpoint_cluster,meds[i])))
        for dPs in dpoint_cluster:
            new_dsmlrty=np.sum(Cost_a(dpoint_cluster,dPs))
            if new_dsmlrty < avg_dsmlrty[i]:
                avg_dsmlrty[i] =  new_dsmlrty
                new_med[i]= dPs
        cost=np.sum(avg_dsmlrty)
    return new_med ,  cost

def convergence(oldMed,newMed):
    return set([tuple(x) for x in oldMed])==set([tuple(x) for x in newMed])


# In[46]:


def k_medoids(arr,pre_or_rand):
    # number of clusters:
    k = 3
    # Use the following medoids if random medoid is set to false in the dashboard. These numbers are indices into the
    # data array.
#     medoids = [24, 74, 124]
    med=pass_medoids(arr,pre_or_rand)
#     f,h =Cluster_cost(arr,pre_medoids)
    medoids,cost=Cluster_cost(arr,med)
#     print ('medoids: ' , medoids)
#     print('cost is : ' , cost)
    converged = False
    i = 1
    while (not converged):
           old_medoids = medoids.copy()
           medoids,cost = Cluster_cost(arr,med)
           converged = convergence(old_medoids, medoids)
           i += 1
    return medoids,cost


# In[73]:


medoids,cost = k_medoids(arr,False)
print('cost is : ' , cost)


# In[65]:


from bokeh.plotting import figure, output_file, show ,curdoc ,output_notebook

from bokeh.sampledata.iris import flowers
from bokeh.layouts import layout , row ,column
from bokeh.models import ColumnDataSource, Select
from bokeh.models import Div

output_notebook()

from bokeh.models import Button
button = Button(label='Cluster data')

def update_button(arr,click):
    if click== "True":
        medoids,cost = k_medoids(arr,True)
        div = Div(text="Final cost is :" + str(cost))
    else :
         medoids,cost = k_medoids(arr,False)
         div = Div(text="Final cost is :" + str(cost))
    button.on_click(update_button)
    
show(button)
show(div)


# In[64]:



def callback(attr, old, new):
    if select.value == "False":
         medoids,cost = k_medoids(arr,False)
         
    else:
         medoids,cost = k_medoids(arr,True)
    div = Div(text="Final cost is :" + str(cost))
    print(str(cost))
    return 

options=[("False"),("True")]
st=Select(value = "False",title="Random medoids",options=options)
st.on_change('value', callback)
show(st)

