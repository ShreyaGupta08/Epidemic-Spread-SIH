
# coding: utf-8

# In[8]:


import pickle
import pandas as pd


# In[15]:


def distancefunc(i,j,data):
#     print(i,j)
    dist = 0
    for k in range(1,8):
#         print(k)
        dist = dist + abs(data.iloc[i][k]-data.iloc[j][k])
    match = 0
#     a = data.iloc[i][5].split(', ')
#     a=[]
#     if data.iloc[i][0] in riverdic_final.keys():
#         a = riverdic_final[data.iloc[i][0]]
#     b = data.iloc[j][5].split(', ')
    b = []
#     if data.iloc[j][0] in riverdic_final.keys():
#         b = riverdic_final[data.iloc[j][0]]
#     for river in a:
#         if river in b:
#             match = match + 2
#     if match == 0:
#         dist += 1
#     else:
#         dist += 1/match
    return dist


# In[16]:


data = pd.read_csv('new_clustering.csv')
data.head()


# In[21]:


def ret_cluster_list(name):
    data = pd.read_csv('new_clustering.csv')
    for i in range(0,50):
#     print(data.iloc[i][2])
        data.iloc[i,2] = data.iloc[i,2][:-1]
        data.iloc[i,2] = float(data.iloc[i,2])
    index = {}
    for i in range(0,50):
        index[data.iloc[i][0]] = i
    with open("final_list.txt", "rb") as fp:
        list_final = pickle.load(fp)
    l = []
    for i in list_final:
        if name in i:
            l=i
            break
    dist = []
    for k in l:
        dist.append((distancefunc(index[name],index[k],data),k))
    dist.sort()
    color = {}
    c = '#ffff99'
    for i in range(0,len(dist)):
        if len(dist)-i<=4:
            c = '#ffff00'
        if len(dist)-i<=2:
            c = '#cccc00'
        color[dist[i][1]] = c
    return color


# In[22]:


print(ret_cluster_list('Ujjain'))

