import networkx as nx                                                               #Importing networkx as nx to use it while making graph.
import pandas as pd                                                                 #Importing pandas as pd to use it in file handling.
import matplotlib.pyplot as plt                                                     #Importing matplotlib.pyplot to plot the graph
import random                                                                       #Importing random library to select random node.
import numpy as np 


#PART-I: FINDING THE LEADER


file=pd.read_excel("graph.xlsx")                                                    #Storing the excel file in file.

alpha=pd.DataFrame(file, columns=["Email Address"])                                 #alpha has the entries which are present in the column which is named as "Email Address".

li=alpha.values.tolist()                                                            #Converting it into a list li.

list1=[]                                                                            #Creating a empty list.                                                                                                                   
for i in range(0,len(li)):                                                          #Using for loop to append the nodes.
    a=li[i][0].upper()[0:11]                                                        #Capitalising the alphabets.
    list1.append(a)                                                                 #Appending all the nodes into a list called list1.
#print(list1)
Graph=nx.DiGraph()                                                                  #Making it a bidirectional graph.
for i in range(0,len(list1)):
    Graph.add_node(list1[i])                                                        #Adding all the nodes the graph.

for j in range(1,31):                                                               #Using for loop.
    l=pd.DataFrame(file, columns=["Your Impression "+ str(j)]).values.tolist()      #USing pandas data frame to access coloumns and then converting it into a list.
    for i in range(0,len(list1)):
        if str(l[i][0])!="nan":                                                     #Not considering "nan", because they are created due to empty blanks in the excel.
            Graph.add_edge(list1[i],l[i][0].upper()[-11:])                          #Creating the edges.

nx.draw(Graph)
plt.show()

nodes=list(Graph.nodes)                                                             #Making a list of nodes(143 nodes).
a=random.choice(nodes)                                                              #a gives us a random node.
dict={}                                                                             #Creating a empty dictionary.
for i in nodes:                                                                     
    dict[i]=0                                                                       #Now, we have all the nodes as keys in the dictionary. 
for i in range(0,1000000):                                                          
    if len(list(Graph.neighbors(a)))!=0:                                            #If a node has not adjacent nodes.
        b=random.choice(list(Graph.neighbors(a)))                                   #Choosing one such node randomly.
        dict[b]=dict[b]+1                                                           #Adding value 1 in the dictionary to the choosen node.
        a=b                                                                         #Then making a=b
    else:
        a=random.choice(nodes)                                                      #Else, choosing randomly again.This loop runs a million times and the key with highest value gives us the leader.
v=[]                                                                                #Creating a list to store all the values.
for i in nodes: 
    v.append(dict[i])                                                               #Storing all the values in the list v.

for i in range(0,len(nodes)):
    if max(v)==dict[nodes[i]]:                                                      
        print("Entry Number of Leader: ",nodes[i])                                  #Printing the node with has max value in the dictionary, i.e., leader.                                                  





#PART-II : TO FIND THE MISSING LINKS.
M=nx.to_numpy_array(Graph)                                                          #M represents the adjacency matrix.
indices=[]                                                                          #The list indices is an empty list.
for i in range(0,143):                                                              #Using for loop.
    for j in range(0,143):                                                          #Using for loop.
        if M[i][j]==0:                                                              #If 0 is present in row with index i and column with index j.
            indices.append([i,j])                                                   #Appending those in the list indices.
k=len(indices)-150
M1=M                                                                                #M1 is duplicate of M.
g=[]                                                                                 #g represents the missing links.
for i in range(1, k):                                                               #For loop.
    M1_row=np.delete(M1, indices[i][0], axis=0)                                     #We have ith element of indices, which is a list. Removing the row with index equal to the first element of that list.
    T=np.delete(M1_row, indices[i][1], axis=1)                                      #Similarly removing removing the column also. Now, T is (n-1)x(n-1) matrix.
    B=T[indices[i-1][0]]                                                            #Taking (i-1)th row in T i.e., ith row in M without 0.
    #Tx=B, gives us the coeeficients of linear combination.
    x, a, b, c=np.linalg.lstsq(T, B, rcond=None)                                    #To get the x in Tx=B
    C=np.delete(M[:, indices[i][1]],indices[i][0])                                  #C is the column matrix containing the chosen zero, but without considering the zero.
    value= C @ x                                                                    #value is the matrix multiplication of column and x which gives a 1 x 1 matrix.
    if value>1:                                                                     #If value is greater than 1.
        M[indices[i][0],indices[i][1]]=1                                            #We will update the matrix by replacing 0 with 1.
        g.append(indices[i])                                                        #Appending the indices of missing links.
    if value<1:                                                                     #If value is less than 1.
        M[indices[i][0],indices[i][1]]=0                                            #We will keep the zero as zero.
print(M)
print("Number of missing links : ", len(g))
print(g)




#PART-III: Proposing a new question and solving it.

#Question: We have 143 nodes and atmax 30 outgoing edges from each node, so find the transitivity percentage. Transitivity percentage is defined as the ratio of (number of transitive cases we have) to (number of transitive cases possible) multiplied by 100.

#Answer:


#Let's first find out the total number of transitive cases we have(numerator in the ratio).

x=list(Graph.edges)                                                             #x is a list containing all the edges in the social network we have.                             
a1=0                                                                            #a1 represents total number of transitive cases we have in the social network.
for i in range(0,len(x)):                                                       #Using for loop.                        
    for j in range(0,len(x)):                                                   #For loop-2.
        if x[i][1]==x[j][1] and (x[i][0],x[j][1]) in x:                         #If we come across a transitive case.
            a1=a1+1                                                             #We add 1 to a1.

print(a1/3)                                                                    #We print a1/3 because there are repeatations. For example, abc, bca and cab are same. We get this value as 31996.

#Now, let's find out total number of transitive cases possible.
a2=0                                                                            #a2 represents total number of possible transitive cases in the social network.
for i in range(0,143):                                                          #For loop.
    l=[]
    for j in range(0,143):                  
        if (nodes[i],nodes[j]) in x:    
            l.append(nodes[j])                                                  
    a2=a2+2*(len(l))*(len(l)-1)/2

print(a2)                                                                      #We will get the value as 89760.

Transitivity_percentage=((a1/3)/(a2))*100

print("Transitivity percentage: ",Transitivity_percentage)


    







