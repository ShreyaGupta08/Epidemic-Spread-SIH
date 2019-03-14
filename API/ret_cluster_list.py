import pickle
import pandas as pd

def distancefunc(i,j,data):
    dist = 0
    for k in range(1,8):
        dist = dist + abs(data.iloc[i][k]-data.iloc[j][k])
    match = 0
    b = []
    return dist
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
